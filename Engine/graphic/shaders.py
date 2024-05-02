""" Managing and creating shaders
"""
from loguru import logger
# Engine
from Engine.data.constants import (
    EMPTY, ZERO, BINARY, NULL,
    VERTEX_SHADER, FRAGMENT_SHADER,
    COMPUTE_SHADER, GEOMETRY_SHADER,
)
from Engine.scripts.app_data import SafetyDict
from Engine.data.config import File
from Engine import graphic


class Shader:
    def __init__(self, _path, shader_type, file_type=NULL):
        """ Shader """
        self.id = EMPTY  # him id
        """ selecting a type and creating a program """
        if shader_type & COMPUTE_SHADER:
            self.program = graphic._Graphics.context.compute_shader(
                self.__read_file__(_path + '.glsl', file_type)
            )
        else:
            program_kwargs = {}
            if shader_type & VERTEX_SHADER and shader_type & FRAGMENT_SHADER:
                program_kwargs['vertex_shader'] = self.__read_file__(_path + '.vert', file_type)
                program_kwargs['fragment_shader'] = self.__read_file__(_path + '.frag', file_type)
            if shader_type & GEOMETRY_SHADER:
                program_kwargs['geometry_shader'] = self.__read_file__(_path + '.glsl', file_type)
            # simple program creating
            self.program = graphic._Graphics.context.program(**program_kwargs)
    
    @staticmethod
    def __read_file__(path: str, _type) -> str:
        """ read shader from file with path """
        if _type is NULL:
            with open(path) as f:
                shader_source = f.read()
            return shader_source
        
        elif _type is BINARY:
            from dill import load
            with open(path + '.dill', 'br') as bf:
                shader_source = load(bf)
            return shader_source
        
        else:
            raise TypeError(f'cen\'t load shader from {_type} file type')
    
    def use(self):
        ...
    
    def __setitem__(self, u_name, u_value):
        try:
            self.program[u_name] = u_value
        except KeyError:
            logger.error(f'uniform `{u_name}` not used in shader')
    
    def __getitem__(self, u_name):
        return self.program.get(u_name, EMPTY)
    
    def __release__(self):
        self.program.release()
        if self.id is not EMPTY:
            ShadersProgram.roster.pop(self.id)


class ShadersProgram:
    roster: dict[str, Shader] = SafetyDict(default_key='default-main')
    
    def __new__(cls, *args, **kwargs):
        if len(cls.roster) is ZERO:
            cls.roster['default-main'] = Shader(
                rf'{File.__ENGINE_DATA__}\shaders\default\main',
                VERTEX_SHADER | FRAGMENT_SHADER
            )
    
    @classmethod
    def __getitem__(cls, item):
        return cls.roster[item]
    
    @classmethod
    def add(cls, key: str, value: Shader):
        cls.roster[key] = value
        value.id = key
    
    @classmethod
    def __release__(cls):
        for shader in cls.roster.values():
            shader.__release__()
    
    @classmethod
    def clear(cls):
        cls.__release__()
        cls.roster.clear()

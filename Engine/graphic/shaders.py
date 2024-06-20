""" Managing and creating shaders
"""
from Engine import logger
# Engine
from Engine.data.constants import (
    VERTEX_SHADER, FRAGMENT_SHADER,
    COMPUTE_SHADER, GEOMETRY_SHADER,
    ZERO,
)  # data
from Engine.scripts.app_data import SafetyDict
from Engine.data.config import File
from Engine import graphic
from Engine.objects.meta_data import ShaderMetaData


class Shader:
    def __init__(self, metadata: ShaderMetaData, shader_path):
        """ Shader """
        self._metadata = metadata  # him id
        """ selecting a type and creating a program """
        program_kwargs = {}
        if metadata.shader_type & COMPUTE_SHADER:
            self.program = graphic.Graphics.context.compute_shader(
                self.__read_file__(shader_path + '.glsl', metadata.file_type)
            )
        elif metadata.shader_type & GEOMETRY_SHADER:
            program_kwargs['geometry_shader'] = self.__read_file__(shader_path + '.glsl', metadata.file_type)
        elif metadata.shader_type & VERTEX_SHADER and metadata.shader_type & FRAGMENT_SHADER:
            program_kwargs['vertex_shader'] = self.__read_file__(shader_path + '.vert', metadata.file_type)
            program_kwargs['fragment_shader'] = self.__read_file__(shader_path + '.frag', metadata.file_type)
        else:
            raise TypeError(f'Wrong shader type')
        # simple program creating
        self.program = graphic.Graphics.context.program(**program_kwargs)
    
    @staticmethod
    def __read_file__(path: str, _type) -> str:
        """ read shader from file with path """
        if _type == 'str':
            with open(path) as f:
                shader_source = f.read()
            return shader_source
        elif _type == 'bin':
            from pickle import load
            with open(path + '.pfl', 'br') as bf:
                shader_source = load(bf)
            return shader_source
        else:
            raise TypeError(f'cen\'t load shader from {_type} file type')
    
    def __setitem__(self, u_name: str, u_value):
        if u_name[0:3] == 'u_':
            try:
                self.program[u_name] = u_value
            except KeyError:
                logger.error(f'uniform `{u_name}` not used in shader')
        else:
            raise AttributeError('Cant change not `u` value')
    
    def __getitem__(self, u_name):
        if u_name[0:3] == 'u_':
            return self.program.get(u_name, ZERO)
        else:
            raise AttributeError('Cant get not `u` value')
    
    def __release__(self):
        ShadersProgram.roster.pop(self._metadata.ID)


class ShadersProgram:
    roster: dict[str, Shader] = SafetyDict(default_key='default-main')
    
    def __new__(cls, *args, **kwargs):
        if len(cls.roster) is ZERO:
            def_shader = Shader(
                metadata=ShaderMetaData(
                    type_id='default_engine_shader',
                    ID='default_engine_main_shader',
                    shader_type=VERTEX_SHADER | FRAGMENT_SHADER
                ),
                shader_path=rf'{File.APPLICATION_path}/{File.SHADER_dir}/default/main'
            )
            cls.add(def_shader)
    
    @classmethod
    def __getitem__(cls, item):
        return cls.roster[item]
    
    @classmethod
    def add(cls, _value: Shader):
        cls.roster[_value._metadata.ID] = _value
    
    @classmethod
    def pop(cls, _id):
        cls.roster.pop(_id)
    
    @classmethod
    def __release__(cls):
        for shader in cls.roster.values():
            shader.__release__()
    
    @classmethod
    def clear(cls):
        cls.__release__()
        cls.__new__(cls)

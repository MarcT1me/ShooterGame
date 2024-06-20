""" Managing and creating shaders
"""
from pygame import image, Surface, transform
# Engine
from Engine.data.constants import ZERO
from Engine.scripts.app_data import SafetyDict
from Engine.data.config import File
from Engine import graphic, OPENGL
from Engine.objects.meta_data import TextureMetaData


class Texture:
    def __init__(self, metadata: TextureMetaData, surf: Surface):
        """ create MGL texture """
        self.metadata = metadata  # him id
        
        self.surf: Surface = surf
        if graphic.Graphics.data.flags & OPENGL:
            self.texture: graphic.Graphics.context.texture = graphic.Graphics.context.texture(
                surf.get_size(), 3 + metadata.is_alpha
            )
            self.texture.filter = metadata.filters
            self.texture.build_mipmaps()
            self.texture.anisotropy = metadata.anisotropy
    
    @staticmethod
    def from_surf(metadata: TextureMetaData, texture_surf: Surface):
        """ Load texture from surf """
        return Texture(metadata, transform.flip(texture_surf, flip_x=False, flip_y=True))
    
    @staticmethod
    def from_file(metadata: TextureMetaData, texture_path: str):
        """ Load texture from image """
        return Texture.from_surf(metadata, image.load(texture_path))
    
    def update(self):
        self.texture.write(image.tostring(self.surf, self.metadata.format))
    
    def use(self):
        self.texture.use(self.metadata.u_id)
    
    @staticmethod
    def __read_file__(path: str) -> Surface:
        """ read shader from file with path """
        return image.load(path)
    
    def __release__(self):
        TextureProgram.roster.pop(self.metadata.ID)


class TextureProgram:
    roster: dict[str, Texture] = SafetyDict(default_key='default-main')
    
    def __new__(cls, *args, **kwargs):
        if len(cls.roster) is ZERO:
            def_texture = Texture.from_file(
                TextureMetaData(
                    type_id='default_engine_texture',
                    ID='default_engine_main_texture',
                ),
                texture_path=rf'{File.__ENGINE_DATA__}/ico.ico'
            )
            cls.add(def_texture)
    
    @classmethod
    def __getitem__(cls, item):
        return cls.roster[item]
    
    @classmethod
    def add(cls, _value: Texture):
        cls.roster[_value.metadata.ID] = _value
    
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

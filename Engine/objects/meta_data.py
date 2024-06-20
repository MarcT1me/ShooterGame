from dataclasses import dataclass, field
from uuid import uuid4
import glm  # math
import Engine
from moderngl import LINEAR_MIPMAP_LINEAR, LINEAR


@dataclass
class MetaData:
    """
    MainData
    type_id - str - some your type
    ID - str - obj id in dict
    """
    type_id: str = field(default=str(Engine.EMPTY))
    ID: str = field(default_factory=uuid4)  # unique object id
    

@dataclass
class ShaderMetaData(MetaData):
    """
    MetaData:
        type_id - str - some your type
        ID - str - obj id in dict
    ShaderMetaData:
        shader_type - int - Engine type
        file_type - type - file type
    """
    shader_type: int = field(default=Engine.VERTEX_SHADER | Engine.FRAGMENT_SHADER)
    file_type: str = field(default='str')
    

@dataclass
class TextureMetaData(MetaData):
    """
    MetaData:
        type_id - str - some your type
        ID - str - obj id in dict
    TextureMetaData:
        is_alpha - bool - Engine type
    """
    is_alpha: bool = field(default=True)
    
    flip_x: bool = field(default=False)
    flip_y: bool = field(default=True)
    
    filters: int = field(default=(LINEAR_MIPMAP_LINEAR, LINEAR))
    anisotropy: float = field(default=32.0)
    format: str = field(default='RGBA')
    
    u_id: int = field(default=0)


@dataclass
class ObjectMetaData(MetaData):
    pos: tuple[float, float, float] | glm.vec3 = field(default=glm.vec3(0))
    time_list: dict = field(default_factory=dict)
    
    def __post_init__(self):
        self.pos = glm.vec3(self.pos)


@dataclass
class ModelMetaData(ObjectMetaData):
    rot: tuple[float, float, float] | glm.vec3 = field(default=glm.vec3(0))
    scale: tuple[float, float, float] | glm.vec3 = field(default=glm.vec3(0))
    
    tex_id: str = field(default='default')
    vao_id: str = field(default='default')
    shader_id: str = field(default='default')
    
    def __post_init__(self):
        super().__post_init__()
        self.rot = glm.vec3(self.rot)
        self.scale = glm.vec3(self.scale)

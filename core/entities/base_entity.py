from Engine.lscript import vec3, increment_creator
from uuid import uuid4


class Entity:
    
    __increment_generator__ = increment_creator()
    increment = lambda: next(Entity.__increment_generator__)
    
    def __init__(self, _id=None, pos=0, rotation=0):
        self.id = _id if _id is not None else uuid4()
        self.not_render = False
        
        self.pos = vec3(pos)
        self.rot = vec3(rotation)
    
    def event(self, event):
        ...
    
    def update(self):
        ...
    
    def render(self):
        ...

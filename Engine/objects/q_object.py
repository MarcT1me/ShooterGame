from Engine.objects.meta_data import *
from pygame.event import Event


class QObject:
    def __init__(self, metadata: MetaData):
        self.metadata = metadata
        
    def event(self, event: Event):
        ...
    
    def update(self):
        ...
    
    def render(self):
        ...
        
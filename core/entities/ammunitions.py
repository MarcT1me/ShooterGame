import pygame as pg
from copy import copy
from core.entities.base_entity import Entity
from Engine import *


class BaseAmmo(Entity):
    stack_sizes = {
        0:    0,
        5.56: 30,
        7.62: 30,
        30.0: 10,
    }
    
    def __init__(self, _type: float, dropped=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texture = pg.image.load(
            f'{config.File.APPLICATION_path}\\presets\\ammo\\ammo_{_type}.png'
        )
        self.dropped = dropped
    
    def drop(self, _pos: vec3):
        self.pos = copy(_pos)
        self.dropped = True
    
    def render(self):
        if self.dropped:
            App.window.screen.blit(
                self.texture,
                vec2(self.pos.xy - App.window.camera.pos.xy)
            )

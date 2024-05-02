import pygame as pg
from Engine import *
from math import inf
# core
from core.entities.base_entity import Entity


class Bullet(Entity):
    def __init__(self, speed=1, damage=1, distance=inf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_pos: vec3 = self.pos
        self.distance: float = distance
        self.damage = damage
        self.speed = speed
    
    def update(self):
        if self.not_render:
            App.scene.delete(self.id)
        
        self.pos += normalize(
            vec3(
                cos(-radians(self.rot.z)),
                sin(-radians(self.rot.z)),
                0
            )
        )*self.speed*App.clock.delta
    
    def render(self):
        pg.draw.circle(
            surface=App.window.screen._win,
            color='red',
            center=self.pos.xy - App.window.camera.pos.xy,
            radius=20
        )

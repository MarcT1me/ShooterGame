import pygame as pg
from Engine import *
# core
from core.entities.base_entity import Entity
from math import inf
from copy import copy


class Bullet(Entity):
    def __init__(self, speed=1, damage=1, max_distance=inf, max_time=inf, size=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_pos: vec3 = copy(self.pos)
        self.max_distance = max_distance
        
        self.start_time = clock.get_ticks()
        self.max_time: float = max_time
        
        self.damage = damage
        self.speed = speed
        self.size = size
        self.latest_pos = self.start_pos
    
    def update(self):
        self.latest_pos = copy(self.pos)
        if any(
                (
                        self.not_render,
                        clock.get_ticks() - self.start_time > self.max_time,
                        length(self.pos - self.start_pos) > self.max_distance
                )
        ):
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
            radius=self.size
        )

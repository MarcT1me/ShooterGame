import pygame as pg

from core.entities.base_entity import Entity
from core.entities.bullet import Bullet
from random import choice as random_choice
from Engine import *


class Barrel(Entity):
    barrel_names = (
        'barrel-oil1.png',
        'barrel-oil2.png'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pg.transform.scale_by(
            pg.image.load(
                f'{config.File.APPLICATION_path}\\presets\\barrels\\{random_choice(self.barrel_names)}'
            ), 3
        )
        self.health = 100
        self.frame_text_rect = pg.Rect(0, 0, 0, 0)
    
    def update(self):
        if -100 <= self.health <= 0:
            App.scene.delete(self.id)
        for i in list(App.scene.entity_list.values()):
            self.frame_text_rect = pg.Rect(*self.pos.xy, *self.image.get_size())
            if isinstance(i, Bullet):
                if self.frame_text_rect.clipline(*i.latest_pos.xy, *i.pos.xy):
                    App.scene.delete(i.id)
                    self.health -= i.damage
    
    def render(self):
        App.window.screen.blit(
            self.image,
            vec2(self.pos.xy - App.window.camera.pos.xy)
        )
        self.render_health()
    
    def render_health(self):
        
        start_pos = App.scene.entity_list['player1'].pos.xy
        end_pos = start_pos + vec2(
            cos(-radians(App.scene.entity_list['player1'].rot.z)),
            sin(-radians(App.scene.entity_list['player1'].rot.z))
        )*App.scene.distance
        
        if self.frame_text_rect.clipline(*start_pos, *end_pos) or\
                length(self.pos.xy - pg.mouse.get_pos() - vec2(App.window.camera.pos.xy)) < 100 or\
                self.health != 100:
            pg.draw.rect(
                surface=App.window.screen._win,
                color='gray',
                rect=(
                    *(self.pos - (10, 20, 0)).xy - App.window.camera.pos.xy,
                    *(100/1.5, 10)
                )
            )
            pg.draw.rect(
                surface=App.window.screen._win,
                color='green' if self.health > 30 else 'red',
                rect=(
                    *(self.pos - (10, 20, 0)).xy - App.window.camera.pos.xy,
                    *(int(self.health/1.5), 10)
                )
            )

import pygame as pg
from Engine import *
# core
from core.entities.base_entity import Entity
# scene
from core.entities.player import Player
from core.entities.weapons import AssaultRifle, ShotGun, ScarL, Knife, DebigGun, Python
from numba import njit
import numpy as np


class TestScene:
    def __init__(self):
        self.entity_list: dict[id, Entity] = dict()
        self.distance = App.window.data.width*1.5
        self.free_cam = False
        
        self.entity_list['player1'] = Player(_id='player1', pos=vec3(App.window.screen.get_size()//2, 0))
        self.entity_list['assault_rifle'] = AssaultRifle(_id='assault_rifle', pos=(850, 10, 0), dropped=True)
        self.entity_list['shotgun'] = ShotGun(_id='shotgun', pos=(900, 20, 0), dropped=True)
        self.entity_list['scar_l'] = ScarL(_id='scar_l', pos=(950, 30, 0), dropped=True)
        self.entity_list['knife'] = Knife(_id='knife', pos=(1000, 40, 0), dropped=True)
        self.entity_list['python'] = Python(_id='python', pos=(1050, 50, 0), dropped=True)
        
        self.entity_list['debug'] = DebigGun(_id='debug', pos=(1000, 1000, 0), dropped=False)
        
        self.floor_texture: pg.image.load = pg.transform.scale_by(
            pg.image.load(
                rf'{config.File.APPLICATION_path}\\presets\\floor2.png'
            ), 0.2
        )
        self.tex_width, self.tex_height = self.floor_texture.get_size()
    
    def delete(self, _id):
        del self.entity_list[_id]
    
    def event(self, event):
        if self.free_cam:
            App.window.camera.__event__(event)
        
        for k, e in list(self.entity_list.items()):
            e.event(event)
    
    def update(self):
        App.window.camera.__update__()
        [e.update() for e in list(self.entity_list.values())]
    
    @staticmethod
    @njit(fastmath=True, nogil=True)
    def floor_grid_counter(
            width: int, pos_x: int, cnvs_width: int,
            height: int, pos_y: int, cnvs_height: int
    ) -> np.ndarray:
        # Вычисляем количество элементов в каждом измерении
        x_count = int(np.ceil((pos_x + cnvs_width)/width)) - int(np.floor(pos_x/width))
        y_count = int(np.ceil((pos_y + cnvs_height)/height)) - int(np.floor(pos_y/height))
        
        # Создаем массивы координат x и y
        x_coords = np.arange(int(np.floor(pos_x/width)), int(np.ceil((pos_x + cnvs_width)/width)))*width
        y_coords = np.arange(int(np.floor(pos_y/height)), int(np.ceil((pos_y + cnvs_height)/height)))*height
        
        # Создаем двумерный массив координат
        coords = np.empty((x_count*y_count, 2), dtype=np.int32)
        
        # Заполняем массив координат
        for i in range(x_count):
            for j in range(y_count):
                coords[i*y_count + j] = (x_coords[i], y_coords[j])
        
        return coords
    
    def draw_floor_grid(self):
        coords: list[tuple[int]] = self.floor_grid_counter(
            self.floor_texture.get_width(), App.window.camera.pos.x, App.window.data.width,
            self.floor_texture.get_height(), App.window.camera.pos.y, App.window.data.height
        )
        
        for coord in coords:
            App.window.screen.blit(self.floor_texture, vec2(coord) - App.window.camera.pos.xy)
    
    def render(self):
        """ render scene """
        
        """ RENER FIELD """
        self.draw_floor_grid()
        if not config.MainData.IS_RELEASE:
            pg.draw.circle(
                surface=App.window.screen._win,
                color='cyan',
                center=App.window.screen.get_size()//2,
                radius=self.distance,
                width=3,
            )
        
        """ ENTITIES """
        for k, entity in list(self.entity_list.items()):
            position = entity.pos.xy - App.window.camera.pos.xy
            
            if length(position - App.window.screen.get_size()//2) <= self.distance:
                entity.render()
                if not config.MainData.IS_RELEASE:
                    pg.draw.line(
                        surface=App.window.screen._win,
                        color='Yellow',
                        start_pos=App.window.screen.get_size()//2,
                        end_pos=position
                    )
            else:
                entity.not_render = True
        
        if App.window.camera.pos.xy%625 == vec2(0, 0):
            App.window.screen.blit(
                self.floor_texture,
                (0, 0)
            )
        
        if not config.MainData.IS_RELEASE:
            """ WIN RECT """
            pg.draw.rect(
                surface=App.window.screen._win,
                color='red',
                rect=(
                    *-App.window.camera.pos.xy,
                    *App.window.screen.get_size()
                ),
                width=3
            )

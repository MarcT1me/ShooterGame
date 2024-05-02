import pygame as pg
from Engine import *
# core
from core.entities.base_entity import Entity
# scene
from core.entities.player import Player
from core.entities.weapons import AssaultRifle, ShotGun, ScarL


class TestScene:
    def __init__(self):
        self.entity_list: dict[id, Entity] = dict()
        self.distance = App.window.data.width*1.5
        self.free_cam = False
        
        self.entity_list['player1'] = Player(_id='player1', pos=vec3(App.window.screen.get_size()//2, 0))
        self.entity_list['assault_rifle'] = AssaultRifle(_id='assault_rifle')
        self.entity_list['shotgun'] = ShotGun(_id='shotgun')
        self.entity_list['scar_l'] = ScarL(_id='scar_l')
    
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
    
    def render(self):
        """ render scene """
        
        """ RENER FIELD """
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
            
            """ SPEED METR """
            speed_metr_pos = App.window.screen.get_size() - (100, 100)
            pg.draw.circle(
                surface=App.window.screen._win,
                color=(75, 225, 15),
                center=speed_metr_pos,
                radius=78,
                width=3
            )
            pg.draw.line(
                surface=App.window.screen._win,
                color=(50, 100, 200),
                start_pos=speed_metr_pos,
                end_pos=speed_metr_pos + App.window.camera.vel.xy*75,
                width=3
            )
            ang = radians(-self.entity_list['player1'].rot.z)
            pg.draw.line(
                surface=App.window.screen._win,
                color=(100, 50, 75),
                start_pos=speed_metr_pos,
                end_pos=speed_metr_pos + vec2(cos(ang), sin(ang))*75,
                width=3
            )
            pg.draw.rect(
                surface=App.window.screen._win,
                color=(50, 50, 10),
                rect=(
                    *speed_metr_pos - (78, 78),
                    *(78*2, 78*2)
                ),
                width=3
            )

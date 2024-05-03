import pygame as pg
from Engine import *
# core
from core.entities.base_entity import Entity
# scene
from core.entities.player import Player
from core.entities.weapons import AssaultRifle, ShotGun, ScarL, Knife, DebigGun


class TestScene:
    def __init__(self):
        self.entity_list: dict[id, Entity] = dict()
        self.distance = App.window.data.width*1.5
        self.free_cam = False
        
        self.entity_list['player1'] = Player(_id='player1', pos=vec3(App.window.screen.get_size()//2, 0))
        self.entity_list['assault_rifle'] = AssaultRifle(_id='assault_rifle')
        self.entity_list['shotgun'] = ShotGun(_id='shotgun')
        self.entity_list['scar_l'] = ScarL(_id='scar_l')
        self.entity_list['knife'] = Knife(_id='knife')
        self.entity_list['debug'] = DebigGun(_id='debug')
        
        self.floor_texture: pg.image.load = pg.transform.scale_by(
            pg.image.load(
                rf'{config.File.APPLICATION_path}\\presets\\floor2.png'
            ), 0.5
        ).convert_alpha()
        self.floor_texture.set_alpha(125)  if not config.MainData.IS_RELEASE else Ellipsis
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
    
    def draw_floor_grid(self):
        c = 0
        # Отображаем текстуру на каждой позиции по оси x
        for x in range(
                int(self.tex_width*(App.window.camera.pos.x//self.tex_width)),
                int(
                    self.tex_width*((App.window.camera.pos.x + App.window.data.width)//self.tex_width) + self.tex_width
                ),
                self.tex_width
        ):
            for y in range(
                    int(self.tex_height*(App.window.camera.pos.y//self.tex_height)),
                    int(
                        self.tex_height*((App.window.camera.pos.y + App.window.data.height)//self.tex_height) +
                        self.tex_height
                    ),
                    self.tex_height
            ):
                App.window.screen.blit(self.floor_texture, vec2(x, y) - App.window.camera.pos.xy)
                c += 1
        if App.clock.timer('some_test_1241412', 0.5):
            print(c)
    
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
                    # pg.draw.line(
                    #     surface=App.window.screen._win,
                    #     color='Yellow',
                    #     start_pos=App.window.screen.get_size()//2,
                    #     end_pos=position
                    # )
                    ...
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

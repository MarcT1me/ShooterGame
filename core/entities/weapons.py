import pygame as pg
from Engine import *
# core
from core.entities.base_entity import Entity
from core.entities.Bullet import Bullet
from random import choice as random_choice
from random import random
from math import inf


class BaseGun(Entity):
    # bullet data
    bullet_speed = 7
    damage = 0
    magazine_size = 0
    ammo_size = 0
    cooldown = 0
    max_distance = inf
    max_time = inf
    bullet_size = 20
    # recoil
    recoil_force = 0
    recoil_multiple = lambda self: (random() - 0.5)*self.recoil_force
    
    # sounds
    pg.mixer.init()
    # gunshot sound effects, default - error sound
    gunshot_sounds = [pg.mixer.Sound(f'{config.File.APPLICATION_path}\\presets\\error.ogg')]
    # gun reload sounds
    reload_sounds = dict()
    for effect in {
        # magazine
        'magazine-drop', 'magazine-insert',
        # marx-man rifles
        'shutter-1', 'shutter-2',
        # loot
        'take-gun', 'take-ammo',
        # other
        'fuse-switch', 'no_ammo',
    }:
        reload_sounds[effect] = pg.mixer.Sound(f'{config.File.APPLICATION_path}\\presets\\{effect}.ogg')
    
    # other
    __increment_generator__ = increment_creator()
    increment = lambda _: next(BaseGun.__increment_generator__)
    
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # texture
        self.texture = pg.transform.scale_by(
            pg.image.load(f'{config.File.APPLICATION_path}\\presets\\{name}\\{name}.png'), 1
        )
        self.gap_v2 = vec2(0, 0)
        # fire
        self.fire = False
        self.inventory = {
            'magazine': 0,
            'shutter':  -1,
        }
    
    def create_bullet(self, _pos, _rot):
        # calculate data
        _id = f"bulltet_{self.increment()}"
        # add bullet
        App.scene.entity_list[_id] = Bullet(
            _id=_id,
            pos=_pos + vec3(
                cos(-radians(_rot.z))*10,
                sin(-radians(_rot.z))*10,
                0
            ),
            rotation=_rot,
            speed=self.bullet_speed,
            damage=self.damage,
            # experimental
            max_distance=self.max_distance,
            max_time=self.max_time,
            size=self.bullet_size
        )
    
    def reload_shutter(self):
        if self.inventory['magazine'] > 0:
            self.inventory['magazine'] -= 1
            self.inventory['shutter'] += (self.inventory['shutter'] < 1)
        elif self.inventory['shutter']:
            self.inventory['shutter'] -= 1
    
    def reload_magazine(self, inventory: dict) -> int:
        inv_ammo = inventory[self.ammo_size]
        used_ammo = int(min(max(inv_ammo, 0), self.magazine_size))
        # reload in magazine
        self.inventory['magazine'] = used_ammo
        # reload in inventory
        inventory[self.ammo_size] -= used_ammo
        return used_ammo
    
    def reload(self, inventory: dict):
        self.reload_magazine(inventory)
        self.reload_shutter()
    
    def gunshot(self) -> bool:
        # magazine
        if self.inventory['shutter'] == 0:
            App.scene.entity_list['player1'].sound_channel.play(self.reload_sounds['no_ammo'])
            return False
        self.inventory['shutter'] -= 1
        # bullet
        self.create_bullet(
            _pos=App.scene.entity_list['player1'].pos,
            _rot=App.scene.entity_list['player1'].rot,
        )
        # recoil
        App.scene.entity_list['player1'].rot.z += self.recoil_multiple()/10
        App.scene.entity_list['player1'].texture_changed = True
        
        recoil_vector = pg.mouse.get_pos() + vec2(
            self.recoil_multiple(),
            self.recoil_multiple()
        )
        
        recoil_vector.x = max(min(recoil_vector.x, App.window.data.width - 1), 1)
        recoil_vector.y = max(min(recoil_vector.y, App.window.data.height - 1), 1)
        pg.mouse.set_pos(recoil_vector)
        # play sound
        App.scene.entity_list['player1'].sound_channel.play(random_choice(self.gunshot_sounds))
        return True
    
    def update_weapon(self): pass
    
    def render_weapon(self, surf):
        # blit weapon on player-surf
        surf.blit(
            self.texture,
            self.gap_v2
        )
    
    
class DebigGun(BaseGun):
    gunshot_sounds = [
        pg.mixer.Sound(f'{config.File.APPLICATION_path}\\presets\\shotgun\\{i}.ogg') for i in {
            'shotgun-gunshot-1', 'shotgun-gunshot-2', 'shotgun-gunshot-3', 'shotgun-gunshot-4'
        }
    ]
    bullet_speed = 5
    recoil_force = 0
    damage = 100
    ammo_size = 0
    magazine_size = -1
    cooldown = 0.035
    max_distance = inf
    bullet_size = 10
    
    def __init__(self, *args, **kwargs):
        super().__init__(name='assault_rifle', *args, **kwargs)
        self.gap_v2 = vec2(30, 26)
        self.inventory['shutter'] = -1
    
    def update_weapon(self):
        super().update()
        
        if self.fire:
            if App.clock.timer('assault_reload', self.cooldown):
                self.gunshot()


""" MAIN """


class Knife(BaseGun):
    gunshot_sounds = [
        pg.mixer.Sound(f'{config.File.APPLICATION_path}\\presets\\knife\\{i}.ogg') for i in {
            'knife_slash1_1'
        }
    ]
    damage = 75
    cooldown = 0.2
    max_time = 0
    
    def __init__(self, *args, **kwargs):
        super().__init__(name='knife', *args, **kwargs)
        self.gap_v2 = vec2(30, 26)
        self.inventory['shutter'] = -1
    
    def reload_shutter(self): pass
    
    def reload_magazine(self, inventory: dict) -> int: pass
    
    def update_weapon(self):
        if self.fire:
            if App.clock.timer('knife', self.cooldown):
                self.gunshot()
    
    def create_bullet(self, _pos, _rot):
        super().create_bullet(
            _pos + vec3(
                cos(-radians(_rot.z))*20,
                sin(-radians(_rot.z))*20,
                0
            ),
            _rot
        )
    
    def gunshot(self) -> bool:
        # bullet
        self.create_bullet(
            _pos=App.scene.entity_list['player1'].pos,
            _rot=App.scene.entity_list['player1'].rot,
        )
        # play sound
        App.scene.entity_list['player1'].sound_channel.play(random_choice(self.gunshot_sounds))
        return True


class AssaultRifle(BaseGun):
    gunshot_sounds = [
        pg.mixer.Sound(f'{config.File.APPLICATION_path}\\presets\\assault_rifle\\{i}.ogg') for i in {
            'assault_rifle-gunshot-1', 'assault_rifle-gunshot-2', 'assault_rifle-gunshot-3', 'assault_rifle-gunshot-4'
        }
    ]
    bullet_speed = BaseGun.bullet_speed + .5
    recoil_force = 75
    damage = 15
    ammo_size = 7.62
    magazine_size = 30
    cooldown = 0.1
    max_distance = 1500
    
    def __init__(self, *args, **kwargs):
        super().__init__(name='assault_rifle', *args, **kwargs)
        self.gap_v2 = vec2(30, 26)
    
    def update_weapon(self):
        super().update()
        
        if self.fire:
            if App.clock.timer('assault_reload', self.cooldown):
                if self.gunshot():
                    self.reload_shutter()


class ShotGun(BaseGun):
    gunshot_sounds = [
        pg.mixer.Sound(f'{config.File.APPLICATION_path}\\presets\\shotgun\\{i}.ogg') for i in {
            'shotgun-gunshot-1', 'shotgun-gunshot-2', 'shotgun-gunshot-3', 'shotgun-gunshot-4'
        }
    ]
    bullet_speed = BaseGun.bullet_speed + .4
    recoil_force = 200
    damage = 9
    ammo_size = 30.0
    magazine_size = 5
    cooldown = 0.75
    max_distance = 1500
    
    def __init__(self, *args, **kwargs):
        super().__init__(name='shotgun', *args, **kwargs)
        self.gap_v2 = vec2(22, 30)
    
    def create_bullet(self, _pos, _rot):
        for i in range(8):
            super().create_bullet(
                _pos,
                _rot + vec3((random() - 0.5)*10, (random() - 0.5)*10, (random() - 0.5)*10)
            )
    
    def update_weapon(self):
        super().update()
        
        if self.fire:
            if App.clock.timer('assault_reload', self.cooldown):
                self.gunshot()
            self.fire = False


class ScarL(BaseGun):
    gunshot_sounds = [
        pg.mixer.Sound(f'{config.File.APPLICATION_path}\\presets\\scar_l\\{i}.ogg') for i in {
            'scar_l-gunshot-0'
        }
    ]
    bullet_speed = BaseGun.bullet_speed + .9
    recoil_force = 125
    damage = 80
    ammo_size = 5.56
    magazine_size = 15
    cooldown = 0.1725
    max_distance = 1500
    
    def __init__(self, *args, **kwargs):
        super().__init__(name='scar_l', *args, **kwargs)
        self.gap_v2 = vec2(22, 30)
    
    def update_weapon(self):
        super().update()
        
        if self.fire:
            if App.clock.timer('assault_reload', self.cooldown):
                if self.gunshot():
                    self.reload_shutter()
            self.fire = False

import pygame as pg
from Engine import *
# core
from core.entities.base_entity import Entity
from core.entities.weapons import BaseGun


class Player(Entity):
    def __init__(self, speed=1, *args, **kwars):
        super().__init__(*args, **kwars)
        
        """ texture """
        self.texture = pg.transform.scale_by(pg.image.load(f'{config.File.APPLICATION_path}\\presets\\player.png'), 1)
        self.frame_texture = self.texture  # current frame texture
        
        self.surf = pg.Surface(vec2(self.texture.get_size()) + (20, 20), flags=SRCALPHA)
        """ orientation in space """
        self.run_multiple = 1
        self.vel: vec3 = vec3(0)
        self.speed: float = speed
        
        self.texture_changed = True
        self.mouse_pos = vec2(0)
        
        """ weapon """
        self.selected_weapon: int = 1
        self.inventory = {
            'weapons': [
                'knife',
                'assault_rifle',
                'scar_l',
                'shotgun',
                'debug',
            ],
            'ammo':    {
                7.62: 250,
                30.0: 70,
                5.56: 120,
                0:    -1
            },
        }
        
        """ sound """
        self.sound_channel = pg.mixer.Channel(0)
    
    @property
    def active_weapon(self) -> BaseGun:
        return App.scene.entity_list[self.inventory['weapons'][self.selected_weapon]]
    
    @property
    def collision(self) -> pg.Rect:
        return pg.Rect(
            *(self.pos.xy - (25, 25) + vec2(
                -cos(radians(self.rot.z)), sin(radians(self.rot.z))
            )*25 - vec2(
                sin(radians(self.rot.z)), cos(radians(self.rot.z))
            )*15),
            *(50, 50)
        )
    
    def event(self, event):
        """ events """
        if event.type == MOUSEMOTION:
            """ mouse scope """
            self.mouse_pos = vec2(event.pos)
            dy = self.mouse_pos.y - (self.pos.y - App.window.camera.pos.y)
            dx = self.mouse_pos.x - (self.pos.x - App.window.camera.pos.x)
            self.rot.z = degrees(-atan2(dy, dx))
            self.texture_changed = True
        
        # MOUSE - FIRE
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active_weapon.fire = True
            elif event.button == 7:
                self.active_weapon.reload_shutter()
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.active_weapon.fire = False
        
        # JOY - FIRE
        elif event.type == JOYAXISMOTION:
            if event.axis == 5:
                bool_tr = (event.value + 1)//2
                if bool_tr >= 0:
                    self.active_weapon.fire = True
                elif bool_tr < 0:
                    self.active_weapon.fire = False
        
        # JUY - CHANGE SLOT
        elif event.type == JOYHATMOTION:
            if self.selected_weapon == 1 and event.value[0] < 0:
                self.selected_weapon = 3
            elif self.selected_weapon == 4 and event.value[0] > 0:
                self.selected_weapon = 1
            else:
                self.selected_weapon += event.value[0]
            self.texture_changed = True
        
        # KEY - CHANGE SLOT
        if event.type == KEYDOWN:
            if event.key == K_1:
                self.active_weapon.fire = False
                self.selected_weapon = 1
                self.texture_changed = True
            elif event.key == K_2:
                self.active_weapon.fire = False
                self.selected_weapon = 2
                self.texture_changed = True
            elif event.key == K_3:
                self.active_weapon.fire = False
                self.selected_weapon = 3
                self.texture_changed = True
            elif event.key == K_0:
                self.active_weapon.fire = False
                self.selected_weapon = 0
                self.texture_changed = True
            
            # KEY - RELOAD
            elif event.key == K_r:
                self.active_weapon.reload_magazine(self.inventory['ammo'])
            elif event.key == K_RETURN:
                self.active_weapon.reload_shutter()
            # KEY - DROP WEAPON
            elif event.key == K_q:
                self.selected_weapon = 0
        
        elif event.type == KEYUP:
            pass
    
    def update(self):
        """ update player data """
        self.vel = vec3(0)
        
        """ handle lists """
        key_ues = False  # walk
        if App.key_list[K_w]:
            self.vel.y -= 1
            key_ues = True
        if App.key_list[K_s]:
            self.vel.y += 1
            key_ues = True
        if App.key_list[K_a]:
            self.vel.x -= 1
            key_ues = True
        if App.key_list[K_d]:
            self.vel.x += 1
            key_ues = True
        
        """ update vectors """
        n_vec = normalize(self.vel)  # key vel
        self.vel = vec3(0) if isnan(n_vec)[0] else n_vec
        
        if not key_ues:
            for key, joystick in App.joysticks.items():
                # vel
                self.vel.x += joystick.get_axis(0)
                self.vel.y += joystick.get_axis(1)
                # scope
                axis_2 = joystick.get_axis(2)/2
                self.rot.z -= axis_2 * App.clock.delta
                if axis_2 != 0:
                    self.texture_changed = True
        
        self.pos += self.vel*self.speed*self.run_multiple*App.clock.delta
        App.window.camera.pos = self.pos - vec3(App.window.screen.get_size()//2, 0)
        App.window.camera.vel = self.vel
        
        """ weapon """
        self.active_weapon.update_weapon()
    
    def render(self):
        self.surf.fill((0, 0, 0, 0))
        
        """ player texture """
        self.surf.blit(
            self.texture,
            (0, 0)
        )
        
        """ weapon """
        self.active_weapon.render_weapon(self.surf)
        
        """ handle main surf """
        if self.texture_changed:  # create frame changed texture
            self.frame_texture = pg.transform.rotozoom(self.surf, self.rot.z, 1)
            self.texture_changed = False
        
        App.window.screen.blit(
            self.frame_texture,
            vec2(App.window.screen.get_size() - self.frame_texture.get_size())//2
        )
        
        if not config.MainData.IS_RELEASE:
            # pg.draw.rect(
            #     surface=App.window.screen._win,
            #     color='red',
            #     rect=(
            #         *(App.window.screen.get_size()//2 - vec2(self.frame_texture.get_size())//2),
            #         *(self.frame_texture.get_size())
            #     ),
            #     width=3
            # )
            collision = self.collision
            collision.center -= App.window.camera.pos.xy
            pg.draw.rect(
                surface=App.window.screen._win,
                color='red',
                rect=collision,
                width=3
            )
            pg.draw.line(
                surface=App.window.screen._win,
                color='cyan',
                start_pos=App.window.screen.get_size()//2,
                end_pos=vec2(
                    cos(-radians(self.rot.z)),
                    sin(-radians(self.rot.z))
                )*App.scene.distance + App.window.screen.get_size()//2,
                width=3
            )

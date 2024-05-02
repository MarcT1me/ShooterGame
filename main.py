import pygame
from Engine.app import mainloop
# Engine
from Engine import *

# core
from core.message_screens import Loading
from core.scene import TestScene
from core.entities.decore import Barrel
from core.entities.player import Player


class ShooterGame(App):
    def __pre_init__(self, *args, **kwargs):
        super().__pre_init__()
        self.win_data = WinData(
            width=1280,
            height=720,
            vsync=config.Screen.vsync,
            flags=config.Screen.flags,
        )
        App.window.data = self.win_data
    
    def __init__(self):
        super().__init__()
        # working with Engine window after Engine.init()
        self.window.set_icon(
            pygame.image.load(
                f'{config.File.APPLICATION_path}\\{config.File.APPLICATION_ICO_dir}\\{config.File.APPLICATION_ICO_name}'
            )
        )
        
        """ other variables """
        self.fps_font = pygame.font.SysFont('Arial', 30)
        self.aggregate_fps: pygame.font.SysFont = ...
        
        self.main_loading_screen = Loading()
        self.main_scene = TestScene()
        
        for i in range(24):
            self.main_scene.entity_list[f'barrel{i}'] = Barrel(_id=f'barrel{i}', pos=30*i)
        
        self.fps_font: pygame.font.SysFont = pygame.font.SysFont('Arial', 20, True)
        self.fps_font: pygame.font.SysFont = pygame.font.SysFont('Arial', 20, True)
        App.scene = self.main_scene
        App.window.set_cursor_style(pygame.cursors.diamond)
    
    def events(self) -> None:
        """ handle events """
        for event in App.event_list:
            # quit from app
            if event.type == QUIT:
                App.running = NO
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    App.running = NO
                    return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    App.running = NO
                # test TR raise
                elif event.key == K_g:
                    _ = 1 + '1'
                
                # other key events
                elif event.key == K_F11:
                    """ toggle fullscreen """
                    # find window into any monitor
                    index, monitor = self.window.get_display_index()
                    # calculate flags and sizes
                    if not self.window.is_full():
                        width = monitor.width
                        height = monitor.height
                        flags = config.Screen.flags | FULLSCREEN
                    else:
                        width = self.win_data.width
                        height = self.win_data.height
                        index = EMPTY  # if not full change monitor on NONE
                        flags = config.Screen.flags
                    
                    # setting changes
                    self.window.data = self.window.data.extern(
                        {
                            'width':   width,
                            'height':  height,
                            'monitor': index,
                            'flags':   flags
                        }
                    )
                    self.window.resset()
                
                elif event.key == K_TAB:
                    """ show monitor """
                    logger.info(graphic.get_current_desktop_size())
            
            elif event.type == VIDEORESIZE:
                """ resize window """
                self.window.data = self.window.data.extern(
                    {
                        'width':  event.size[0],
                        'height': event.size[1],
                    }
                )
                self.window.resset()
            elif event.type == WINDOWDISPLAYCHANGED:
                logger.debug(f'Window now on {event.display_index} display')
            
            # Handle hotplugging
            elif event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                App.joysticks[joy.get_instance_id()] = joy
                logger.info('joystick connect', joy.get_instance_id())
            elif event.type == pygame.JOYDEVICEREMOVED:
                logger.info('joystick disconnect', event.instance_id)
                del App.joysticks[event.instance_id]
            
            App.scene.event(event)
    
    def update(self) -> None:
        """ Update application """
        self.aggregate_fps = round(min(self.clock.get_fps(), 99999))
        App.scene.update()
    
    def render(self) -> None:
        """ render app surfaces """
        App.scene.render()
        
        fin_fps_font = self.fps_font.render(
            f'fps: {self.aggregate_fps}      delta: {self.clock.delta*0.001}',
            True,
            'cyan'
        )
        App.window.screen.blit(
            fin_fps_font,
            (0, App.window.data.height - fin_fps_font.get_height())
        )
        
        player: Player = App.scene.entity_list["player1"]
        weapon_id: str = player.inventory['weapons'][player.selected_weapon]
        weapon_inventory: dict = App.scene.entity_list[weapon_id].inventory
        fin_scene_font = self.fps_font.render(
            f'SCENE len: {len(App.scene.entity_list)}       '
            f'PLAYER weapon  '
            f'name: {weapon_id}       '
            f'magazine: {weapon_inventory["magazine"]}  '
            f'shutter {weapon_inventory["shutter"]}       '
            f'ammo {player.inventory["ammo"][App.scene.entity_list[weapon_id].ammo_size]}',
            True,
            'white'
        )
        App.window.screen.blit(
            fin_scene_font,
            (0, 0)
        )


if __name__ == '__main__':
    mainloop(ShooterGame)

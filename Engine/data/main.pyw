import pygame
# Engine
from Engine.app import mainloop
from Engine import *


class QuantumGame(App):
    def __pre_init__(self, *args, **kwargs):
        """ app pre- initialisation """
        # read and rewrite configs
        super().__pre_init__()
        config.File.reed_data()
        config.File.set_default_data()
        
        # setting Engine data
        self.window.data = WinData(
            width=config.Screen.size[0],
            height=config.Screen.size[1],
            vsync=config.Screen.vsync,
            flags=config.Screen.flags,
            monitor=config.Screen.monitor,
            title=f'{config.MainData.APPLICATION_name}  v {config.MainData.APPLICATION_version}'
        )
    
    def __init__(self):
        """ app initialisation """
        super().__init__()
        
        self.fps_font = pygame.font.SysFont('Arial', 30)
        self.aggregate_fps: pygame.font.SysFont = ...
    
    def __post_init__(self, *args, **kwargs):
        """ some post-init """
        logger.debug([str(i) for i in (NULL, EMPTY, BINARY)])
        
        # event
        self.test_event = pygame.event.Event(pygame.USEREVENT + 1)
        
        # wait him 5 sec
        self.clock.expect(self.test_event, 5)
        
        # print name
        logger.debug(f'create test wait event with name {self.test_event.name}')
    
    def handle_event(self) -> None:
        """ App events """
        for event in App.event_list:
            # quit from app
            if event.type == QUIT:
                App.running = NO
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    App.running = NO
                    return
                # test TR raise
                elif event.key == K_g and App.key_list[K_LCTRL]:
                    _ = 1 + '1'
                    return
                # test TR raise
                elif event.key == K_r and App.key_list[K_LCTRL]:
                    config.File.reed_data()
                    
                    self.window.data = WinData(
                        width=config.Screen.size[0],
                        height=config.Screen.size[1],
                        vsync=config.Screen.vsync,
                        flags=config.Screen.flags,
                        monitor=config.Screen.monitor,
                        title=f'{config.MainData.APPLICATION_name}  v {config.MainData.APPLICATION_version}'
                    )
                
                # other key events
                elif event.key == K_F11 and App.key_list[K_LCTRL]:
                    """ toggle fullscreen """
                    config.Screen.full = not config.Screen.full
                    self.window.set_desktop_full(config.Screen.full)
                
                elif event.key == K_F10 and App.key_list[K_LCTRL]:
                    """ toggle fullscreen """
                    config.Screen.full = not config.Screen.full
                    self.window.toggle_full(config.Screen.full)
                
                elif event.key == K_TAB:
                    """ show monitor """
                    logger.info(graphic.get_current_desktop_size())
            
            elif event.type == VIDEORESIZE:
                """ resize window """
                self.window.data = self.window.data.extern(
                    {
                        'width': event.size[0],
                        'height': event.size[1],
                    }
                )
                self.window.resset()
            elif event.type == WINDOWDISPLAYCHANGED:
                logger.debug(f'Window now on {event.display_index} display')
            
            # Handle hot-plugging
            elif event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                App.joysticks[joy.get_instance_id()] = joy
                logger.info('joystick connect', joy.get_instance_id())
            elif event.type == pygame.JOYDEVICEREMOVED:
                logger.info('joystick disconnect', event.instance_id)
                del App.joysticks[event.instance_id]
            
            # custom
            elif event.type == self.test_event.type:
                if self.clock.timer('safe_console', INF):
                    logger.warning(
                        f'TestEvent waited \t delay in processing = {(event.end - event.start) - event.delay}'
                    )
    
    def update(self) -> None:
        """ Update application """
        self.aggregate_fps = round(min(self.clock.get_fps(), 99999))
    
    def render(self) -> None:
        """ render app surfaces """
        # without filling and flipping
        
        fin_fps_font = self.fps_font.render(
            f'fps: {self.aggregate_fps}      delta: {self.clock.delta * 0.001}',
            True,
            'cyan'
        )  # create frame
        App.window.screen.blit(
            fin_fps_font,
            (0, App.window.data.height - fin_fps_font.get_height())
        )  # blit


if __name__ == '__main__':
    mainloop(QuantumGame)

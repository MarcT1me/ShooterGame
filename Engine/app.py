""" Collection of utilities for working with the application class.
"""
from loguru import logger
import pygame
# default
from abc import abstractmethod
from typing import Optional

# Engine import
import Engine
from Engine import timing
from Engine.graphic import err_screen
from Engine.graphic import Graphics


class App:
    """
    Main App class.
    The main parent class for creating logic and running it in the main loop
    
    FEATURES
        it does not have an initializer to simplify inheritance and management
    
    METHODS
        1) events: Event method. Needs to be overwritten after inheritance:
        2) update_app: Updating program data. Needs to be overwritten after inheritance:
        3) update_window: Rendering of the program window. Needs to be overwritten after inheritance
        4) run: the main cycle of the program
        
    CLASS FIELD
        running (bool): a variable is a condition for the operation of the main loop
    """
    running: bool = True
    exception = False  # type: Exception | False
    failures: list[Exception | Warning] = []
    
    window = Graphics
    clock: Optional[timing.clock] = None
    
    event_list: Optional[list[pygame.event.EventType]] = None
    key_list: Optional[list[pygame.event.EventType]] = None
    
    joysticks: Optional[dict[int, pygame.joystick.JoystickType]] = {}
    
    scene = None
    
    def __new__(cls, *args, **kwargs):
        """ creating App class """
        obj = super().__new__(cls)
        obj.__pre_init__(*args, **kwargs)
        return obj
    
    def __pre_init__(self, *args, **kwargs):
        """ Pre-initialisation Application. Before main __init__ """
        App.failures.clear()
        
        pygame.init()
        Engine.config.File.load_engine_config('settings')
        Engine.config.File.load_engine_config('graphics')
    
    def __init__(self, *args, **kwargs):
        """ Main app initialisation.
        in method realised init pygame, load config files and clock
         use supper()
         """
        if App.window.data.flags & Engine.OPENGL:
            App.window.set_gl_attributes()
        
        # set main functions
        App.clock = timing.clock()
        App.window.set_core()
        
        if App.window.data.flags & Engine.OPENGL:
            App.window.set_modern_gl()
        
        # pre-init
        if Engine.config.MainData.PRE_INIT:
            """ Pre-initialisation """
        
        logger.success('ENGINE - INIT\n')
    
    def __post_init__(self, *args, **kwargs):
        """ Post initialisation, after main __init__ """
        ...
    
    def on_exit(self) -> None:
        """ method called after ending app.run """
        from Engine.scripts import node_window, button
        
        pygame.quit()  # release pygame
        # clear rosters
        node_window.NodeWindow.roster_relies()
        button.Button.roster_relies()
        # release moderngl
        try:
            if App.window.data.flags & Engine.OPENGL:
                App.window.context.release()
        except Exception as exc:
            logger.error(f'can`t release context, {exc.args[0]}')
        
        logger.success('ENGINE - QUIT\n\n')
    
    @staticmethod
    def failure(err) -> None:
        """ calling, if got exception in mainloop """
        App.failures.append(err)
        print('\n\n')
        logger.exception(err)
        print('\n\n')
    
    def __repr__(self): return f'<class: App; running={self.running}>'
    
    def __str__(self): return f'{"running" if self.running else "stoped"} App'
    
    @abstractmethod
    def events(self) -> None:
        """ handle all events """
        ...
    
    @abstractmethod
    def update(self) -> None:
        """ UpDate application"""
        ...
    
    @abstractmethod
    def render(self) -> None:
        """ render all app surfaces, and use engine render methods """
        ...
    
    def run(self) -> None:
        """ Run game.
        The method that starts the event loop.
        This is a while loop that uses the current variable in the App class field as a condition. 3 methods are
        called in the loop itself: events, update_app, update_window
        
        :return: Nothing
        :raises KeyboardInterrupt: if the cycle is not completed correctly.
        """
        # after main.init
        self.__post_init__()
        """ Main-loop """
        while self.running:
            # events
            App.event_list = pygame.event.get()
            App.key_list = pygame.key.get_pressed()
            self.events()
            # update
            self.update()
            # render
            App.window.screen.fill('black')
            self.render()
            App.window.interface.render()
            App.window.flip()
            # clok tick
            App.clock.tick(Engine.config.Screen.fps)


def mainloop(app):
    """
    :param app: application class with initializer
    :return: Last worked app
    :raise AssertionError: if there are problems with the argument
    """
    assert issubclass(app, App), 'Arg `app` must be inherited by `Engine.app.App`'
    
    work_app = app  # current app class
    while work_app.running:
        try:
            # run app
            work_app = app()
            work_app.run()
        except Exception as err:
            # if app get exception
            work_app.failure(err=err)
            App.running = err_screen.showWindow(err) if Engine.config.MainData.IS_RELEASE \
                else err_screen.showTraceback(err)  # show err window
        finally:
            # after all
            work_app.on_exit()
    # end main;oop
    return work_app

""" Engine Graphic core
"""
# graphics
from pygame import display, mouse, event, cursors, Surface, image
import moderngl
# window utils
from pygetwindow import getWindowsWithTitle
from screeninfo import get_monitors
# Engine
from Engine import (  # constants
    GL_CONTEXT_MAJOR_VERSION, GL_CONTEXT_MINOR_VERSION,  # k, k
    GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE,  # k: v
    OPENGL, EMPTY, FULLSCREEN,
    config,
)  # data and constants
from Engine.lscript import Optional  # typing
from Engine import logger  # logging
# __init__ imports
from Engine.scripts.app_data import WinData
from Engine.graphic.window import Window
from Engine.objects.camera import Camera
from Engine.graphic.interface import AdvancedInterface  # interface surface
from Engine.graphic.shaders import Shader  # shaders
from Engine.graphic.texture import Texture  # shaders


class Graphics:
    """ Main Engine graphic class
     """
    data: Optional[WinData] = EMPTY  # Window configs
    
    screen: Optional[Window] = EMPTY  # Window surface
    context: Optional[moderngl.Context] = EMPTY  # MGL context
    
    """ other private """
    __monitors = get_monitors()
    
    @staticmethod
    def set_gl_attributes(*, major: int = 3, minor: int = 3):
        """ set opengl attribute """
        display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, major)
        display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, minor)
        display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)
        logger.debug(f'set gl attributes, {major, minor}')
    
    @classmethod
    def set_window_core(cls):
        """ set main window variables"""
        cls.screen = Window(win_data=cls.data)
        # working with created window
        cls.set_caption(cls.data.title)
        cls.set_icon(
            image.load(
                f'{config.File.APPLICATION_path}\\{config.File.APPLICATION_ICO_dir}\\{config.File.APPLICATION_ICO_name}'
            )
        )
        cls.toggle_full(config.Screen.full)
        # creating Engine tools
        if cls.data.flags & OPENGL:
            cls.context = moderngl.create_context()
        cls.flip()
    
    @classmethod
    def set_gl_core(cls):
        """ set all mgl configs """
        cls.context.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
        cls.context.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        cls.context.viewport = (cls.data.view_x, cls.data.view_y, cls.data.size[0], cls.data.size[1])
        
        logger.info(
            f"\n\tEngine graphic - init\n"
            f"screen:\n"
            f"\tWinData = {cls.data};\n"
            f"context:\n"
            f"\tsize = {cls.context.screen.size} \tGPU = {cls.context.info['GL_RENDERER']};\n"
        )
    
    @classmethod
    def get_display_index(cls):
        # find window
        win = getWindowsWithTitle(cls.data.title)[0]
        # iter on all monitors and find current window display
        for index, monitor in enumerate(cls.__monitors):
            if monitor.x <= win.left and monitor.y <= win.top or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top or \
                    monitor.x <= win.left and monitor.y <= win.top + win.height or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top + win.height:
                return index, monitor
        else:
            return None, None
    
    @staticmethod
    def set_icon(_img):
        display.set_icon(_img)
    
    @staticmethod
    def set_caption(_caption):
        display.set_caption(_caption)
    
    @classmethod
    def toggle_full(cls, _is_full):
        """ toggle fullscreen """
        if _is_full != cls.is_full():
            # find window into any monitor
            index, monitor = cls.get_display_index()
            # calculate flags and sizes
            if not cls.is_full():
                width = monitor.width
                height = monitor.height
                flags = config.Screen.flags | FULLSCREEN
            else:
                width = config.Screen.size[0]
                height = config.Screen.size[1]
                index = EMPTY  # if not full change monitor on NONE
                flags = config.Screen.flags
            
            # setting changes
            cls.data = cls.data.extern(
                {
                    'size':   (width, height),
                    'monitor': index,
                    'flags':   flags
                }
            )
            
            cls.resset()
    
    @classmethod
    def set_desktop_full(cls, _is_full):
        """ Set full screen YES/NO  """
        if _is_full != cls.is_full():
            # calculate flags and sizes
            if not cls.is_full():
                flags = config.Screen.flags | FULLSCREEN
            else:
                flags = config.Screen.flags
            # setting changes
            cls.data = cls.data.extern(
                {
                    'flags': flags
                }
            )
            cls.resset()
            display.toggle_fullscreen()
    
    @staticmethod
    def is_full():
        return display.is_fullscreen()
    
    @staticmethod
    def set_cursor_mode(visible: bool = None, grab: bool = None) -> None:
        mouse.set_visible(visible if visible is not None else mouse.get_visible())
        event.set_grab(grab if grab is not None else event.get_grab())
    
    @staticmethod
    def set_cursor_image(_image: Surface, hotspot: tuple = (0, 0)) -> None:
        cursor = cursors.Cursor(hotspot, _image)
        mouse.set_cursor(cursor)
    
    @staticmethod
    def set_cursor_style(system: int) -> None:
        mouse.set_cursor(system)
    
    @staticmethod
    def flip():
        display.flip()
    
    @classmethod
    def resset(cls):
        cls.screen = Window(win_data=cls.data)
        if cls.data.flags & OPENGL:
            cls.context.viewport = (cls.data.view_x, cls.data.view_y, cls.data.size[0], cls.data.size[1])
        cls.interface = AdvancedInterface(cls.data)
        logger.debug(f'win.data = {cls.data}')


def event_window(_event: event.Event):
    return getattr(_event, 'window', None)


def get_desktop_sizes() -> list[tuple[int, int]]:
    return display.get_desktop_sizes()


def get_current_desktop_size() -> tuple[int, int]:
    index, _ = Graphics.get_display_index()
    return get_desktop_sizes()[index]


def get_window_size() -> tuple[int, int]:
    return display.get_window_size()

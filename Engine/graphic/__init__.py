""" Engine Graphic core
"""
from pygame import display, mouse, event, cursors, Surface
import moderngl
from loguru import logger
from pygetwindow import getWindowsWithTitle
from screeninfo import get_monitors
# default
from typing import Optional
# Engine
from Engine import (  # constants
    GL_CONTEXT_MAJOR_VERSION, GL_CONTEXT_MINOR_VERSION,  # k, k
    GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE,  # k: v
    OPENGL, EMPTY
)
# typing
from Engine.scripts.app_data import WinData
from Engine.graphic.window import Window
from Engine.graphic.interface import AdvancedInterface
from Engine.graphic.shaders import Shader
from Engine.graphic.camera import Camera


class Graphics:
    data: Optional[WinData] = EMPTY # Window configs
    
    screen: Optional[Window] = EMPTY  # Window surface
    interface: Optional[AdvancedInterface] = EMPTY  # Interface surface
    
    context: Optional[moderngl.Context] = EMPTY  # MGL context
    shader: Optional[Shader] = EMPTY  # current shader program
    camera = ...
    
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
    def set_core(cls):
        """ set main variables"""
        cls.screen = Window(win_data=cls.data)
        cls.interface = AdvancedInterface(win_data=cls.data)
        cls.camera = Camera()
        if cls.data.flags & OPENGL:
            cls.context = moderngl.create_context()
        display.set_caption(cls.data.title)
        cls.flip()
    
    @classmethod
    def set_modern_gl(cls):
        """ set all mgl configs """
        cls.context.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
        cls.context.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        cls.context.viewport = (cls.data.view_x, cls.data.view_y, cls.data.width, cls.data.height)
        # create interface surface
        cls.interface = AdvancedInterface(cls.data)
        
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
    
    @staticmethod
    def set_full(_is_full):
        """ Set full screen YES/NO  """
        if _is_full != display.is_fullscreen():
            display.toggle_fullscreen()
    
    @staticmethod
    def is_full():
        return display.is_fullscreen()
    
    @staticmethod
    def set_cursor_mode(visible: bool = None, grab: bool = None) -> None:
        mouse.set_visible(visible if visible is not None else mouse.get_visible())
        event.set_grab(grab if grab is not None else event.get_grab())
    
    @staticmethod
    def set_cursor_image(image: Surface, hotspot: tuple = (0, 0)) -> None:
        cursor = cursors.Cursor(hotspot, image)
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
            cls.context.viewport = (cls.data.view_x, cls.data.view_y, cls.data.width, cls.data.height)
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

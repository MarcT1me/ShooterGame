""" Main engine Window
"""
from pygame.display import set_mode, get_window_size
from pygame import Rect
# Engine
from Engine.scripts.app_data import WinData
from Engine.data import config
from Engine.lscript import vec2


class Window:
    def __init__(self, win_data: WinData):
        """ init main window """
        kwargs = {
            'size':  (win_data.width, win_data.height),
            'flags': win_data.flags,
            'vsync': win_data.vsync,
        }
        if win_data.monitor not in (None, config.EMPTY) and str(win_data.monitor) not in 'nullEmptyType':
            kwargs['display'] = win_data.monitor
        self._win = set_mode(**kwargs)
    
    def __repr__(self):
        return f'<IWindow: t=\'{config.Screen.title}\' s={get_window_size()}>'
    
    def fill(self, color, *, rect=None, special_flags=0):
        self._win.fill(
            color,
            rect if rect is not None else Rect(0, 0, *self._win.get_size()),
            special_flags
        )
    
    def blit(self, source, dest, *, area=None, special_flags=0):
        self._win.blit(
            source,
            dest,
            area if area is not None else Rect(0, 0, *source.get_size()),
            special_flags
        )
    
    def get_size(self):
        return vec2(self._win.get_size())

from pygame import Surface
from pygame.rect import Rect
from pygame.constants import (FULLSCREEN, RESIZABLE, NOFRAME)
import pygame._sdl2.video as sdl2_video
from screeninfo import get_monitors
from glm import vec2
# engine
from Engine.scripts.app_data import WinData
from Engine.data.config import Screen


class NodeWindow:
    roster = dict()
    
    def __init__(self, _id: str, *, win_data: WinData):
        """ init confirm window class """
        self.id = _id
        self.win_data = win_data

        self.surf: Surface = Surface(size=(win_data.width, win_data.height))  # create window surface
        """ setting window """
        self.win: sdl2_video.Window = sdl2_video.Window(
            title=Screen.title
        )

        """ other window and render variables """
        self._renderer: sdl2_video.Renderer = sdl2_video.Renderer(self.win)  # create window texture from surface
        self._rend_tex: sdl2_video.Texture = sdl2_video.Texture.from_surface(self._renderer, self.surf)

        self.set()
        NodeWindow.roster[_id] = self

    def set(self, *, win_data: WinData = None) -> __init__:
        win_data = self.win_data if win_data is None else win_data

        """ Window """
        self.win.size = (win_data.width, win_data.height)  # size
        # change position
        ox = 0
        oy = 0
        if win_data.posX is not None:
            ox += win_data.posX
            oy += win_data.posY
            self.win.position = (ox, oy)
        # change monitor
        if win_data.monitor is not None:
            monitors = get_monitors()
            monitor = monitors[win_data.monitor]
            ox = monitor.x
            oy = -monitor.y
            self.win.position = (ox, oy)
        self.toggle_fullscreen(win_data.flags & FULLSCREEN)
        # opacity
        self.win.opacity = win_data.opacity
        # mouse
        self.win.relative_mouse = win_data.relative_mouse
        # resizable
        self.win.resizable = win_data.flags & RESIZABLE
        # borders
        self.win.borderless = win_data.flags & NOFRAME
        """ renderer """
        # viewport
        self._renderer.set_viewport(
            (win_data.view_x, win_data.view_y, win_data.width, win_data.height)
        )
        # main window return
        return self

    def toggle_fullscreen(self, is_full):
        self.win.set_fullscreen(desktop=True) if is_full else self.win.set_windowed()

    def move(self, offset: vec2 | tuple):
        self.win.position += vec2(offset)

    def set_visibility(self, visibility: bool):
        self.win.show() if visibility else self.win.hide()

    @property
    def get_surf(self):
        return self._renderer.to_surface()

    @property
    def get_rect(self):
        return self._rend_tex.get_rect()

    def flip(self) -> None:
        self.__update_tex()
        self.__render()

    def __update_tex(self) -> None:
        self._rend_tex.update(self.surf)

    def __render(self) -> None:
        self._renderer.clear()
        rect = Rect(0, 0, self.win_data.width, self.win_data.height)
        self._renderer.blit(
            self._rend_tex, rect, rect, Screen.blit_flags
        )
        self._renderer.present()

    def release(self) -> None:
        self.win.destroy()
        NodeWindow.roster.pop(self.id)

    @staticmethod
    def roster_render():
        for win in NodeWindow.roster.values():
            win.flip()

    @staticmethod
    def roster_relies():
        for win in list(NodeWindow.roster.values()):
            win.release()

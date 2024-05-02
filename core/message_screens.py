from Engine.app import App
from pygame import image, font, draw, transform
from Engine import config


class Loading:
    def __init__(self, p: int = 0):
        self.p = p
        self.background_image = transform.scale(
            image.load(
                f'{config.File.APPLICATION_path}\\presets\\loading_image.jpg'
            ),
            App.window.screen.get_size()
        )
        self.loading_fin_font = font.SysFont('Arial', 100).render('Loading', True, (100, 100, 100))
        self.load_bar_rect = [
            0,  # x
            App.window.data.height - 10,  # y - в нижней части экрана
            0,  # width (progress)
            10  # height
        ]
        self.render()
    
    def jump_to(self, value):
        self.p = value
        self.load_bar_rect[2] = self.p/100*App.window.data.width
        self.render()
    
    def render(self):
        App.window.screen.blit(
            self.background_image,
            (0, 0)
        )
        App.window.screen.blit(
            self.loading_fin_font,
            (20, App.window.data.height//5 - self.loading_fin_font.get_height()//2)
        )
        
        draw.rect(App.window.screen._win, (100, 100, 100), self.load_bar_rect)
        App.window.flip()

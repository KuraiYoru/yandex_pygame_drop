import pygame_menu
from settings import *
from PIL import ImageFont
from pygame_menu import sound

# ---------- создание меню с помощью библиотеки pygame-menu оно уже готово забей
class Menu:
    def __init__(self, func, screen, value):
        font = 'fonts/font.ttf'
        title = 'Great Abyss'
        title_font = 'fonts/for_title.ttf'
        font1 = ImageFont.truetype(title_font, 100)
        size = font1.getsize(title)
        mytheme = pygame_menu.Theme(
            widget_font=font,
            title_background_color=(4, 47, 126),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
            title_offset=((WIDTH / 2 - size[0] / 2 + 20, 100)),
            title_font=title_font,
            title_font_size=100,
            title_font_shadow=True,
            title_font_shadow_color=(40, 40, 40),
            title_font_shadow_offset=10,

        )

        about_theme = pygame_menu.themes.THEME_DARK.copy()
        about_theme.widget_font = pygame_menu.font.FONT_NEVIS
        about_theme.title_font = pygame_menu.font.FONT_8BIT
        about_theme.title_offset = (5, -2)
        about_theme.widget_offset = (0, 0.14)

        myimage = pygame_menu.baseimage.BaseImage(
            image_path='sprites/213.jpg',
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL

        )
        about_menu = pygame_menu.Menu(
            center_content=False,
            height=400,
            mouse_visible=True,
            theme=about_theme,
            title='About',
            width=600,
        )
        about_menu.add.label(f"Creator: KuraiYoru", margin=(0, 20))
        about_menu.add.button('Return to Menu', pygame_menu.events.BACK, margin=(0, 150))
        about_menu.add.label(f"Music from https://opengameart.org/")

        mytheme.background_color = myimage
        menu = pygame_menu.Menu(title, WIDTH, HEIGHT, theme=mytheme)
        self.engine = sound.Sound()

        self.engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, 'music/song18.mp3')
        menu.set_sound(self.engine, recursive=True)

        menu.add.label(value, font_color=(255, 255, 255)).set_margin(0, 20)
        menu.add.button('Play', func).set_margin(0, 20).resize(150, 75, False)
        menu.add.button(about_menu.get_title(), about_menu).resize(150, 75, False).set_margin(0, 20)
        menu.add.button('Quit', pygame_menu.events.EXIT).resize(150, 75, False)
        menu.mainloop(screen)

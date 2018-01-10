"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg

from . import tools

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
ORIGINAL_CAPTION = "Badius"


#Initialization
pg.mixer.pre_init(44100,-16,2, 1024)
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

if pg.joystick.get_count() > 0:
    joystick = pg.joystick.Joystick(0)
    joystick.init()
    print("{} initialised".format(joystick.get_name()))
else:
    joystick = False

#
FRICTION = -0.18

#Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
MOV   = tools.load_all_movies(os.path.join("resources", "movies"))

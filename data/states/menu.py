"""
This module contains our intro state with the movie.
"""

import pygame as pg

from .. import setup, tools


class Menu(tools._State):
    """Scene that plays our intro movie."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "GAME"
        self.font = pg.font.Font(setup.FONTS["Fixedsys500c"], 50)
        self.title = self.render_font(self.font, "Intro Screen",
                                      pg.Color("white"),
                                      (setup.SCREEN_RECT.centerx, 30))
        self.ne_key = self.render_font(self.font, "Press Any Key",
                                       pg.Color("yellow"),
                                       (setup.SCREEN_RECT.centerx, 550))
        self.blink = False
        self.timer = 0.0

    def startup(self, current_time, persistant):
        return tools._State.startup(self, current_time, persistant)

    def cleanup(self):
        return tools._State.cleanup(self)

    def get_event(self, event):
        """End intro scene on any key press."""
        if event.type == pg.KEYDOWN:
            self.done = True

    def draw(self, surface):
        """Blit all items to the surface including the movie."""
        surface.fill(pg.Color("darkslateblue"))
        surface.blit(*self.title)
        if self.blink:
            surface.blit(*self.ne_key)

    def update(self, surface, keys, current_time, time_delta):
        """Update blink; end scene if intro movie is done; draw everything."""
        self.current_time = current_time
        if self.current_time-self.timer > 1000.0/5.0:
            self.blink = not self.blink
            self.timer = self.current_time
        self.draw(surface)


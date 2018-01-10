
import random
import pygame as pg
from .. import tools, setup

vec2 = pg.math.Vector2
vec3 = pg.math.Vector3

random.seed()

class Starfield(pg.sprite.Group):
    def __init__(self, surface):
        pg.sprite.Group.__init__(self)
        self.surface = surface
        self.max_stars = 100
        while len(self.sprites()) < self.max_stars:
            self.add(Star(self, True))

    def update(self, *args):
        for star in self.sprites():
            star.update()
            if star.pos.x < -10:
                star.kill()

        while len(self.sprites()) < self.max_stars:
            self.add(Star(self))


class Star(pg.sprite.Sprite):
    def __init__(self, starfield, first=False):
        pg.sprite.Sprite.__init__(self)
        diceroll = random.randrange(0, 100)
        if diceroll < 75:
            self.depth = 0
        elif diceroll < 95:
            self.depth = 1
        else:
            self.depth = 2
        # self.depth = random.randrange(0, 3)
        self.vx = 5 ** self.depth
        self.pos = self.new_pos(first)
        self.image = pg.Surface((2 ** self.depth, 2 ** self.depth))
        self.image.fill(pg.Color('white'))
        self.rect = self.image.get_rect()

    def new_pos(self, first=False):
        offset = 0
        if not first:
            offset = setup.SCREEN_SIZE[0]

        return pg.math.Vector2(offset + random.randrange(10, setup.SCREEN_SIZE[0]),
                   random.randrange(0, setup.SCREEN_SIZE[1]))

    def update(self, *args):
        self.pos.x -= self.vx
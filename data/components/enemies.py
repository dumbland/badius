import pygame as pg

from .. import tools, setup

class Enemy(pg.sprite.Sprite):
    def __init__(self, spawner):
        super().__init__()
        self.spawner = spawner
        self.pos = pg.math.Vector2(setup.SCREEN_SIZE[0], 0)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.death_sound = None
        self.index = 0

    def update(self, *args):
        super().update(*args)
        if self.rect.right < 0:
            self.kill()

    def kill(self, murdered=False):
        if murdered:
            self.spawner.add_explosion(self)
        super().kill()

class Grunt(Enemy):
    def __init__(self, spawner):
        super().__init__(spawner)
        self.image = setup.GFX['grunt']
        self.image.set_colorkey(pg.Color('magenta'))
        self.rect = self.image.get_rect()
        self.vel = pg.math.Vector2(-2, 0)
        self.death_sound = setup.SFX['explosion']

class Squiggy(Enemy):
    def __init__(self, spawner):
        super().__init__(spawner)
        self.rotate = 0
        # self.image = setup.GFX['sine']
        self.image.set_colorkey(pg.Color('magenta'))
        self.rect = self.image.get_rect()
        self.vel = pg.math.Vector2(-2, 0)
        self.death_sound = setup.SFX['explosion']


    @property
    def image(self):
        if self.rotate == 0:
            return setup.GFX['sine']
        else:
            rot_image = pg.transform.rotate(setup.GFX['sine'], self.rotate)
            self.rect = rot_image.get_rect(center=self.rect.center)
            return rot_image

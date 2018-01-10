

import pygame as pg
from .. import tools, setup
from . import weapons
# from .projectiles import Bullet

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(setup.SCREEN_SIZE[0]/2, setup.SCREEN_SIZE[1]/2)
        self.acc = pg.math.Vector2(0, 0)

        self.sheet = setup.GFX['strip-ship']
        self.sprites = tools.strip_from_sheet(self.sheet,
                                              (0, 0),
                                              (128, 64), 7)
        self.image.set_colorkey(pg.Color('magenta'))
        self.rect = self.image.get_rect()
        self.rect.center = (setup.SCREEN_SIZE[0]/2, setup.SCREEN_SIZE[1]/2)
        self.thrust = 1

        self.loadout = [weapons.Chaingun(self)]
        self.firing = False

    @property
    def image(self):
        if self.vel.y < -2:
            return self.sprites[2]
        elif self.vel.y > 2:
            return self.sprites[1]
        else:
            return self.sprites[0]


    def engage(self):
        for weapon in self.loadout:
            weapon.engage()

    def disengage(self):
        for weapon in self.loadout:
            weapon.disengage()


    def update(self):
        for weapon in self.loadout:
            weapon.update()

        self.acc = pg.math.Vector2(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.acc.x = -self.thrust
        if keys[pg.K_d]:
            self.acc.x = self.thrust
        if keys[pg.K_w]:
            self.acc.y = -self.thrust
        if keys[pg.K_s]:
            self.acc.y = self.thrust
        if keys[pg.K_SPACE]:
            # self.engage()
            self.firing = True
        if not keys[pg.K_SPACE] and self.firing:
            # self.disengage()
            self.firing = False


        if setup.joystick:
            joy_lr = setup.joystick.get_axis(0)
            joy_ud = setup.joystick.get_axis(1)
            joy_a = setup.joystick.get_button(0)

            if joy_lr <= -0.1:
                self.acc.x = -self.thrust
            if joy_lr >= 0.1:
                self.acc.x = self.thrust
            if joy_ud <= -0.1:
                self.acc.y = -self.thrust
            if joy_ud >= 0.1:
                self.acc.y = self.thrust
            if joy_a:
                self.fire()

        self.pos += self.vel

        # apply friction
        self.acc.x += self.vel.x * setup.FRICTION
        self.acc.y += self.vel.y * setup.FRICTION

        # motion
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

        if self.pos.y < 30:
            self.pos.y = 30
        if self.pos.x < 120:
            self.pos.x = 120
        if self.pos.x > setup.SCREEN_SIZE[0] - 20:
            self.pos.x = setup.SCREEN_SIZE[0] - 20
        if self.pos.y > setup.SCREEN_SIZE[1] - 30:
            self.pos.y = setup.SCREEN_SIZE[1] - 30

        self.rect.midright = self.pos
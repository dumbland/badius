

import pygame as pg
from .. import tools, setup

import copy

class Projectile(pg.sprite.Sprite):
    def __init__(self, weapon):
        pg.sprite.Sprite.__init__(self)
        self.weapon = weapon
        self.game = self.weapon.game
        self.ship = self.weapon.ship
        self.pos = pg.math.Vector2(self.weapon.ship.rect.midright, self.weapon.ship.rect.midright)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.cooldown = 0
        self.timer = 0
        self.sound = None
        self.detonates = True
        self.already_dead = False

    def update(self):
        self.vel += self.acc
        self.pos += self.vel + (self.acc * 0.5)

        self.rect.midleft = self.pos
        if self.rect.left > setup.SCREEN_SIZE[0]:
            self.kill()

    def kill(self):
        self.weapon.num_projectiles -= 1
        if not self.already_dead:
            super().kill()


class Laser(Projectile):
    def __init__(self, weapon):
        Projectile.__init__(self, weapon)
        self.image = pg.Surface((1, 4))
        self.image.fill(pg.Color('green'))
        self.rect = self.image.get_rect()
        self.rect.midleft = self.pos
        self.vel = pg.math.Vector2(20, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.sound = setup.SFX['laser']
        self.detonates = False

    def update(self):
        if self.ship.firing:
            #self.rect.inflate_ip(abs(self.vel.x - 1), 0)
            #self.image.fill(pg.Color('green'))
            self.image = pg.transform.scale(self.image, (self.rect.width + int(self.vel.x) - 1, 4))
            self.rect = self.image.get_rect()
            self.rect.midleft = self.ship.rect.midright

        self.rect.midleft = self.pos
        #if not self.ship.firing and self.rect.left > setup.SCREEN_SIZE[0]:
        #    self.kill()

    def kill(self):
        pg.sprite.Sprite.kill(self)

class FinishedLaser(Projectile):
    def __init__(self, weapon, laser):
        super().__init__(weapon)
        self.image = pg.Surface((laser.rect.width, laser.rect.height))
        self.image.fill(pg.Color('green'))
        self.rect = self.image.get_rect()
        self.vel = laser.vel
        self.acc = laser.acc
        self.sound = laser.sound
        self.detonates = False
        self.pos = pg.math.Vector2(laser.ship.pos.x, laser.ship.pos.y)
        self.rect.midleft = self.pos


    def kill(self):
        self.weapon.beam = None
        super().kill()


class Bullet(Projectile):
    def __init__(self, weapon):
        Projectile.__init__(self, weapon)
        self.image = pg.Surface ((12, 4))
        self.image.fill(pg.Color('yellow'))
        pg.draw.rect(self.image, pg.Color('black'), (2, 0, 4, 4))
        self.rect = self.image.get_rect()
        self.vel = pg.math.Vector2(20, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.sound = setup.SFX['bullet']

class Missile(Projectile):
    def __init__(self, weapon):
        Projectile.__init__(self, weapon)
        self.image = pg.Surface((12, 4))
        self.image.fill(pg.Color('red'))
        self.rect = self.image.get_rect()
        self.vel = pg.math.Vector2(1, 0)
        self.acc = pg.math.Vector2(1, 0)
        self.sound = setup.SFX['missile']
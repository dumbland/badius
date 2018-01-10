
import pygame as pg
import copy

from .. import tools, setup
from . import projectiles



class Weapon(object):
    def __init__(self, ship):
        self.ship = ship
        self.game = ship.game
        self.cooldown = 10
        self.timer = self.cooldown
        self.max_projectiles = 0
        self.num_projectiles = 0
        self.projectile = None

    def engage(self):
        if self.timer == self.cooldown and (self.max_projectiles == 0 or self.max_projectiles > self.num_projectiles):
            # fire
            p = self.projectile(self)
            self.game.all_sprites.add(p)
            self.game.projectiles.add(p)
            self.timer = 0
            self.num_projectiles += 1
            if p.sound != None:
                p.sound.play()

    def disengage(self):
        pass

    def tick(self):
        self.timer = min(self.timer + 1, self.cooldown)

    def update(self):
        self.tick()

        if self.ship.firing:
            if self.timer == self.cooldown and (self.max_projectiles == 0 or self.max_projectiles > self.num_projectiles):
                prj = self.projectile(self)
                self.game.all_sprites.add(prj)
                self.game.projectiles.add(prj)
                self.timer = 0
                self.num_projectiles += 1
                if prj.sound is not None:
                    prj.sound.play()


class Chaingun(Weapon):
    def __init__(self, ship):
        Weapon.__init__(self, ship)
        self.cooldown = 5
        self.timer = self.cooldown
        self.max_projectiles = 5
        self.projectile = projectiles.Bullet


class MissileLauncher(Weapon):
    def __init__(self, ship):
        Weapon.__init__(self, ship)
        self.cooldown = 100
        self.timer = self.cooldown
        self.max_projectiles = 1
        self.projectile = projectiles.Missile

class DeathRay(Weapon):
    def __init__(self, ship):
        super().__init__(ship)
        self.cooldown = 10
        self.timer = self.cooldown
        self.num_projectiles = 0
        self.max_projectiles = 2
        self.projectile = projectiles.Laser
        self.beam = None
        self.max_length = 200

    @property
    def num_projectiles(self):
        return self.__num_projectiles

    @num_projectiles.setter
    def num_projectiles(self, value):
        print("Setting num_projectiles to {}".format(value))
        self.__num_projectiles = value

    def update(self):
        self.tick()

        if self.beam is None:
            # no beam in progress
            if self.ship.firing:
                if self.timer == self.cooldown and (self.max_projectiles == 0 or self.max_projectiles > self.num_projectiles):
                    # start new shot
                    laser = self.projectile(self)
                    self.game.lasers.add(laser)
                    self.game.all_sprites.add(laser)
                    self.beam = laser
        else:
            # beam in progress
            if not self.ship.firing or (self.beam.rect.width >= self.max_length):
                # end the beam
                beam = projectiles.FinishedLaser(self, self.beam)
                self.game.projectiles.add(beam)
                self.game.all_sprites.add(beam)
                self.num_projectiles += 1
                self.timer = 0

                self.beam.kill()
                self.beam = None
                self.game.lasers.empty()

            # self.beam is not None and ((not self.ship.firing) or self.beam.rect.width >= self.max_length) :



    # def engage(self):
    #     if self.timer == self.cooldown and self.beam is None and (self.max_projectiles == 0 or self.max_projectiles > self.num_projectiles):
    #         laser = self.projectile(self)
    #         self.game.lasers.add(laser)
    #         self.game.all_sprites.add(laser)
    #         self.beam = laser
    #
    # def disengage(self):
    #     if self.beam is not None:
    #         beam = projectiles.FinishedLaser(self, self.beam)
    #         self.game.projectiles.add(beam)
    #         self.game.all_sprites.add(beam)
    #
    #         # self.beam.kill()
    #         # self.beam = None
    #
    #         self.num_projectiles += 1
    #         self.timer = 0
    #
    #
    # def update(self):
    #     super().update()
    #     if self.beam and self.beam.rect.width >= self.max_length:
    #         self.disengage()
    #         # print(self.num_projectiles)

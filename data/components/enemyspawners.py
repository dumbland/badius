import pygame as pg
import math
import random

from .. import tools, setup
from . import enemies, explosions

random.seed()

class EnemySpawner(pg.sprite.Group):
    def __init__(self, owner):
        super().__init__()
        self.game = owner
        self.frames_since_spawn = 0
        self.max_enemies = 0
        self.enemy_type = None
        self.dead = False

    def start(self):
        pass

    def update(self, *args):
        self.frames_since_spawn += 1
        super().update(self, *args)

    def basic_motion(self):
        for e in self.sprites():
            e.vel += e.acc
            e.pos += e.vel + (0.5 * e.acc)
            e.rect.center = e.pos
            if e.pos.x < 0 - e.rect.width:
                e.kill()

    def add_explosion(self, sprite):
        exp = explosions.Explosion(sprite)
        self.game.all_sprites.add(exp)
        self.game.explosions.add(exp)

class RandomGrunts(EnemySpawner):
    def __init__(self, owner):
        super().__init__(owner)
        self.max_enemies = 12
        self.enemy_type = enemies.Grunt
        # self.start()

    def randomise_position(self, enemy):
        enemy.pos.x = setup.SCREEN_SIZE[0] + random.randrange(32, setup.SCREEN_SIZE[0])
        enemy.pos.y = random.randrange(32, setup.SCREEN_SIZE[1] - 64)
        enemy.vel.x = -(random.randrange(2, 8))
        return enemy

    def update(self, *args):
        super().update(*args)
        while len(self.sprites()) < self.max_enemies:
            e = self.randomise_position(self.enemy_type(self))
            self.game.all_sprites.add(e)
            self.game.enemies.add(e)
            self.add(e)
        self.basic_motion()

class Looper(EnemySpawner):
    def __init__(self, game):
        super().__init__(game)
        self.max_enemies = 6
        self.enemy_type = enemies.Squiggy
        self.frame_since_rotate = 0
        self.looping = []
        self.vel_x = -5
        self.radius = 128
        self.angle = 360/self.max_enemies
        self.arclength = (self.angle / 360) * (2 * math.pi * self.radius)
        self.start_loop_x = setup.SCREEN_WIDTH * 3/4
        self.frames_since_rotate = 0
        self.pos = pg.math.Vector2(0, 0)
        self.start()



    def start(self):
        super().start()
        index = 0
        self.pos.x = setup.SCREEN_WIDTH
        self.pos.y = random.randrange(setup.SCREEN_HEIGHT/4, setup.SCREEN_HEIGHT*3/4)
        while len(self.sprites()) < self.max_enemies:
            enemy = self.enemy_type(self)
            enemy.index = index
            enemy.vel.x = self.vel_x
            enemy.pos.x = self.pos.x + enemy.index * self.arclength
            enemy.pos.y = self.pos.y - self.radius
            enemy.rect.center = enemy.pos
            self.game.all_sprites.add(enemy)
            self.game.enemies.add(enemy)
            self.add(enemy)
            index += 1
            self.looping.append(False)
            print("Creating new Looper")

    def update(self, *args):
        super().update(*args)
        if self.frames_since_rotate > 0:
            self.frames_since_rotate += 1

        for enemy in self.sprites():
            if enemy.pos.x <= self.start_loop_x:
                self.looping[enemy.index] = True
                if self.frames_since_rotate == 0:
                    self.frames_since_rotate = 1
                    self.pos.x = self.start_loop_x

            if self.looping[enemy.index]:
                vel_a = (self.vel_x) / (2*math.pi*self.radius) * 360
                angle = -(enemy.index*self.angle) - (vel_a * self.frames_since_rotate - 1) + 90
                enemy.pos.x = (self.radius * math.cos(-angle * math.pi/180)) + self.pos.x
                enemy.pos.y = (self.radius * math.sin(-angle * math.pi/180)) + self.pos.y
                enemy.rect.center = enemy.pos
            else:
                enemy.pos += enemy.vel
                enemy.rect.center = enemy.pos

        # if self.frame_since_rotate > 0:
        #     self.frame_since_rotate += 1
        #
        # if self.pos.x <= setup.SCREEN_WIDTH*3/4:
        #     self.frame_since_rotate = 1
        #     self.vel.x = 0
        #
        # for enemy in self.sprites():
        #     if enemy.pos.x <= self.pos.x:
        #         self.looping[enemy.index] = True
        #     if self.looping[enemy.index]:
        #         angular_vel = (5/2) / (256*math.pi) * 360
        #         angle = enemy.index*-60 + (self.frame_since_rotate-1) * -angular_vel + 90
        #         enemy.pos.x = (128 * math.cos(-angle * math.pi/180)) + self.pos.x
        #         enemy.pos.y = (128 * math.sin(-angle * math.pi/180)) + self.pos.y
        #         enemy.rect.center = enemy.pos
        #         enemy.rotate = angle - 90
        #     else:
        #         arclength = 60/360 * (2*math.pi*128)
        #         enemy.pos.x = self.pos.x + (arclength * enemy.index)
        #         enemy.pos.y = (128 * math.sin(-(90) * math.pi/180)) + self.pos.y
        #         enemy.rect.center = enemy.pos
        #         enemy.rotate = 0
        #

        # for enemy in self.sprites():
        #     if self.pos.x <= setup.SCREEN_WIDTH*3/4:
        #         if self.frame_since_rotate == 0:
        #             self.vel.x = 0
        #             self.frame_since_rotate = 1
        #
        #         angular_velocity = ((self.vel.x/2) / (256 * math.pi)) * 360
        #         angle = (enemy.index * -60) + (self.frame_since_rotate * -angular_velocity) + 90
        #         # arclength = angle/360 * (2 * math.pi * 128)
        #
        #         enemy.pos.x = (128 * math.cos(-(angle) * math.pi/180)) + self.pos.x
        #         enemy.pos.y = (128 * math.sin(-(angle) * math.pi/180)) + self.pos.y
        #         enemy.rect.center = enemy.pos
        #         enemy.rotate = angle - 90
        #     else:
        #         arclength = 60/360 * (2 * math.pi * 128)
        #         enemy.pos.x = self.pos.x + (arclength * enemy.index)
        #         enemy.pos.y = (128 * math.sin(-(90) * math.pi/180)) + self.pos.y
        #         enemy.rect.center = enemy.pos
        #         enemy.rotate = 0
        #         print("{} {}".format(enemy.index, enemy.pos))

        if len(self.sprites()) <= 0:
            self.dead = True





class SineCluster(EnemySpawner):
    def __init__(self, game):
        super().__init__(game)
        self.max_enemies = 6
        self.enemy_type = enemies.Squiggy
        self.pos = pg.math.Vector2(setup.SCREEN_SIZE[0], random.randrange(setup.SCREEN_SIZE[1]/4, setup.SCREEN_SIZE[1]*3/4))
        self.start()


    def start(self):
        super().start()
        index = 0
        while len(self.sprites()) < self.max_enemies:
            e = self.enemy_type(self)
            e.pos.x = self.pos.x + 32 + (index * 92)
            e.pos.y = self.pos.y + random.randrange(0, setup.SCREEN_SIZE[1]/2)
            # e.vel.y = 5
            e.index = index
            e.rect.center = e.pos
            self.game.all_sprites.add(e)
            self.game.enemies.add(e)
            self.add(e)
            index += 1
            print("Creating new SineCluster {}, {}".format(e.pos.x, e.pos.y))

    def update(self, *args):
        super().update()
        f = 8
        a = 128
        # + (speed * self.time_since_spawn)
        for e in self.sprites():
            e.pos.x += e.vel.x
            e.pos.y = self.pos.y + int(a * math.sin(f * ((float(e.pos.x + (e.index * 92)) / setup.SCREEN_SIZE[0]) * (2 * math.pi))))
            e.rect.center = e.pos

        if len(self.sprites()) == 0:
            self.dead = True
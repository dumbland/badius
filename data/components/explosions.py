
import pygame as pg

from .. import setup, tools

class Explosion(pg.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        self.strip = tools.strip_from_sheet(setup.GFX['kaboom'],
                                            (0, 0), (64, 64), 3)
        self.pos = sprite.pos
        self.vel = sprite.vel
        self.acc = sprite.acc
        self.animation_frames = 5
        self.timer = 0
        self.frame = 0
        self.image = self.strip[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = sprite.pos
        self.time_to_live = self.animation_frames * len(self.strip)

    def update(self, *args):
        self.timer += 1
        if self.timer % self.animation_frames == 0:
            self.frame = (self.frame + 1) % len(self.strip)
            self.image = self.strip[self.frame]

        self.pos.x += self.vel.x
        self.rect.center = self.pos

        if self.pos.x < 0 or self.timer >= self.time_to_live:
            self.kill()
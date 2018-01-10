"""
The class for our Game scene is found here.
"""

import pygame as pg
import random

from .. import setup, tools
from ..components import Starfield, Player, RandomGrunts, SineCluster, Looper


class Game(tools._State):
    """This state could represent the actual gameplay phase."""
    def __init__(self):
        tools._State.__init__(self)
        self.next = "INTRO"
        # self.bgm = setup.MUSIC["Anitek_-_07_-_Contact"]
        # self.font = pg.font.Font(setup.FONTS["Fixedsys500c"], 50)
        # text = ["This is the game.", "Music should be playing",
        #         "to demonstrate", "that the intro movie",
        #         "has relinquished control", "of the mixer module.", "",
        #         "Press escape to return", "to the intro movie."]
        # self.rendered_text = self.make_text_list(self.font, text,
        #                                          pg.Color("white"), 50, 50)
        # self.escape = self.render_font(self.font, "Press Escape",
        #                                pg.Color("yellow"),
        #                                (setup.SCREEN_RECT.centerx, 550))
        self.blink = False
        self.timer = 0.0
        self.screen = pg.Surface(setup.SCREEN_SIZE)
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.starfield = Starfield(self.screen)
        self.spawners = []

    def startup(self, current_time, persistant):
        self.spawners = [RandomGrunts(self), Looper(self)]
        return tools._State.startup(self, current_time, persistant)

    def cleanup(self):
        return tools._State.cleanup(self)

    def make_text_list(self, font, strings, color, start_y, y_space):
        """
        Takes a list of strings and returns a list of
        (rendered_surface, rect) tuples. The rects are centered on the screen
        and their y coordinates begin at starty, with y_space pixels between
        each line.
        """
        rendered_text = []
        for i,string in enumerate(strings):
            msg_center = (setup.SCREEN_RECT.centerx, start_y + i * y_space)
            msg_data = self.render_font(font, string, color, msg_center)
            rendered_text.append(msg_data)
        return rendered_text

    def get_event(self, event):
        """Go back to intro on escape key."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True

    def draw(self, surface):
        """Blit all elements to surface."""
        # surface.fill(pg.Color("lightslategrey"))
        # for msg in self.rendered_text:
        #     surface.blit(*msg)
        # if self.blink:
        #     surface.blit(*self.escape)
        self.screen.fill(pg.Color('black'))

        for star in self.starfield.sprites():
            self.screen.blit(star.image, (star.pos.x, star.pos.y))

        for projectile in self.projectiles.sprites():
            self.screen.blit(projectile.image, projectile.rect)

        for laser in self.lasers.sprites():
            # print(laser.rect.width)
            self.screen.blit(laser.image, laser.rect)

        for enemy in self.enemies.sprites():
            self.screen.blit(enemy.image, enemy.rect)

        for explosion in self.explosions.sprites():
            self.screen.blit(explosion.image, explosion.rect)

        self.screen.blit(self.player.image, self.player.rect)

        prj_text = self.render_font(pg.font.SysFont(None, 32),
                                    "Velocity: {:.2f}, {:.2f} Projectiles: {} Enemies: {}".format(self.player.vel.x, self.player.vel.y, len(self.projectiles.sprites()) + len(self.lasers.sprites()), len(self.enemies.sprites())),
                                    pg.Color('yellow'),
                                    (setup.SCREEN_SIZE[0]/2, 10))
        self.screen.blit(*prj_text)

        surface.blit(self.screen, (0, 0))


    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.current_time = current_time
        args = (surface, keys, current_time, time_delta)
        # if self.current_time-self.timer > 1000.0/5.0:
        #     self.blink = not self.blink
        #     self.timer = self.current_time

        for spawner in self.spawners:
            spawner.update(*args)
            if spawner.dead:
                self.spawners.remove(spawner)
        while len(self.spawners) < 2:
            # spawners = [Looper(self), SineCluster(self)]
            # idx = random.randrange(0, len(spawners))
            spawner = Looper(self) # spawners[idx]
            spawner.origin_y = random.randrange(setup.SCREEN_SIZE[1]/4, setup.SCREEN_SIZE[1] * 3/4)
            self.spawners.append(spawner)

        self.starfield.update()
        self.all_sprites.update()

        for p in self.projectiles.sprites():
            hits = pg.sprite.spritecollide(p, self.enemies, False)
            if hits:
                for hit in hits:
                    if hit.death_sound != None:
                        hit.death_sound.play()
                    hit.kill(True)
                if p.detonates:
                    p.kill()

        for l in self.lasers.sprites():
            hits = pg.sprite.spritecollide(l, self.enemies, False)
            if hits:
                for hit in hits:
                    if hit.pos.x < setup.SCREEN_SIZE[0]:
                        if hit.death_sound != None:
                            hit.death_sound.play()
                        hit.kill()


        self.draw(surface)

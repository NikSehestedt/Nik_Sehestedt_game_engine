#This file was created by Nik Sehestedt
import pygame as pg
from settings import *

# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.groups = game.all_sprites
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * tilesize
        self.y = y * tilesize
    def death(self):
        self.x = self.game.p1col*tilesize
        self.y = self.game.p1row*tilesize
        print("You Died")
    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def collide_with_deathblocks(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.deathblocks, False)
            if hits:
                self.death()

               
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.vy = PLAYER_SPEED
    # bad move
    # def move(self, dx = 0, dy = 0):
    #     self.x += dx
    #     self.y += dy
    #better move
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.collide_with_deathblocks('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_deathblocks('x')
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.groups = game.all_sprites
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

class Deathblock(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.deathblocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
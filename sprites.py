#This file was created by Nik Sehestedt
import pygame as pg
from settings import *
from random import choice
# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.groups = game.all_sprites
        #self.image = pg.Surface((tilesize, tilesize))
        self.effect = ""
        self.image = game.player_img
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * tilesize
        self.y = y * tilesize
        self.moneybag = 0
        self.speed = 300
        
    def death(self):
        self.x = self.game.p1col*tilesize
        self.y = self.game.p1row*tilesize
        self.speed = 300
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
    def invccollisions(self, group, dir):
        if self.effect == "invincibility":
            if dir == "x":
                hits = pg.sprite.spritecollide(self, group, False)
                if hits:
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                    self.rect.x = self.x
            if dir == "y":
                hits = pg.sprite.spritecollide(self, group, False)
                if hits:
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                    self.rect.y = self.y
    
    #checks if the player collides with a sprite
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            #if its a coin
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
               # if self.moneybag == 25:

            #if its a powerup
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.effect = choice(Powerupeffects)
                print (self.effect)
                if self.effect == "speed":
                    self.speed += 100
                    self.image = self.game.player_img
                if self.effect == "invincibility":
                    self.image = self.game.invcplayer_img
            if str(hits[0].__class__.__name__) == "Deathblock":
                if self.effect != "invincibility":
                    self.death()
                if self.effect == "invincibility":
                    self.rect.x = self.x
                    self.invccollisions(self.game.deathblocks, 'x')
                    self.rect.y = self.y
                    self.invccollisions(self.game.deathblocks, 'y')
            if str(hits[0].__class__.__name__) == "Enemy":
                if self.effect != "invincibility":
                    self.death()


               
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vx = -self.speed
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vx = self.speed
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.vy = -self.speed
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # def interact(self):
    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_KP_ENTER]:

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
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.deathblocks, False)
        self.collide_with_group(self.game.coins,True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.groups = game.all_sprites
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(AQUA)
        #self.image = game.wall_img
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
        #self.image = pg.Surface((tilesize, tilesize))
        #self.image.fill(RED)
        self.image = game.deathblock_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((tilesize, tilesize))
        #self.image.fill(YELLOW)
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((tilesize, tilesize))
        #self.image.fill(PURPLE)
        self.image = game.powerups_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, countdown):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.countdown = countdown
        self.tick = self.game.clock.tick
        #self.image = pg.Surface((tilesize, tilesize))
        #self.image.fill(RED)
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * tilesize
        self.y = y * tilesize
        self.speed = 1
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
            hitsd = pg.sprite.spritecollide(self, self.game.deathblocks, False)
            if hitsd:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
            hitsd = pg.sprite.spritecollide(self, self.game.deathblocks, False)
            if hitsd:
                self.vy *= -1
                self.rect.y = self.y
                
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if self.rect.x < self.game.p1.rect.x:
            self.vx = 200
        if self.rect.x > self.game.p1.rect.x:
            self.vx = -200
        if self.rect.y < self.game.p1.rect.y:
            self.vy = 200
        if self.rect.y > self.game.p1.rect.y:
            self.vy = -200
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
#This file was created by Nik Sehestedt
import pygame as pg
from settings import *
from random import choice
# write a player class
vec = pg.math.Vector2
def collide_with_walls(sprite, group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

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
        self.pos = vec(0,0)
        self.sheathed = True
        if self.sheathed == False:
            self.speed = 200
        
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
        if dir == 'y':
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

class Weapon(pg.sprite.Sprite):
    def __init__(self, player, game,x,y):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.p1 = player
        self.image = game.sword_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * tilesize
        self.rect.y = self.y * tilesize

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Enemy":
               hits[0].hp -= 1
    def update(self):
        keys = pg.key.get_pressed()
        if self.p1.sheathed == False:
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                self.rect.x = self.p1.rect.x-32
                self.rect.y = self.p1.rect.y
                self.image = self.game.swordleft_img
            if keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.rect.x = self.p1.rect.x+32
                self.rect.y = self.p1.rect.y
                self.image = self.game.swordright_img
            if keys[pg.K_w] or keys[pg.K_UP]:
                self.rect.x = self.p1.rect.x
                self.rect.y = self.p1.rect.y-32
                self.image = self.game.sword_img
            if keys[pg.K_s] or keys[pg.K_DOWN]:
                self.rect.x = self.p1.rect.x
                self.rect.y = self.p1.rect.y+32
                self.image = self.game.sworddown_img
            if keys[pg.K_e]:
                self.rect.x = self.game.weaponcol
                self.rect.y = self.game.weaponrow
                self.p1.sheathed = True
        if self.p1.sheathed == True:
            if keys[pg.K_e]:
                self.rect.x = self.p1.rect.x
                self.rect.y = self.p1.rect.y-32
                self.p1.sheathed = False
                print("I should be getting teleported")
        self.collide_with_group(self.game.mobs, False)
        #if self.sheathed == False:
        #     if keys[pg.K_e]:
                
        #         self.sheathed = True
        


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
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.enemy_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * tilesize
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = 150
        self.hp = 3
    # def collide_with_group(self, group, kill):
    #     hits = pg.sprite.spritecollide(self, group, kill)
    #     if str(hits[0].__class__.__name__) == "Weapon":
    #         self.hp -= 1
    #         print("The enemy took damage")

    def update(self):
        self.rot = (self.game.p1.rect.center - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.deathblocks, 'x')
        collide_with_walls(self, self.game.deathblocks, 'y')
        #self.collide_with_group(self.game.weapons, False)
        if self.hp < 1:
            self.kill()
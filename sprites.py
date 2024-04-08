#This file was created by Nik Sehestedt
import pygame as pg
from settings import *
from random import choice
from random import randint
from utils import *
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
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.groups = game.all_sprites
        #self.image = pg.Surface((tilesize, tilesize))
        self.effect = ""
        self.image = game.player_img
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.mx, self.my =0,0
        self.x = x * tilesize
        self.y = y * tilesize
        self.moneybag = 0
        self.speed = 300
        self.pos = vec(0,0)
        self.sheathed = True
        self.cooling = False
        self.damagecooling = False
        self.health = 100
        self.movebox = [506, 522, 344, 360]
        self.map_pos = (0,0)
    def death(self):
        self.x = self.game.p1col*tilesize
        self.y = self.game.p1row*tilesize
        self.speed = 300
        print("You Died")
    def movebox_collisions(self):
        self.mx, self.my = 0,0
        if self.mx != 0 and self.my != 0:
            self.mx *= 0.7071
            self.my *= 0.7071
        if self.rect.x <= self.movebox[0]:
            if self.vx < 0:
                    self.x = self.movebox[0]
            self.mx = self.speed
            if self.goingright == True:
                self.vx = self.mx
            else:
                self.vx = 0
            self.rect.x = self.x
            self.movebox[0] += -self.mx * self.game.dt
            self.movebox[1] += -self.mx * self.game.dt
        if self.rect.x >= self.movebox[1]:
            if self.vx > 0:
                    self.x = self.movebox[1]
            self.mx = -self.speed
            if self.goingleft == True:
                self.vx = self.mx
            else:
                self.vx = 0
            self.rect.x = self.x
            self.movebox[0] += -self.mx * self.game.dt
            self.movebox[1] += -self.mx * self.game.dt
        if self.rect.y <= self.movebox[2]:
            if self.vy < 0:
                    self.y = self.movebox[2]
            self.my = self.speed
            if self.goingup == True:
                self.vy = self.my
            else:
                self.vy = 0
            self.rect.y = self.y
            self.movebox[2] += -self.my * self.game.dt
            self.movebox[3] += -self.my * self.game.dt
        if self.rect.y >= self.movebox[3]:
            if self.vy > 0:
                    self.y = self.movebox[3]
            self.my = -self.speed
            if self.goingdown == True:
                self.vy = self.my
            else:
                self.vy = 0
            self.rect.y = self.y
            self.movebox[2] += -self.my * self.game.dt
            self.movebox[3] += -self.my * self.game.dt
        
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
               # if self.moneybag == 25
            if str(hits[0].__class__.__name__) == "Deathblock":
                if self.effect != "invincibility":
                    self.health -= 3
                    self.damagecooling = True
                    self.game.cooldown.cd = 0.3
                if self.effect == "invincibility":
                    self.rect.x = self.x
                    self.invccollisions(self.game.deathblocks, 'x')
                    self.rect.y = self.y
                    self.invccollisions(self.game.deathblocks, 'y')
            if str(hits[0].__class__.__name__) == "Enemy":
                if self.effect != "invincibility":
                    self.health-=randint(10,25)
                    self.damagecooling = True
                    self.game.cooldown.cd = 0.4
            #if its a powerup
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.effect = choice(Powerupeffects)
                print (self.effect)
                self.game.cooldown.cd = 5
                self.cooling = True
                if self.effect == "speed":
                    self.speed += 100
                    
                    self.image = self.game.player_img
                if self.effect == "invincibility":
                    self.image = self.game.invcplayer_img


               
    def get_keys(self):
        self.mapx,self.mapy = self.map_pos
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vx = -self.speed
            self.goingleft = True
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vx = self.speed
            self.goingright = True
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.vy = -self.speed
            self.goingup = True
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.vy = self.speed
            self.goingdown = True
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        else:
            self.goingleft = False
            self.goingright = False
            self.goingup = False
            self.goingdown = False
        
        if self.sheathed == True:
            if keys[pg.K_e]:
                self.weapon = Weapon(self.game, self.rect.x, self.rect.y - 32)
                self.sheathed = False
        # if self.rect.x <= self.movebox[0]:
        #     self.vx = self.speed
        #     self.mx = self.speed
        #     self.movebox[0] += -self.mx * self.game.dt
        #     self.movebox[1] += -self.mx * self.game.dt
        # elif self.rect.x >= self.movebox[1]:
        #     self.vx = -self.speed
        #     self.mx = -self.speed
        #     self.movebox[0] += -self.mx * self.game.dt
        #     self.movebox[1] += -self.mx * self.game.dt
        # if self.rect.y <= self.movebox[2]:
        #     self.vy = self.speed
        #     self.my = self.speed
        #     self.movebox[2] += -self.my * self.game.dt
        #     self.movebox[3] += -self.my * self.game.dt
        # elif self.rect.y >= self.movebox[3]:
        #     self.vy = -self.speed
        #     self.my = -self.speed
        #     self.movebox[2] += -self.my * self.game.dt
        #     self.movebox[3] += -self.my * self.game.dt
        
        


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
        self.collide_with_group(self.game.coins,True)
        self.movebox_collisions()
        self.mapx += self.mx *self.game.dt
        self.mapy += self.my *self.game.dt
        self.map_pos = (self.mapx,self.mapy)
        if self.game.cooldown.cd < 1:
            self.cooling = False
            self.speed = 300
            self.image = self.game.player_img
            self.effect = ""
        if not self.cooling:
            self.collide_with_group(self.game.power_ups, True)
        if not self.damagecooling:
            self.collide_with_group(self.game.deathblocks, False)
            self.collide_with_group(self.game.mobs, False)
        if self.health <= 0:
            self.death()
       

   # def render(self,display):
    #    display.blit(self.image,(self.rect.x,self.rect.y))
class Weapon(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.sword_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * tilesize
        self.rect.y = self.y * tilesize
        #self.cooling = False

    # def collide_with_group(self, group, kill):
    #     hits = pg.sprite.spritecollide(self, group, kill)
    #     if hits:
    #         if str(hits[0].__class__.__name__) == "Enemy":
    #            hits[0].hp -= 1
    #            self.game.cooldown.cd = 1
    #            self.cooling = True
    def update(self):
        keys = pg.key.get_pressed()
        if self.game.p1.sheathed == False:
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                self.rect.x = self.game.p1.rect.x-32
                self.rect.y = self.game.p1.rect.y
                self.image = self.game.swordleft_img
            if keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.rect.x = self.game.p1.rect.x+32
                self.rect.y = self.game.p1.rect.y
                self.image = self.game.swordright_img
            if keys[pg.K_w] or keys[pg.K_UP]:
                self.rect.x = self.game.p1.rect.x
                self.rect.y = self.game.p1.rect.y-32
                self.image = self.game.sword_img
            if keys[pg.K_s] or keys[pg.K_DOWN]:
                self.rect.x = self.game.p1.rect.x
                self.rect.y = self.game.p1.rect.y+32
                self.image = self.game.sworddown_img
            if keys[pg.K_e]:
                self.kill()
                self.game.p1.sheathed = True
                
        
        #if self.game.cooldown.cd <= 0:
        #    self.cooling = False
        #if not self.cooling:
        #    self.collide_with_group(self.game.mobs, False)
        #if self.sheathed == False:
        #     if keys[pg.K_e]:
                
        #         self.sheathed = True
        


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls, game.np_sprites
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
        self.groups = game.all_sprites, game.deathblocks, game.np_sprites
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
        self.groups = game.all_sprites, game.coins, game.np_sprites
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
        self.groups = game.all_sprites, game.power_ups, game.np_sprites
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
        self.groups = game.all_sprites, game.mobs, game.np_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.damageicon = False
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
        self.cooling = False
        self.imagecooling = 0
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Weapon":
                self.hp -= 1
                self.cooling = True
                self.game.cooldown.cd = 3
                self.damageicon = True
                self.imagecooling = self.game.cooldown.cd = 0.1
                print("The enemy took damage")

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
        if self.game.cooldown.cd <= 0:
            self.cooling = False
        if self.imagecooling <= 0:
            self.damageicon = False
        if self.damageicon:
            self.image = pg.Surface((tilesize, tilesize))
            self.image.fill(white)
        if not self.damageicon:
            self.image = self.game.enemy_img
        
        if not self.cooling:
            self.collide_with_group(self.game.weapons, False)
        if self.hp <= 0:
            self.kill()
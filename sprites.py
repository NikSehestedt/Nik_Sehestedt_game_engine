#This file was created by Nik Sehestedt
#imports the libraries
import pygame as pg
from settings import *
from random import choice
from random import randint
from utils import *
from math import *
#sets vec
vec = pg.math.Vector2
#creates a collide_with_walls for the enemies
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
#creates player
class Player(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        #assigns player to groups
        self.groups = game.all_sprites, game.players
        #initializes sprite code
        pg.sprite.Sprite.__init__(self, self.groups)
        #sets all the data up
        self.game = game
        self.effect = ""
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.mx, self.my =0,0
        self.x = x*tilesize
        self.y = y*tilesize
        self.moneybag = 0
        self.speed = 300
        self.pos = vec(0,0)
        self.position = vec(self.x, self.y)
        self.sheathed = True
        self.cooling = False
        self.damagecooling = False
        self.swordcooling = False
        self.health = 100
        self.movebox = [(self.game.p1col*32) - 16, (self.game.p1col*32), (self.game.p1row*32)-16, (self.game.p1row*32)]
        self.map_pos = (0,0)
        self.mapx, self.mapy = self.map_pos
    #kills the player
    def death(self):
        self.rect.x = self.game.p1col*tilesize
        self.rect.y = self.game.p1row*tilesize
        self.x = self.game.p1col*tilesize
        self.y = self.game.p1row*tilesize
        self.speed = 300
        self.health = 100
        print("You Died")
    #makes it so the player can move the map creating the illusion of a moving camera
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
    #collision for walls
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

    #collisions for when the player is invincible (currently bugged)
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
               
        #if its a deathblock
            if str(hits[0].__class__.__name__) == "Deathblock":
                if self.effect != "invincibility":
                    self.health -= 3
                    self.damagecooling = True
                    self.game.cooldown.cd = 1
                if self.effect == "invincibility":
                    #makes it so you cant phase through deathblocks while invincible
                    self.rect.x = self.x
                    self.invccollisions(self.game.deathblocks, 'x')
                    self.rect.y = self.y
                    self.invccollisions(self.game.deathblocks, 'y')
                    #collides with enemies
            if str(hits[0].__class__.__name__) == "Enemy":
                if self.effect != "invincibility":
                    self.health-=randint(10,25)
                    print("I took damage")
                    self.damagecooling = True
                    self.game.cooldown.cd = 2
                    #collides with bosses
            if str(hits[0].__class__.__name__) == "Boss":
                if self.effect != "invincibility":
                    #more damage than normal enemy
                    self.health-=randint(15,35)
                    print("I took damage")
                    self.damagecooling = True
                    self.game.cooldown.cd = 2
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


    #finds out what keys you are pressing
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        #standard directions
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
            #for movebox collisions
            self.goingleft = False
            self.goingright = False
            self.goingup = False
            self.goingdown = False
        if self.sheathed == True:
            if self.swordcooling == False:
                if keys[pg.K_e]:
                    self.weapon = Weapon(self.game, self.rect.x, self.rect.y)
                    self.sheathed = False
                    #makes it so you dont accidently instantly delete the sword
                    self.swordcooling = True
                    self.game.cooldown.cd = 3

    #updates everything for the player(everything that gets repeated goes here)
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
        #disables cooldowns
        if self.game.cooldown.cd < 1:
            self.cooling = False
            self.damagecooling = False
            self.swordcooling = False
            self.speed = 300
            self.image = self.game.player_img
            self.effect = ""
        #lets us pick up powerups again
        if not self.cooling:
            self.collide_with_group(self.game.power_ups, True)
        #ends i-frames
        if not self.damagecooling:
            self.collide_with_group(self.game.deathblocks, False)
            self.collide_with_group(self.game.mobs, False)
            self.collide_with_group(self.game.bosses, False)
        #triggers death
        if self.health <= 0:
            self.death()
       
#creates the sword
class Weapon(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.originalimage = game.sword_img
        self.image = game.sword_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 0,0
        self.rect.x = self.x
        self.rect.y = self.y
        
    #useless
    def follow(self,obj):
        self.vx = obj.vx
        self.vy = obj.vy
    #sword spins around the player(currently buggy)
    # def rotate(self):
    #     mouse_x, mouse_y = pg.mouse.get_pos()
    #     rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
    #     angle = (180 / pi) * -atan2(rel_y, rel_x)
    #     self.image = pg.transform.rotate(self.originalimage, int(angle))
    #     self.rect = self.image.get_rect(center = (self.game.p1.x + 32*cos(angle), self.game.p1.y + 32*sin(angle)))
    #     self.center = (self.game.p1.x + 32*cos(angle), self.game.p1.y + 32*sin(angle))
    def point_at(self, x, y):
        self.angle = 180+degrees(atan2(x-self.game.p1.rect.x, y-self.game.p1.rect.y))
        self.image = pg.transform.rotate(self.originalimage, self.angle)
        self.rect = self.image.get_rect(center = ((self.game.p1.rect.x + 32*cos(self.angle)), (self.game.p1.rect.y + 32*sin(self.angle))))
        self.circle = ((self.game.p1.rect.x + 32*cos(self.angle)), (self.game.p1.rect.y + 32*sin(self.angle)))
    #updates the sword
    def update(self):
        self.follow(self.game.p1)
        self.point_at(*pg.mouse.get_pos())
        #self.x += self.vx * self.game.dt
        #self.y += self.vy * self.game.dt
        self.x, self.y = self.circle
        self.rect.x = self.x
        self.rect.y = self.y
        keys = pg.key.get_pressed()
        if self.game.p1.sheathed == False:
            # if keys[pg.K_a] or keys[pg.K_LEFT]:
            #     self.rect.x = self.game.p1.rect.x
            #     self.rect.y = self.game.p1.rect.y-32
            # #     self.rect.x = self.game.p1.rect.x-32
            # #     self.rect.y = self.game.p1.rect.y
            # #     #self.image = self.game.swordleft_img
            # if keys[pg.K_d] or keys[pg.K_RIGHT]:
            #     self.rect.x = self.game.p1.rect.x
            #     self.rect.y = self.game.p1.rect.y-32
            # #     self.rect.x = self.game.p1.rect.x+32
            # #     self.rect.y = self.game.p1.rect.y
            # #     #self.image = self.game.swordright_img
            # if keys[pg.K_w] or keys[pg.K_UP]:
            #     self.rect.x = self.game.p1.rect.x
            #     self.rect.y = self.game.p1.rect.y-32
            # #     #self.image = self.game.sword_img
            # if keys[pg.K_s] or keys[pg.K_DOWN]:
            #     self.rect.x = self.game.p1.rect.x
            #     self.rect.y = self.game.p1.rect.y-32
            # #     self.rect.x = self.game.p1.rect.x
            # #     self.rect.y = self.game.p1.rect.y+32
                #self.image = self.game.sworddown_img
            if self.game.p1.swordcooling == False:
                if keys[pg.K_e]:
                    self.kill()
                    self.game.p1.sheathed = True
                    self.game.p1.swordcooling = True
                    self.game.cooldown.cd = 3
#creates walls
class Wall(pg.sprite.Sprite):
    #everything in init follows the same structure as Player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls, game.np_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(AQUA)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
#creates deathblocks
class Deathblock(pg.sprite.Sprite):
    #same here
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.deathblocks, game.np_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.deathblock_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
#creates coins
class Coin(pg.sprite.Sprite):
    #and here
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins, game.np_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
#creates powerups
class PowerUp(pg.sprite.Sprite):
    #anddd here
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups, game.np_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.powerups_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
#creates safespaces(currently enemies can clip so not really safe)
class Safespace(pg.sprite.Sprite):
    #here too
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.safewalls, game.np_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.safe_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
#creates enemies
class Enemy(pg.sprite.Sprite):
    #and finally here
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs, game.np_sprites
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
        self.cooling = False
        self.imagecooling = 0
    #collides with sprites(only the sword rn)
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Weapon":
                self.hp -= 1
                self.cooling = True
                self.game.cooldown.cd = 2
                print("The enemy took damage")
    #moves toward the player and collides with walls deathblocks and safewalls
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
        collide_with_walls(self, self.game.safewalls, 'x')
        collide_with_walls(self, self.game.safewalls, 'y')
        #these are to create i-frames
        if self.game.cooldown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.collide_with_group(self.game.weapons, False)
        #kills it
        if self.hp <= 0:
            self.kill()
            self.game.p1.moneybag += 2
    #creates bosses
class Boss(pg.sprite.Sprite):
    #and finally here
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bosses, game.np_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.boss_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * tilesize
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = 100
        self.hp = 30
        self.cooling = False
        self.imagecooling = 0
    #collides with sprites(only the sword rn)
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Weapon":
                self.hp -= 1
                self.cooling = True
                self.game.cooldown.cd = 2
                print("The enemy took damage")
    #moves toward the player and collides with walls deathblocks and safewalls
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
        collide_with_walls(self, self.game.safewalls, 'x')
        collide_with_walls(self, self.game.safewalls, 'y')
        #these are to create i-frames
        if self.game.cooldown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.collide_with_group(self.game.weapons, False)
        #kills it
        if self.hp <= 0:
            self.kill()
            self.game.p1.moneybag += 20
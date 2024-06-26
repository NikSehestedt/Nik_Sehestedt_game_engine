#This file was created by Nik Sehestedt
#imports the libraries
import pygame as pg
from settings import *
from random import *
from utils import *
from math import *
from os import path
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
        # self.spritesheet = Spritesheet(path.join(img_dir, P1SPRITESHEET))
        # self.load_images()
        # self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.mx, self.my =0,0
        self.x = x*tilesize
        self.y = y*tilesize
        self.moneybag = 0
        self.kills = 0
        self.speed = 200
        self.pos = vec(0,0)
        self.position = vec(self.x, self.y)
        self.Psheathed = True
        self.Ssheathed = True
        self.health = 100
        #sets the cooldown
        self.cooling = False
        self.damagecooling = False
        self.swordcooling = False
        #sets the position of the map
        self.map_pos = (width/2 - 32 - self.x, height/2 - 32 - self.y)
        self.mapx, self.mapy = self.map_pos
        self.handsaway = False
        self.hands = Hands(self.game, self.map_pos)
    #kills the player
    def death(self):
        self.game.playing = False
        print("You Died")

    # def load_images(self):
    #     self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
    #                             self.spritesheet.get_image(32, 0, 32, 32)]
    #     for frame in self.standing_frames:
    #         frame.set_colorkey(BLACK)
    #     self.walk_frames_r = [self.spritesheet.get_image(678, 860, 120, 201),
    #                           self.spritesheet.get_image(692, 1458, 120, 207)]
    #     self.walk_frames_l = []
    #     for frame in self.walk_frames_r:
    #         frame.set_colorkey(BLACK)
    #         self.walk_frames_l.append(pg.transform.flip(frame, True, False))
    #     self.jump_frame = self.spritesheet.get_image(256, 0, 128, 128)
    #     self.jump_frame.set_colorkey(BLACK)
    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.walking:
    #         if now - self.last_update > 500:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.standing_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
    #     if self.jumping:
    #         bottom = self.rect.bottom
    #         self.image = self.jump_frame
    #         self.rect = self.image.get_rect()
    #         self.rect.bottom = bottom
    #collision for walls
    def collide_with_walls(self, group, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, group, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, group, False)
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
            #if its a medkit
            if str(hits[0].__class__.__name__) == "Medkit":
                self.health += randint(30,50)
                if self.health > 100:
                        self.health = 100


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
            #summon the sword
        if keys[pg.K_1]:
            if self.swordcooling == False:
                if self.Psheathed == True:
                    self.sword = Sword(self.game, self.map_pos)
                    self.Psheathed = False
                    #makes it so you dont accidently instantly delete the sword
                    self.swordcooling = True
                    self.game.cooldown.cd = 3
                    print("Sword has been summoned")
            if self.swordcooling == False:
                if self.Psheathed == False:
                    self.sword.kill()
                    self.Psheathed = True
                    #makes it so you dont accidently instantly resummon the sword
                    self.swordcooling = True
                    self.game.cooldown.cd = 3
                    print("sword has been deleted")
                    self.hands = Hands(self.game, self.map_pos)
    

    #updates everything for the player(everything that gets repeated goes here)
    def update(self):
        self.get_keys()
        #self.animate()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls(self.game.walls, 'x')
        self.rect.y = self.y
        self.collide_with_walls(self.game.walls, 'y')   
        self.collide_with_group(self.game.coins,True)
        self.collide_with_group(self.game.medkits, True)
        #self.mapx += -self.vx *self.game.dt
        #self.mapy += -self.vy *self.game.dt
        #self.map_pos = (self.mapx,self.mapy)
        self.map_pos = (width/2 - 32 - self.x, height/2 - 32 - self.y)
        #makes it so you always either have hands or sword
        if self.Psheathed == False:
            self.Ssheathed = True
            self.handsaway = True
            self.hands.pickup(None)
            self.hands.kill()
        if self.Ssheathed == False:
            self.Psheatehed = True
            self.handsaway = True
            self.hands.pickup(None)
            self.hands.kill()
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
    def __init__(self,game, pos, img):
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.originalimage = img
        self.image = img
        self.rect = self.image.get_rect()
        self.x, self.y = pos
    #modified from chatgpt
    def point_atmouse(self, distance, offset):
        # Get mouse position
        mousemap = pg.mouse.get_pos()
        p1screen = self.game.map_to_screen()
        # Calculate angle between player and mouse
        dx = mousemap[0] - p1screen[0]
        dy = mousemap[1] - p1screen[1]
        self.angle = atan2(dy, dx)
        if self.angle < 0:
            self.angle += 2 * pi
        # Rotate the sword image based on the angle
        self.image = pg.transform.rotate(self.originalimage, -degrees(self.angle)-90)
        # Calculate sword position relative to the player
        self.xrel = (cos(self.angle)) * distance
        self.yrel = (sin(self.angle)) * distance
        # if self.angle >= pi / 2 and self.angle < pi:
        #     # Second quadrant
        #     self.xrel = abs(self.xrel)
        # elif self.angle >= pi and self.angle < pi * 3 / 2:
        #     # Third quadrant
        #     self.xrel = abs(self.xrel)
        #     self.yrel = -abs(self.yrel)
        # else:
        #     # Fourth quadrant
        #     self.yrel = -abs(self.yrel)
        # Set sword position
        self.x = ((self.game.p1.rect.x) + self.xrel) + offset
        self.y = ((self.game.p1.rect.y) + self.yrel) + offset
#creates a sword(now very simple)
class Sword(Weapon):
    def __init__(self, game, map_pos):
        self.groups = game.all_sprites, game.weapons
        self.game = game
        super().__init__(self.game, map_pos, self.game.sword_img)
    #updates the sword
    def update(self):
        super().point_atmouse(32, -5)
        self.rect.x = self.x
        self.rect.y = self.y
#creates hands(not very simple)
class Hands(Weapon):
    def __init__(self, game, map_pos):
        self.groups = game.all_sprites, game.weapons
        self.game = game
        super().__init__(self.game, map_pos, self.game.hands_img)
        self.pickupcooling = False
        self.holding = False
        self.grabbed_item = None
        self.spinning = False
        self.spin_acceleration = 0.001
        self.max_spin_speed = 2
        self.spincooling = False
        self.spacedown = False
        self.spin_speed = 0
        self.angular_velocity = 0  # Variable to track the angular velocity of the rotation
        self.previous_angle = 0
        self.throwing = False  # Flag to track if the item is being thrown
        self.throw_speed = 0  # Speed of the throw
        self.throw_decceleration = 0.05  # decceleration of the throw
        self.starttime = 0
    def pickup(self, obj):
        #if holding an item
        if self.grabbed_item: 
            self.grabbed_item.grabbed = False
            self.grabbed_item = None
            self.holding = False
        if obj:
            self.obj = obj
            self.obj.grabbed = True
            self.obj.spinning = False
            self.obj.thrown = False
            self.holding = True
            self.grabbed_item = obj
        
    # def spin(self):
    #     self.spinning = True
    #     self.spin_speed = 0.2  # Initial rotation speed
    #     self.obj.spinning = True
    def release(self):
        #if self.spinning:
            #self.throw_speed = self.spin_speed  # Set initial throw speed
            #self.obj.spinning = False
            #self.obj.throwinit = True
            self.starttime = self.game.cooldown.current_time
            self.obj.thrown = True
            self.obj.x = self.x
            self.obj.y = self.y
            self.obj.grabbed = False
            self.obj.velocitychange = True
            self.grabbed_item = None
            self.holding = False
            self.throwing = True
            #self.spinning = False
            #self.obj.throwinit = False
         

    #updates the hands
    def update(self):
        #modified from chatgpt
        if not self.spinning:
            super().point_atmouse(27, 0)
        #current_angle = degrees(self.angle)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
        #     self.spacedown = True
        #     if self.holding:  # Spin with item if spacebar is pressed while holding it
        #         if not self.spinning:
        #             self.spin()
        # else:
            #self.spacedown = False
            #if self.spinning:  # Release item if spacebar is released while holding it
            if self.holding:
                self.release()
        mouse_click = pg.mouse.get_pressed()[0]
        if mouse_click == 1:  # Left click
            if self.pickupcooling == False:
                if not self.holding:  # If hands are not holding an item
                    for item in self.game.picksprites:
                        if pg.sprite.collide_rect(self, item):
                            self.pickup(item)
                            self.pickupcooling = True 
                            self.game.cooldown.cd = 1.3
                            break
                elif self.grabbed_item:  # If hands are holding an item
                    self.pickup(None)  # Release the item
                    self.game.cooldown.cd = 1.3
                    self.pickupcooling = True
        # if self.spinning:
        #     self.spin_speed += self.spin_acceleration  # Increase spin speed
        #     if self.spin_speed > self.max_spin_speed:
        #         self.spin_speed = self.max_spin_speed  # Cap spin speed
        #     self.angle += self.spin_speed  # Update player's angle
        #     self.x = ((self.game.p1.rect.x) + (cos(self.angle) * 27))
        #     self.y = ((self.game.p1.rect.y) + (sin(self.angle) * 27))
        #     self.image = pg.transform.rotate(self.originalimage, -degrees(self.angle)-90)
        self.rect.x = self.x
        self.rect.y = self.y
        if self.game.cooldown.cd < 1:
            self.pickupcooling = False
        # # Calculate the angular velocity
        # self.angular_velocity = current_angle - self.previous_angle
        # # Store the current angle for the next update cycle
        # self.previous_angle = current_angle

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
#creates walls
class SecretWall(pg.sprite.Sprite):
    #everything in init follows the same structure as Player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.secrets, game.np_sprites
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
        self.groups = game.all_sprites, game.coins, game.picksprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.originalimage = game.coin_img
        self.image = self.originalimage
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
        self.grabbed = False
    def update(self):
        if self.grabbed:
            # Apply the effect of being grabbed
            self.image = pg.transform.rotate(self.originalimage, -degrees(self.game.p1.hands.angle)-90)
            self.rect.x = self.game.p1.hands.x + cos(self.game.p1.hands.angle) * 32
            self.rect.y = self.game.p1.hands.y + sin(self.game.p1.hands.angle) * 32
#creates coins
class Medkit(pg.sprite.Sprite):
    #and here
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.medkits, game.picksprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.originalimage = game.medkit_img
        self.image = self.originalimage
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
        self.grabbed = False
    def update(self):
        if self.grabbed:
            # Apply the effect of being grabbed
            self.image = pg.transform.rotate(self.originalimage, -degrees(self.game.p1.hands.angle)-90)
            self.rect.x = self.game.p1.rect.x + cos(self.game.p1.hands.angle) * 32
            self.rect.y = self.game.p1.rect.y + sin(self.game.p1.hands.angle) * 32
#creates powerups
class PowerUp(pg.sprite.Sprite):
    #anddd here
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups, game.picksprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.originalimage = game.powerups_img
        self.image = self.originalimage
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
        self.grabbed = False
    def update(self):
        if self.grabbed:
            # Apply the effect of being grabbed
            self.image = pg.transform.rotate(self.originalimage, -degrees(self.game.p1.hands.angle)-90)
            self.rect.x = self.game.p1.hands.x + cos(self.game.p1.hands.angle) * 32
            self.rect.y = self.game.p1.hands.y + sin(self.game.p1.hands.angle) * 32
#creates boxes
class Box(pg.sprite.Sprite):
    #here too
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boxes, game.picksprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.originalimage = game.box_img
        self.image = self.originalimage
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
        self.vx, self.vy = 0,0
        self.grabbed = False
        self.thrown = False
        self.decelerationfactor = 3
        self.cooldown = Timer(game)
        self.angle = 0
        self.spinning = False
        self.velocitychange = False
        self.movement = 0
        self.px =0
        self.py =0
        self.deceleration = 0
        self.throwinit = False
        self.timesincethrow = 0
        self.deceleration = 1
        self.xfactor = 1
        self.yfactor = 1
        self.xcooling = False
        self.ycooling = False
        #inverts vx and vy depending on what side of the wall the box collides with
    def collide_with_group(self, group, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, group, False)
            if hits:
                dx = self.rect.centerx - hits[0].rect.centerx
                if dx > 0:
                # Colliding on the right side of the wall
                    self.xfactor *=-1
                    print("right")
                    self.xcooling = True
                    self.game.cooldown.cd=1.1
                else:
                    # Colliding on the left side of the wall
                    self.xfactor *=-1
                    print("left")
                    self.xcooling = True
                    self.game.cooldown.cd=1.1
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, group, False)
            if hits:
                dy = self.rect.centery - hits[0].rect.centery
                if dy < 0:
                # Colliding on the bottom side of the wall
                    self.yfactor *=-1
                    print("bottom")
                    self.ycooling = True
                    self.cooldown.cd=1.1
                else:
                    # Colliding on the top side of the wall
                    self.yfactor *=-1
                    print("top")
                    self.ycooling = True
                    self.cooldown.cd=1.1
    #modified from chatgpt
    # def collide_with_group(self, group, kill):
    #     hits = pg.sprite.spritecollide(self, group, kill)
    #     if hits:
    #         wall = hits[0]
    #         # Check if the object's rect collides with the wall's rect
    #         if self.rect.colliderect(wall.rect):
    #             # Determine the direction of collision
    #             dx = self.rect.centerx - wall.rect.centerx
    #             dy = self.rect.centery - wall.rect.centery
            
    #             # Check if the collision is more horizontal or vertical
    #             if abs(dx) > abs(dy):
    #                 if not self.xcooling:
    #                     # Colliding horizontally
    #                     if dx > 0:
    #                         # Colliding on the right side of the wall
    #                         self.xfactor *=-1
    #                         print("right")
    #                         self.xcooling = True
    #                         self.game.cooldown.cd=1.1
    #                     else:
    #                         # Colliding on the left side of the wall
    #                         self.xfactor *=-1
    #                         print("left")
    #                         self.xcooling = True
    #                         self.game.cooldown.cd=1.1
    #             if abs(dy) > abs(dx):
    #                 if not self.ycooling:
    #                     # Colliding vertically
    #                     if dy < 0:
    #                         # Colliding on the bottom side of the wall
    #                         self.yfactor*=-1
    #                         print("bottom")
    #                         self.ycooling = True
    #                         self.cooldown.cd=1.1
    #                     else:
    #                         # Colliding on the top side of the wall
    #                         self.yfactor*=-1
    #                         print("top")
    #                         self.ycooling = True
    #                         self.cooldown.cd=1.1
                # if self.rect.left < wall.rect.right:
                #     self.xfactor *= -1
                #     print("Collided with wallrightside")
                #     print(self.xfactor)
                # if self.rect.right > wall.rect.left:
                #     self.xfactor *= -1
                #     print("Collided with wallleftside")
                # if self.rect.top < wall.rect.bottom:
                #     self.yfactor *= -1
                #     print("Collided with wallbottomside")
                # if self.rect.bottom > wall.rect.top:
                #     self.yfactor *= -1
                #     print("Collided with walltopside")
                
                # if self.vx > self.vy:
                #     self.xfactor*=-1
                # if self.vy > self.vx:
                #     self.yfactor*=-1
                # if self.vx == self.vy:
                #     self.xfactor*=-1
                #     self.yfactor*=-1
    #updates
    def update(self):
        if self.grabbed:
            # Apply the effect of being grabbed
            self.angle = self.game.p1.hands.angle
            self.image = pg.transform.rotate(self.originalimage, -degrees(self.angle)-90)
            self.rect.x = self.game.p1.hands.x + cos(self.angle) * 13
            self.rect.y = self.game.p1.hands.y + sin(self.angle) * 13
        # if self.spinning:
        #     self.svx = self.x - self.px
        #     self.svy = self.y - self.py
        #     self.px = self.x
        #     self.py = self.y
        #     print(self.svx)
        #     print(self.svy)
        # if self.throwinit:
        #     self.x = self.px
        #     self.y = self.py
        if self.thrown:
            if self.velocitychange:
                self.vx = (500*cos(self.angle))*(self.deceleration)*self.xfactor
                self.vy = (500*sin(self.angle))*(self.deceleration)*self.yfactor
                print (self.xfactor)
                print (self.yfactor)
            self.x += self.vx *self.game.dt
            self.y += self.vy *self.game.dt
            
            self.movement = abs(self.vx) + abs(self.vy)
        #     self.anglechange = 0.2 * (1 - (self.deceleration))
            if self.movement < 10:
        #         self.anglechange = 0
                self.vx = 0
                self.vy = 0
        #         self.velocitychange = False
                self.thrown = False
                self.deceleration = 1
            if self.game.cooldown.cd < 1:
                self.xcooling = False
            if self.cooldown.cd < 1:
                self.ycooling = False
            self.deceleration -= self.decelerationfactor*0.01
            if self.deceleration <=0:
                self.deceleration = 0
            if not self.xcooling:
                self.collide_with_group(self.game.walls,'x')
            if not self.ycooling:
                self.collide_with_group(self.game.walls,'y')
            self.rect.x = self.x
            self.rect.y = self.y
        #     if self.velocitychange:
        #         self.vx =  50* (1-(self.deceleration))
        #         self.vy =  50* (1-(self.deceleration))
        #         # self.vx = 500
        #         # self.vy = 500
        #     if self.deceleration >= 1:
        #         self.deceleration = 1
        #     self.x += self.vx *self.game.dt
        #     self.y += self.vy *self.game.dt
            
        #     self.angle += self.anglechange
        #     self.image = pg.transform.rotate(self.originalimage, -degrees(self.angle)-90)
        #     print (self.vx)
        #     print (self.vy)
        #     self.rect.x = self.x
        #     self.rect.y = self.y
        if not self.thrown:
            self.xfactor = 1
            self.yfactor = 1
        #     self.game.p1.hands.starttime = 0

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
        self.x = x*tilesize
        self.y = y*tilesize
        self.pos = vec(x, y) * tilesize
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = 150
        self.hp = 100
        self.cooldown = Timer(game)
        self.cooling = False
        self.knockbackcooling = False
        self.imagecooling = 0
    #collides with sprites
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Sword":
                choices = (1.075,1.1,1.125)
                self.hp -= 34
                self.speed = -1500
                self.cooling = True
                self.game.cooldown.cd = 2
                self.cooldown.cd = choices[randint(0,2)]
                self.knockbackcooling = True
                print("The enemy took damage")
            if str(hits[0].__class__.__name__) == "Hands":
                choices = (1.075,1.1,1.125)
                self.hp -= 20
                self.speed = -750
                self.cooling = True
                self.game.cooldown.cd = 2
                self.cooldown.cd = choices[randint(0,2)]
                self.knockbackcooling = True
                print("The enemy took damage")
            if str(hits[0].__class__.__name__) == "Box":
                if hits[0].grabbed:
                    choices = (1.075,1.1,1.125)
                    self.hp -= 25
                    self.speed = -500
                    self.cooling = True
                    self.game.cooldown.cd = 2
                    self.cooldown.cd = choices[randint(0,2)]
                    self.knockbackcooling = True
                    print("The enemy took damage")
                if hits[0].thrown:
                    choices = (1.075,1.1,1.125)
                    self.hp -= 50
                    self.speed = -2000
                    self.cooling = True
                    self.game.cooldown.cd = 2
                    self.cooldown.cd = choices[randint(0,2)]
                    self.knockbackcooling = True
                    print("The enemy took damage")
    #moves toward the player and collides with walls deathblocks and safewalls
    def update(self):
        self.cooldown.ticking()
        #if abs(self.game.p1.rect.x - self.x)*32 < 5:
        #    if abs(self.game.p1.rect.y - self.y)*32 < 5:
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
        if self.cooldown.cd < 1:
            self.knockbackcooling = False
        if not self.cooling:
            self.collide_with_group(self.game.weapons, False)
            self.collide_with_group(self.game.picksprites, False)
        if not self.knockbackcooling:
            self.speed = 150
        collide_with_walls(self, self.game.boxes, 'x')
        collide_with_walls(self, self.game.boxes, 'y')
        #kills it
        if self.hp <= 0:
            self.kill()
            self.game.p1.moneybag += 2
            self.game.p1.kills += 1
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
        self.hp = 1000
        self.cooldown = Timer(game)
        self.cooling = False
        self.knockbackcooling = False
        self.knockbacktime = 0
        self.imagecooling = 0
    #collides with sprites
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Sword":
                choices = (1.075,1.1,1.125)
                self.hp -= 34
                self.speed = -1000
                self.cooling = True
                self.game.cooldown.cd = 2
                self.cooldown.cd = choices[randint(0,2)]
                self.knockbackcooling = True
                print("The enemy took damage")
            if str(hits[0].__class__.__name__) == "Hands":
                choices = (1.075,1.1,1.125)
                self.hp -= 20
                self.speed = -500
                self.cooling = True
                self.game.cooldown.cd = 2
                self.cooldown.cd = choices[randint(0,2)]
                self.knockbackcooling = True
                print("The enemy took damage")
            if str(hits[0].__class__.__name__) == "Box":
                if hits[0].grabbed:
                    choices = (1.075,1.1,1.125)
                    self.hp -= 25
                    self.speed = -500
                    self.cooling = True
                    self.game.cooldown.cd = 2
                    self.cooldown.cd = choices[randint(0,2)]
                    self.knockbackcooling = True
                    print("The enemy took damage")
                if hits[0].thrown:
                    choices = (1.075,1.1,1.125)
                    self.hp -= 50
                    self.speed = -2000
                    self.cooling = True
                    self.game.cooldown.cd = 2
                    self.cooldown.cd = choices[randint(0,2)]
                    self.knockbackcooling = True
                    print("The enemy took damage")
    #moves toward the player and collides with walls deathblocks and safewalls
    def update(self):
        self.cooldown.ticking()
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
        if self.cooldown.cd < 1:
            self.knockbackcooling = False
        if not self.cooling:
            self.collide_with_group(self.game.weapons, False)
            self.collide_with_group(self.game.picksprites, False)
        if not self.knockbackcooling:
            self.speed = 100
        #kills it
        collide_with_walls(self, self.game.boxes, 'x')
        collide_with_walls(self, self.game.boxes, 'y')
        if self.hp <= 0:
            self.kill()
            self.game.p1.moneybag += 20
            self.game.p1.kills += 10
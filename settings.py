from os import path
#base stuff
width, height = 1024, 768
tilesize = 32
PLAYER_SPEED = 300
Powerupeffects = ["speed", "invincibility"]
#colors
BGCOLOR = ((40,81,39))
WHITE = ((255,255,255))
GREEN = ((0,255,0))
LIGHTGREY = ((217,217,214))
AQUA = ((0,255,255))
YELLOW = ((242, 210, 66))
RED = ((255,0,0))
PURPLE =((255,0,255))
BLACK = ((0,0,0))
#sets the FPS
FPS = 60
#stuff for spritesheets
dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')
P1SPRITESHEET = 'theBell.png'
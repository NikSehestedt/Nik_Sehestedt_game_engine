#this file was created by Nik Sehestedt
#period 4 is the best

'''
Beta goal:
Pick stuff up
Gameplay goal:
better combat system, knockback and all
'''
#imports the libraries
import pygame
from settings import *
from sprites import *
import sys
from random import randint
from os import path
from math import *
from utils import *


#draws health bar
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 320
    BAR_HEIGHT = 50
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

#Creates a game and a screen to put the game on
class Game:

    #initializes the game
    def __init__(self):
        pygame.init()

        #creates the screen
        self.screen = pygame.display.set_mode((width, height))
        #sets the screen caption
        pygame.display.set_caption("My Video Game")

        #sets a clock for the future
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,100)
        self.running = True
        #loads the data
        self.load_data()

    #keeps the data to be used
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        #all of the textures are set here
        self.player_img = pygame.image.load(path.join(img_folder, 'Playernew.png')).convert_alpha()
        self.sword_img = pygame.image.load(path.join(img_folder, 'Swordnew.png')).convert_alpha()
        self.invcplayer_img = pygame.image.load(path.join(img_folder, 'invc.png')).convert_alpha()
        self.deathblock_img = pygame.image.load(path.join(img_folder, 'Lava.png')).convert_alpha()
        self.enemy_img = pygame.image.load(path.join(img_folder, 'enemy.png')).convert_alpha()
        #self.wall_img = pygame.image.load(path.join(img_folder, 'Johnson.png')).convert_alpha()
        self.powerups_img = pygame.image.load(path.join(img_folder, 'Speedup.png')).convert_alpha()
        self.coin_img = pygame.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()
        self.safe_img = pygame.image.load(path.join(img_folder, 'Safezone.png')).convert_alpha()
        self.boss_img = pygame.image.load(path.join(img_folder, 'boss.png')).convert_alpha()
        self.medkit_img = pygame.image.load(path.join(img_folder, 'medkit.png')).convert_alpha()
        self.hands_img = pygame.image.load(path.join(img_folder, 'Hands.png')).convert_alpha()
        self.box_img = pygame.image.load(path.join(img_folder, 'Box.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        #sorts through the map
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    #puts our sprites in Game
    def new(self):
        self.cooldown = Timer(self)
        #puts the sprite groups to variables
        self.all_sprites = pygame.sprite.Group()
        self.np_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.deathblocks = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.safewalls = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.secrets = pygame.sprite.Group()
        self.medkits = pygame.sprite.Group()
        self.picksprites = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        #makes the map
        self.mapx = len(self.map_data[0])*32
        self.mapy = len(self.map_data)*32
        self.map = pygame.Surface(((len(self.map_data[0])-1)*32,len(self.map_data)*32))
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                #makes walls on the screen
                if tile == '1':
                    Wall(self, col, row)
                #makes the player
                if tile == 'p':
                    #finds the players starting coordinates
                    self.p1col = col
                    self.p1row = row
                    self.p1 = Player(self, self.p1col, self.p1row)
                #makes the deathblocks
                if tile == 'd':
                    Deathblock(self, col, row)
                #makes coins
                if tile == 'C':
                    Coin(self, col, row)
                #makes powerups
                if tile == 'P':
                    PowerUp(self, col, row)
                #makes enemies
                if tile == 'M':
                    Enemy(self, col, row)
                #makes safespaces
                if tile == 'S':
                    Safespace(self, col, row)
                #makes bosses
                if tile == 'B':
                    Boss(self, col, row)
                #makes secretwalls
                if tile == 'V':
                    SecretWall(self, col, row)
                #makes medkits
                if tile == 'H':
                    Medkit(self, col, row)
                if tile == 'O':
                    Box(self, col, row)
        #makes the UI

    

    #runs the game
    def run(self):
        #when the game is running
        self.playing = True
        while self.playing:
            #creates fps
            self.dt = self.clock.tick(FPS)/1000
            self.betterdt = floor(self.dt)
            #this is input
            self.events()
            #this is processing
            self.update()
            #this is output
            self.draw()
    #quits the game
    def quit(self):
        pygame.quit()
        sys.exit()    
    
    def input(self):
        pass
    #updates the sprites on the screen
    def update(self):
        self.all_sprites.update()
        self.cooldown.ticking()
       
    def map_to_screen(self):
        player_screen_x = self.p1.x + self.p1.map_pos[0] + 32
        player_screen_y = self.p1.y + self.p1.map_pos[1] + 32
        return player_screen_x, player_screen_y
    

        #draws text
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*tilesize,y*tilesize)
        surface.blit(text_surface, text_rect)
    #draws sprites, background color
    def draw(self):
        #makes background look like endless walls
        self.screen.fill(AQUA)
        #creates map on screen
        self.screen.blit(self.map,self.p1.map_pos)
        #puts background on map
        self.map.fill(BGCOLOR)
        #draws the spriteson the map
        self.all_sprites.draw(self.map)
        #puts the money count on the UI
        self.draw_text(self.screen, "Kills: "+str(self.p1.kills), 64, WHITE, 25, 1)
        self.draw_text(self.screen, str(self.p1.moneybag), 64, WHITE, 1,1)
        draw_health_bar(self.screen, 64, 704, self.p1.health)
        pygame.display.flip()

    def events(self):
    #runs if running is true, and sets running to false if pygame is quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        


    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

#assigns game to g
g = Game()
#g.show_start_screen
#calls the run function and the new function, running the game
while True:
    g.new()
    g.run()
    #g.show_go_screen()
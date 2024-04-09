#this file was created by Nik Sehestedt
#period 4 is the best

#imports the libraries
import pygame
from settings import *
from sprites import *
import sys
from random import randint
from os import path
from math import floor
from utils import *



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
        self.player_img = pygame.image.load(path.join(img_folder, 'Mario.png')).convert_alpha()
        self.sword_img = pygame.image.load(path.join(img_folder, 'Sword.png')).convert_alpha()
        self.sworddown_img = pygame.image.load(path.join(img_folder, 'Sworddown.png')).convert_alpha()
        self.swordleft_img = pygame.image.load(path.join(img_folder, 'Swordleft.png')).convert_alpha()
        self.swordright_img = pygame.image.load(path.join(img_folder, 'Swordright.png')).convert_alpha()
        self.invcplayer_img = pygame.image.load(path.join(img_folder, 'GoldMario.png')).convert_alpha()
        self.deathblock_img = pygame.image.load(path.join(img_folder, 'Lava.png')).convert_alpha()
        self.enemy_img = pygame.image.load(path.join(img_folder, 'Baldron.png')).convert_alpha()
        #self.wall_img = pygame.image.load(path.join(img_folder, 'Johnson.png')).convert_alpha()
        self.powerups_img = pygame.image.load(path.join(img_folder, 'Speedup.png')).convert_alpha()
        self.coin_img = pygame.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()
        self.safe_img = pygame.image.load(path.join(img_folder, 'Safezone.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        #sorts through the map
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
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
        #makes the map
        self.map = pygame.Surface((len(self.map_data[0])*32,len(self.map_data)*32))
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
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
        #self.p1.update()
        #movementcooldown = self.cooldown.countdown(0.1)
        #if movementcooldown == 0:
            #self.mobs.update()
        

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
        self.draw_text(self.screen, str(self.p1.moneybag), 64, white, 1,1)
        #creates map on screen
        self.screen.blit(self.map,self.p1.map_pos)
        #puts background on map
        self.map.fill(BGCOLOR)
        #draws the spriteson the map
        self.all_sprites.draw(self.map)
        #self.p1.render(self.screen)
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
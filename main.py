#this file was created by Nik Sehestedt
#imports the libraries
import pygame
from settings import *
from sprites import *
import sys
from random import randint
from os import path
#initializes pygame



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
        self.player_img = pygame.image.load(path.join(img_folder, 'Mario.png')).convert_alpha()
        self.deathblock_img = pygame.image.load(path.join(img_folder, 'Lava.png')).convert_alpha()
        self.enemy_img = pygame.image.load(path.join(img_folder, 'Baldron.png')).convert_alpha()
        #self.wall_img = pygame.image.load(path.join(img_folder, 'Johnson.png')).convert_alpha()
        self.powerups_img = pygame.image.load(path.join(img_folder, 'Speedup.png')).convert_alpha()
        self.coin_img = pygame.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()
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
        #puts the sprite group to a variable
        self.all_sprites = pygame.sprite.Group()
        #puts the walls to a variabale
        self.walls = pygame.sprite.Group()
        self.deathblocks = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        #puts the player to a variable
        #self.p1 = Player(self, 10, 10)
        #adds the player to the sprite group
        #self.all_sprites.add(self.p1)
        #runs through the map and creates the walls
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
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'M':
                    Enemy(self, col, row)
    

    #runs the game
    def run(self):
        #when the game is running
        self.playing = True
        while self.playing:
            #creates fps
            self.dt = self.clock.tick(FPS)/1000
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
        
#creates tiles on the screen
    def draw_grid(self):
        for x in range(0, width, tilesize):
            #draws horizontal lines
            pygame.draw.line(self.screen, LIGHTGREY,(x,0), (x, height))
        for y in range(0, height,tilesize):
            #draws vertical lines
            pygame.draw.line(self.screen, LIGHTGREY, (0,y), (width, y))

        #draws text
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*tilesize,y*tilesize)
        surface.blit(text_surface, text_rect)
    #draws sprites, background color, and calls the draw_grid function
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.p1.moneybag), 64, white, 1,1)
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
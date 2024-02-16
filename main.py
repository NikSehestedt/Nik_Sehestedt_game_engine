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
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
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
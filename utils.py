import pygame as pg

from math import floor

class Timer():
    # sets all properties to zero when instantiated...
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()
    # resets event time to zero - cooldown reset
    def get_countdown(self):
        return floor(self.cd)
    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt
    # def event_reset(self):
    #     self.event_time = floor((self.game.clock.)/1000)
    # sets current time
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
          
# # sets up file with multiple images...
# class Spritesheet:
#     # utility class for loading and parsing spritesheets
#     def __init__(self, filename):
#         self.spritesheet = pg.image.load(filename).convert()

#     def get_image(self, x, y, width, height):
#         # grab an image out of a larger spritesheet
#         image = pg.Surface((width, height))
#         image.blit(self.spritesheet, (0, 0), (x, y, width, height))
#         # image = pg.transform.scale(image, (width, height))
#         image = pg.transform.scale(image, (width * 4, height * 4))
#         return image
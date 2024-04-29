import pygame
import sys
from pygame.locals import *
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.can_move_vertically = False
        self.vertical_time_remaining = 0

    def update(self, keys):
        if keys[K_RIGHT]:
            self.rect.x += 5
            if self.rect.right > W:
                self.rect.right = W
        elif keys[K_LEFT]:
            self.rect.x -= 5
            if self.rect.left < 0:
                self.rect.left = 0
        elif keys[K_UP] and self.can_move_vertically:
            self.rect.y -= 5
            if self.rect.top < 0:
                self.rect.top = 0
        elif keys[K_DOWN] and self.can_move_vertically:
            self.rect.y += 5
            if self.rect.bottom > H:
                self.rect.bottom = H

        # Decrement vertical time remaining if player is allowed to move vertically
        if self.can_move_vertically:
            self.vertical_time_remaining -= 1
            if self.vertical_time_remaining <= 0:
                self.can_move_vertically = False

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, brick_type):
        super().__init__()
        self.brick_type = brick_type
        if brick_type == 0:  # Normal brick
            self.image = pygame.Surface((60, 20))
            self.image.fill((0, 255, 0))
        elif brick_type == 1:  # Brick spawns multiple balls
            self.image = pygame.Surface((60, 20))
            self.image.fill((255, 0, 0))
        elif brick_type == 2:  # Brick allows vertical movement for the player
            self.image = pygame.Surface((60, 20))
            self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = [3, -3]

    def update(self, walls, player, bricks):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Ball collision with walls
        if self.rect.left < walls.left or self.rect.right > walls.right:
            self.speed[0] = -self.speed[0]
        if self.rect.top < walls.top:
            self.speed[1] = -self.speed[1]

        # Ball collision with player
        if self.rect.colliderect(player.rect) and self.speed[1] > 0:
            self.speed[1] = -self.speed[1]

        # Ball collision with bricks
        brick_hit = pygame.sprite.spritecollideany(self, bricks)
        if brick_hit:
            if brick_hit.brick_type == 1:  # Brick spawns multiple balls
                for _ in range(3):
                    new_ball = Ball(self.rect.centerx, self.rect.centery)
                    balls.add(new_ball)
                    all_sprites.add(new_ball)
            elif brick_hit.brick_type == 2:  # Brick allows vertical movement for the player
                player.can_move_vertically = True
                player.vertical_time_remaining = 3000  # 3 seconds
            brick_hit.kill()
            self.speed[1] = -self.speed[1]

        # Ball goes off-screen at the bottom
        if self.rect.bottom > walls.bottom:
            self.kill()

pygame.init()

W, H = 640, 480
S_display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
balls = pygame.sprite.Group()
player = Player(W // 2, H - 20)

all_sprites.add(player)

# Create bricks
for x in range(10):
    for y in range(4):
        brick_type = random.choices([0, 0, 0, 1, 2], weights=[75, 5, 5, 5, 5])[0]  # 75% normal, 5% each special
        brick = Brick(x * 60 + 40, y * 30 + 60, brick_type)
        bricks.add(brick)
        all_sprites.add(brick)

# Add initial ball
initial_ball = Ball(W // 2, H // 2)
balls.add(initial_ball)
all_sprites.add(initial_ball)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player.update(keys)

    # Update vertical movement for the player if allowed
    if player.can_move_vertically:
        player.vertical_time_remaining -= 1
        if player.vertical_time_remaining <= 0:
            player.can_move_vertically = False

    # Update balls
    balls.update(S_display.get_rect(), player, bricks)

    S_display.fill((0, 0, 0))
    all_sprites.draw(S_display)
    pygame.display.flip()
    clock.tick(60)

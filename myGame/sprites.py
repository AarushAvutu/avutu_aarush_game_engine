# Import necessary modules from Pygame
import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import os

# Import constants and settings from external files
from settings import *

# Set up asset folders for images and sounds
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

# Player class inheriting from Sprite

class Player(Sprite):
    def __init__(self, game, l_control, r_control, jump_control, img_file):
        # Call the constructor of the Sprite class
        Sprite.__init__(self)
        
        # Store a reference to the Game instance and set up player attributes
        self.game = game
        self.img_file = img_file

        # Load player image and configure its properties
        self.image = pg.image.load(os.path.join(img_folder, self.img_file)).convert()
        self.image.set_colorkey(BLACK)
        
        # Set up player rectangle and initial position
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)

        # Set up player velocity, acceleration, and movement control configurations
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.canmove = True
        self.l_control = l_control
        self.r_control = r_control
        self.jump_control = jump_control

    def controls(self):
        # Handle player controls based on key presses
        keys = pg.key.get_pressed()
        if self.canmove:
            # Left movement control
            if keys[self.l_control]:
                self.acc.x = -5
                self.game.paused = False
            # Right movement control
            if keys[self.r_control]:
                self.acc.x = 5
            # Jump control
            if keys[self.jump_control]:
                self.jump()

    def jump(self):
        # Handle player jump when colliding with platforms or the ground
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        ghits = pg.sprite.collide_rect(self, self.game.ground)
        if hits or ghits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        # Update player position and apply controls

        # Set gravitational acceleration
        self.acc = vec(0, PLAYER_GRAV)

        # Handle player controls
        self.controls()

        # Apply friction
        self.acc.x += self.vel.x * -PLAYER_FRIC

        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Ensure player stays within the left boundary
        if self.rect.x <= 0:
            self.rect.x = 0

        # Update player rectangle position
        self.rect.midbottom = self.pos

        # Check collisions with mobs and update score
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if hits:
            self.game.score += 1


# Platform class inheriting from Sprite
class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        # Call the constructor of the Sprite class
        Sprite.__init__(self)
        # Configure platform properties
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5

    def update(self):
        # Update platform position, handling movement if category is "moving"
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

# Mob class inheriting from Sprite
#for later use
class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        # Call the constructor of the Sprite class
        Sprite.__init__(self)
        # Configure mob properties for later use
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)

    def update(self):
        # Update mob position to follow the player
        if self.rect.x < self.game.player.rect.x:
            self.rect.x += 1
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -= 1
        if self.rect.y < self.game.player.rect.y:
            self.rect.y += 1
        if self.rect.y > self.game.player.rect.y:
            self.rect.y -= 1

# new Powerup class inheriting from Sprite
class Powerup(Sprite):
    def __init__(self, x, y, category, img_file):
        # Call the constructor of the Sprite class
        Sprite.__init__(self)
        # Configure powerup properties
        self.img_file = img_file
        self.image = pg.image.load(os.path.join(img_folder, self.img_file)).convert()
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.x = x
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.y = y
        self.pos = vec(self.x, self.y)
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5

    def update(self):
        # Update powerup position, handling movement if category is "moving"
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

    def impact(self):
        # Check for collisions with other sprites
        hits = pg.sprite.spritecollide(self, self.game.all_sprites, False)
        if hits:
            if self.rect.y < hits[0].rect.y:
                self.vel.y = -PLAYER_JUMP



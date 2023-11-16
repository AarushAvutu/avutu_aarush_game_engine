
import pygame as pg
import random
import os
from settings import *
from sprites import *

vec = pg.math.Vector2

# Get the current directory and set folders for images and sounds
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # Initialize Pygame and game-specific attributes
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("A.A. Platformer")
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.scroll_speed = 5
        self.score = 0
        self.score2 = 0

    def new(self):
        # Set up a new game session
        self.camera = Camera(WIDTH, HEIGHT)
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.Powerups = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()

        # Create Player instances with their respective controls and images
        self.player = Player(self, pg.K_a, pg.K_d, pg.K_w, "theBell.png")
        self.player2 = Player(self, pg.K_LEFT, pg.K_RIGHT, pg.K_UP, "theBell.png")

        # Create a Powerup instance with a specific image and properties
        self.Powerup = Powerup(100, 10, "moving", "pineapple.png")

        # Add players, ground, and powerup to the sprite groups
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)
        self.ground = Platform(*GROUND)
        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.Powerup)
        new_platform = Platform(200, 400, 100, 10, "moving")
        new_Powerup = Powerup(100, 10, "moving", "pineapple.png")
        self.all_sprites.add(new_platform)
        self.all_platforms.add(new_platform)
        self.Powerups.add(self.Powerup)

        # Create the initial set of platforms from a predefined list
        for p in PLATFORM_LIST:
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
            self.all_platforms.add(plat)

        # Run the main game loop
        self.run()

    def run(self):
        # Main game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
                self.handle_powerup_collisions()
            self.draw()

    def update(self):
        # Update game elements
        self.all_sprites.update()

        # Scroll all sprites vertically to simulate upward movement
        for sprite in self.all_sprites:
            sprite.rect.y += self.scroll_speed

        # Create a new platform when the last one is about to leave the screen
        self.create_new_platform()
        self.create_new_powerup()

        # Check and handle collisions with powerups, scores, &Platforms for both players
        self.score_system()
        self.handle_powerup_collisions()
        self.plat_collisions()



    def plat_collisions(self):
         # Player 1 collisions with platforms and ground
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
        if hits:
            if self.player.vel.y > 0:
                # Land on the platform if falling
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
            elif self.player.vel.y < 0:
                # Bounce back if jumping into a platform
                self.player.vel.y = -self.player.vel.y

        # Handle collision with the ground for Player 1
        ghits = pg.sprite.collide_rect(self.player, self.ground)
        if ghits:
            # Land on the ground and apply cooldown logic
            self.player.pos.y = self.ground.rect.top
            self.player.vel.y = 0
            if self.player.cd.delta == 2:
                self.player.cd.event_reset()
                self.player.health -= 1

        # Player 2 collisions with platforms and ground
        hits = pg.sprite.spritecollide(self.player2, self.all_platforms, False)
        if hits:
            if self.player2.vel.y > 0:
                # Land on the platform if falling
                self.player2.pos.y = hits[0].rect.top
                self.player2.vel.y = 0

        # Handle collision with the ground for Player 2
        ghits = pg.sprite.collide_rect(self.player2, self.ground)
        if ghits:
            # Land on the ground
            self.player2.pos.y = self.ground.rect.top
            self.player2.vel.y = 0

            # Additional handling for Player 2 collisions
            if self.player2.vel.y > 0:
                hits = pg.sprite.spritecollide(self.player2, self.all_platforms, False)
                ghits = pg.sprite.collide_rect(self.player2, self.ground)
                if hits or ghits:
                    # Land on the platform if falling and increase horizontal velocity
                    self.player2.pos.y = hits[0].rect.top
                    self.player2.vel.y = 0
                    self.player2.vel.x = hits[0].speed * 1.5

    def score_system(self):
        # Check if players are in the camera range and increase the score if so
        if self.player.rect.colliderect(self.camera.rect):
            self.score += 1
        if self.player2.rect.colliderect(self.camera.rect):
            self.score2 += 1

        # End the game if a player reaches a score of 2200, 2200 to give time to see winner screen or if both players are bellow the screen
        if (self.player.rect.bottom > HEIGHT and self.player2.rect.bottom > HEIGHT):
            self.playing = False
            self.running = False
        #if one socre over 2000 or equal they win and displays win screen
        if self.score >= 2200:
            self.playing = False
            self.running = False
            '''pg.display.set_caption("P1 Win Screen")
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
            self.draw_text("P1 Wins! ", 50, BLUE, WIDTH/2, HEIGHT/6)
            pg.time.wait(10000)'''

        if self.score2 >= 2200:
            self.playing = False
            self.running = False
            '''pg.display.set_caption("P1 Win Screen")
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
            self.draw_text("P1 Wins! ", 50, BLUE, WIDTH/2, HEIGHT/6)
            pg.time.wait(10000)'''



    def events(self):
        # Handle Pygame events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Draw game elements on the screen
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Display scores and game rules on the screen
        self.draw_text("Score P2: " + str(self.score2), 22, WHITE, WIDTH/2, HEIGHT/10)
        self.draw_text("Score P1: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/14)
        self.draw_text("Winner is on screen for 2000 Tie if both under screen! P1:WASD P2:Arrows Pineapple +200", 16, WHITE, WIDTH/2, HEIGHT/22)

        # Display winner messages if the score reaches 1980
        if self.score >=2000:
            self.draw_text("P1 Wins", 40, BLUE, WIDTH/2, HEIGHT/8)
        if self.score2 >=2000:
            self.draw_text("P2 Wins", 40, BLUE, WIDTH/2, HEIGHT/8)
       
        pg.display.flip()


    def draw_text(self, text, size, color, x, y):
        # Helper function to draw text on the screen
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def create_new_platform(self):
        # Create a new platform when the last one is about to leave the screen
        last_platform = self.all_platforms.sprites()[-1]
        #if last plat is bellow screen adds new plat 
        if last_platform.rect.bottom < HEIGHT:

            new_platform = Platform(random.randint(50, WIDTH-50),
                                    last_platform.rect.y - random.randint(100, 150),
                                    100, 10, "moving")
            self.all_sprites.add(new_platform)
            self.all_platforms.add(new_platform)

    def create_new_powerup(self):
    # Create a new power-up when the last one is about to leave the screen
     last_powerup = self.Powerups.sprites()[-1]
    # Check if the last powerup is below the screen and add a new one
     if last_powerup.rect.bottom < HEIGHT:
        new_powerup = Powerup(random.randint(50, WIDTH-50),
                              last_powerup.rect.y - random.randint(500, 550),
                              "moving", "pineapple.png")
        self.all_sprites.add(new_powerup)
        self.Powerups.add(new_powerup)

    def handle_powerup_collisions(self):
        # Check and handle collisions between players and power-ups
        powerup_hits = pg.sprite.spritecollide(self.player, self.Powerups, True)
        powerup2_hits = pg.sprite.spritecollide(self.player2, self.Powerups, True)

        # Award points if a player collects a power-up
        if powerup_hits:
            self.score += 200

        if powerup2_hits:
            self.score2 += 200


#new class Camera
class Camera:
    def __init__(self, width, height):
        # Initialize the camera with the specified width and height
        self.width = width
        self.height = height
        # Create a Rect object representing the camera's position and size
        self.rect = pg.Rect(0, 0, self.width, self.height)

    def update(self, target):
        # Update the camera's position based on the target sprite's center
        # Offset the camera vertically to keep the target sprite centered
        offset_y = -(target.rect.centery - self.height // 2)
        for sprite in target.game.all_sprites:
            # Apply the vertical offset to all sprites to simulate scrolling
            sprite.rect.y += offset_y




# Create an instance of the Game class and start the game loop
g = Game()
while g.running:
    g.new()

pg.quit()

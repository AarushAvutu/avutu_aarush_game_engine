WIDTH = 700
HEIGHT = 800
FPS = 30

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

GROUND = (0, HEIGHT - 40, WIDTH, 40, "normal")
#list of platforms before starts generating new ones for scroll
PLATFORM_LIST = [
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"normal"),
                 (125, HEIGHT - 350, 100, 20, "moving"),
                 (222, 200, 100, 20, "normal"),
                 (175, 100, 80, 20, "normal")]


import pygame as py
import random

py.init()

clock = py.time.Clock()
FPS = 60

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("RPG Game")

TILE_SIZE = 50
ROWS = SCREEN_HEIGHT // TILE_SIZE
COLUMS = SCREEN_WIDTH // TILE_SIZE

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED = ( 173, 5, 5)
BLUE = (26, 0, 196)
GREEN = (28, 181, 7)
PURPLE = (133, 3, 150)

# Variables


# Sprites
player_idle = py.transform.scale(py.image.load('./sprites/player/player_idle.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))


# Classes
class Player():

    def __init__(self) -> None:
        self.pos_y = 0
        self.pos_x = 0
        self.speed = 5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        
    
    def draw(self):
        screen.blit(player_idle, (SCREEN_WIDTH // 2 - player_idle.get_width() // 2, SCREEN_HEIGHT // 2 - player_idle.get_height() // 2))

    def direction(self):
        if event.key == py.K_w:
            self.up = True
        if event.key == py.K_s:
            self.down = True
        if event.key == py.K_a:
            self.left = True
        if event.key == py.K_d:
            self.right = True

    def move(self):
        if self.up:
            self.pos_y -= self.speed
        if self.down:
            self.pos_y += self.speed
        if self.left:
            self.pos_x -= self.speed
        if self.right:
            self.pos_x += self.speed

# Functions
def draw_screen():
    screen.fill(GREEN)
    

# Generated Variables
player = Player()



running = True
while running:

    clock.tick(FPS)

    draw_screen()
    player.draw()

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        if event.type == py.KEYDOWN:
            player.direction()

    player.move()

    py.display.update()
    
py.quit()
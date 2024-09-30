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
COLUMNS = SCREEN_WIDTH // TILE_SIZE
MAP_SCALE = 3

# UP, LEFT, DOWN, RIGHT
MAP_BORDER = [ TILE_SIZE * COLUMNS // 2 * - 1, TILE_SIZE * ROWS // 2 * - 1, (TILE_SIZE * COLUMNS // 2 * - 1) + (TILE_SIZE * COLUMNS * MAP_SCALE), (TILE_SIZE * ROWS // 2 * - 1) + (TILE_SIZE * ROWS * MAP_SCALE)]

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED = ( 173, 5, 5)
BLUE = (26, 0, 196)
GREEN = (28, 181, 7)
PURPLE = (133, 3, 150)

# Variables


# Sprites
player_idle = py.transform.scale(py.image.load('./sprites/player/player_idle.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
bg_0 = py.transform.scale(py.image.load('./sprites/background/bg_0.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
bg_1 = py.transform.scale(py.image.load('./sprites/background/bg_1.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
bg_2 = py.transform.scale(py.image.load('./sprites/background/bg_2.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
bg_3 = py.transform.scale(py.image.load('./sprites/background/bg_3.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
bg_4 = py.transform.scale(py.image.load('./sprites/background/bg_4.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
bg_5 = py.transform.scale(py.image.load('./sprites/background/bg_5.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))

background = []

mapseed = []

# Classes
class Player():

    def __init__(self) -> None:
        self.pos_y_min = TILE_SIZE * COLUMNS // 2 * -1
        self.pos_x_min = TILE_SIZE * ROWS // 2 * -1
        self.pos_y = self.pos_y_min + SCREEN_HEIGHT // 2 * (MAP_SCALE - 1)
        self.pos_x = self.pos_x_min + SCREEN_WIDTH // 2 * (MAP_SCALE - 1)
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

    def stop_direction(self):
        if event.key == py.K_w:
            self.up = False
        if event.key == py.K_s:
            self.down = False
        if event.key == py.K_a:
            self.left = False
        if event.key == py.K_d:
            self.right = False

    def move(self):
        if self.up:
            if self.pos_y > self.pos_y_min * 2 + player_idle.get_height() // 2:
                self.pos_y -= self.speed
        if self.down:
            if self.pos_y < TILE_SIZE * ROWS * MAP_SCALE + self.pos_y_min * 2 - player_idle.get_height() // 2:
                self.pos_y += self.speed
        if self.left:
            if self.pos_x > self.pos_x_min * 2 + player_idle.get_width() // 2:
                self.pos_x -= self.speed
        if self.right:
            if self.pos_x < TILE_SIZE * COLUMNS * MAP_SCALE + self.pos_x_min * 2 - player_idle.get_width() // 2:
                self.pos_x += self.speed

    def reset(self):
        self.pos_y = self.pos_y_min + SCREEN_HEIGHT // 2 * (MAP_SCALE - 1)
        self.pos_x = self.pos_x_min + SCREEN_WIDTH // 2 * (MAP_SCALE - 1)

class Enemy():

    def __init__(self) -> None:
        self.x = random.randint(MAP_BORDER[1], MAP_BORDER[2])
        self.y = random.randint(MAP_BORDER[0], MAP_BORDER[3])
        self.spawn_x = self.x
        self.spawn_y = self.y
        self.aggro = False
        self.wandering = True
        self.wander_speed = 2
        self.aggro_speed = 4
        self.moving = False
        self.moving_x = False
        self.moving_y = False
        self.point = [self.x, self.y]
        self.speed = 4
        self.choice = 0
        self.wait = True
        self.max_wait_time = 100
        self.min_wait_time = 10
        self.wait_time = (self.max_wait_time + self.min_wait_time) // 2
        self.wander_range = 5 * TILE_SIZE
        self.aggro_range = 3 * TILE_SIZE
        self.aggro_distance = 10 * TILE_SIZE
    
    def draw(self):
        screen.blit(player_idle, (self.x - player.pos_x, self.y - player.pos_y))

    def pick_point(self):
        self.point = [self.spawn_x + random.randint(-self.wander_range, self.wander_range), self.spawn_y + random.randint(-self.wander_range, self.wander_range)]

    def check_aggro(self):
        if abs(self.x - player.pos_x - 350) < self.aggro_range and abs(self.y - player.pos_y - 350) < self.aggro_range:
            self.aggro = True
            self.wandering = False
        else:
            if self.aggro:
                self.pick_point()
            self.wandering = True
            self.aggro = False

    def move(self):
        #print(f"{self.point} \n {self.x}  {player.pos_x} \n {self.y}  {player.pos_y}")
        self.check_aggro()

        if self.wandering:
            self.speed = self.wander_speed
        if self.aggro:
            self.point = [player.pos_x - player_idle.get_width() // 2 + SCREEN_WIDTH // 2, player.pos_y - player_idle.get_height() // 2 + SCREEN_HEIGHT // 2]
            self.speed = self.aggro_speed
            self.moving = True

        if self.moving:

            if self.x > self.point[0] + self.speed and self.x > MAP_BORDER[1]:
                self.x -= self.speed
                self.moving_x = True
            elif self.x < self.point[0] - self.speed and self.x < MAP_BORDER[3] - player_idle.get_width():
                self.x += self.speed
                self.moving_x = True
            else:
                self.moving_x = False

            if self.y > self.point[1] + self.speed and self.y > MAP_BORDER[0]:
                self.y -= self.speed
                self.moving_y = True
            elif self.y < self.point[1] - self.speed and self.y < MAP_BORDER[2] - player_idle.get_height():
                self.y += self.speed
                self.moving_y = True
            else:
                self.moving_y = False
            
            if self.moving_x != True and self.moving_y != True:
                self.moving = False

        else:
            match self.choice:
                case 0:
                    if self.wait:
                        if self.wait_time > 0:
                            self.wait_time -= 1
                        else:
                            self.wait_time = random.randint(self.min_wait_time, self.max_wait_time)
                            self.wait = False
                    else:
                        #self.choice = random.randint(0, 1)
                        self.wait = True
                        self.pick_point()
                        self.moving = True
                        #self.choice = random.randint(0, 1)
                case 1:
                    pass


class Fighter(Enemy):
    def __init__(self) -> None:
        super().__init__()

    # def move(self):
    #     self.x = 700
    #     self.y = 700
    #     print(f"{self.point} \n {self.x}  {player.pos_x} \n {self.y}  {player.pos_y}")

# Functions
def bg_tile_chance():
    for x in range(50):
        background.append(bg_0)
    for x in range(5):
        background.append(bg_1)
        background.append(bg_2)
        background.append(bg_3)
        background.append(bg_4)
    background.append(bg_5)

def render_background():
    for y in range(ROWS * MAP_SCALE):
        for x in range(COLUMNS * MAP_SCALE):
            mapseed.append(background[random.randint(0, len(background) - 1)])

def draw_screen():
    screen.fill(GREEN)
    count = 0
    for y in range(ROWS * MAP_SCALE):
        for x in range(COLUMNS * MAP_SCALE):
            screen.blit(mapseed[count], (x * TILE_SIZE - player.pos_x + player.pos_x_min, y * TILE_SIZE - player.pos_y + player.pos_y_min))
            count += 1

def draw_grid():
    py.draw.line(screen, WHITE, (0 - player.pos_x_min - player.pos_x, 0 - player.pos_y_min - player.pos_y), (SCREEN_WIDTH - player.pos_x_min - player.pos_x, 0 - player.pos_y_min - player.pos_y))
    py.draw.line(screen, WHITE, (0 - player.pos_x_min - player.pos_x, 0 - player.pos_y_min - player.pos_y), (0 - player.pos_x_min - player.pos_x, SCREEN_HEIGHT - player.pos_y_min - player.pos_y))
    for x in range(MAP_SCALE):
        py.draw.line(screen, WHITE, (0 - player.pos_x_min - player.pos_x, SCREEN_HEIGHT * x - player.pos_y_min - player.pos_y), (SCREEN_WIDTH - player.pos_x_min - player.pos_x, SCREEN_HEIGHT * x - player.pos_y_min - player.pos_y))
        py.draw.line(screen, WHITE, (SCREEN_WIDTH * x - player.pos_x_min - player.pos_x, 0 - player.pos_y_min - player.pos_y), (SCREEN_WIDTH * x - player.pos_x_min - player.pos_x, SCREEN_HEIGHT - player.pos_y_min - player.pos_y))

def show_corners():
    py.draw.rect(screen, WHITE, (MAP_BORDER[1] - player.pos_x, MAP_BORDER[0] - player.pos_y, TILE_SIZE, TILE_SIZE))
    py.draw.rect(screen, WHITE, (MAP_BORDER[1] - player.pos_x, MAP_BORDER[2] - player.pos_y, TILE_SIZE, TILE_SIZE))
    py.draw.rect(screen, WHITE, (MAP_BORDER[3] - player.pos_x, MAP_BORDER[0] - player.pos_y, TILE_SIZE, TILE_SIZE))
    py.draw.rect(screen, WHITE, (MAP_BORDER[3] - player.pos_x, MAP_BORDER[2] - player.pos_y, TILE_SIZE, TILE_SIZE))

def gen_enemies():
    for i in range(5):
        enemies.append(Fighter())

# Generated Variables
player = Player()

enemies = []
gen_enemies()

bg_tile_chance()
render_background()


running = True
while running:

    clock.tick(FPS)

    draw_screen()
    player.draw()

    for enemy in enemies:
        enemy.draw()

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        if event.type == py.KEYDOWN:
            player.direction()

            if event.key == py.K_l:
                running = False

            if event.key == py.K_r:
                player.reset()
                mapseed = []
                enemies = []
                gen_enemies()
                render_background()
        
        if event.type == py.KEYUP:
            player.stop_direction()

    player.move()

    for enemy in enemies:
        enemy.move()

    py.display.update()
    
py.quit()
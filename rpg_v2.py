import pygame as py
import random
import math

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
MAP_SCALE = 1

# UP, LEFT, DOWN, RIGHT
MAP_BORDER = [ TILE_SIZE * COLUMNS // 2 * - 1 + 350, TILE_SIZE * ROWS // 2 * - 1 + 350, (TILE_SIZE * COLUMNS // 2 * - 1) + (TILE_SIZE * COLUMNS * MAP_SCALE) + 350, (TILE_SIZE * ROWS // 2 * - 1) + (TILE_SIZE * ROWS * MAP_SCALE) + 350]

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

    def __init__(self):
        self.cord = py.math.Vector2(( SCREEN_WIDTH // 2 * (MAP_SCALE - 1), SCREEN_HEIGHT // 2 * (MAP_SCALE - 1)))
        self.speed = 5
        self.dest = py.math.Vector2(self.cord[0], self.cord[1])
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

    def set_dest(self):
        if self.up:
            if self.dest[1] < MAP_BORDER[0] - 350:
                self.dest[1] = MAP_BORDER[0] - 350
            else:
                self.dest[1] -= self.speed
        if self.down:
            if self.dest[1] > MAP_BORDER[2] - 350:
                self.dest[1] = MAP_BORDER[2] - 350
            else:
                self.dest[1] += self.speed
        if self.left:
            if self.dest[0] < MAP_BORDER[1] - 350:
                self.dest[0] = MAP_BORDER[1] - 350
            else:
                self.dest[0] -= self.speed
        if self.right:
            if self.dest[0] > MAP_BORDER[3] - 350:
                self.dest[0] = MAP_BORDER[3] - 350
            else:
                self.dest[0] += self.speed

        if self.up == False and self.down == False:
            self.dest[1] = self.cord[1]
        if self.left == False and self.right == False:
            self.dest[0] = self.cord[0]

    def move(self):
        self.set_dest()

        self.move_cord = math.sqrt((self.cord[0] - self.dest[0]) ** 2 + (self.cord[1] - self.dest[1]) ** 2)
        if self.move_cord != 0 and self.move_cord > self.speed:
            self.cord[0] += self.speed * (self.dest[0] - self.cord[0]) / self.move_cord 
            self.cord[1] += self.speed * (self.dest[1] - self.cord[1]) / self.move_cord

    def reset(self):
        self.cord[1] = SCREEN_HEIGHT // 2 * (MAP_SCALE - 1)
        self.cord[0] = SCREEN_WIDTH // 2 * (MAP_SCALE - 1)
        self.dest = py.math.Vector2(self.cord[0], self.cord[1])

class Enemy():

    def __init__(self) -> None:
        self.base_sprite = player_idle
        self.cord = py.math.Vector2((random.randint(MAP_BORDER[1], MAP_BORDER[2] - self.base_sprite.get_width()), random.randint(MAP_BORDER[0], MAP_BORDER[3] - self.base_sprite.get_height())))
        self.spawn_x = self.cord[0]
        self.spawn_y = self.cord[1]
        self.aggro = False
        self.wandering = True
        self.wander_speed = 2
        self.aggro_speed = 3
        self.moving = False
        self.point = py.math.Vector2(self.cord[0], self.cord[1])
        self.speed = 4
        self.choice = 0
        self.wait = True
        self.max_wait_time = 150
        self.min_wait_time = 50
        self.wait_time = (self.max_wait_time + self.min_wait_time) // 2
        self.wander_range = 5 * TILE_SIZE
        self.aggro_range = 3 * TILE_SIZE
        self.aggro_distance = 5 * TILE_SIZE
        self.forget = False
        self.forget_timer_max = 100
        self.forget_timer = self.forget_timer_max
    
    def draw(self):
        screen.blit(self.base_sprite, (self.cord[0] - player.cord[0], self.cord[1] - player.cord[1]))

    def pick_point(self):
        self.point = py.math.Vector2(self.spawn_x + random.randint(-self.wander_range, self.wander_range), self.spawn_y + random.randint(-self.wander_range, self.wander_range))
        if self.point[1] < MAP_BORDER[0]:
            self.point[1] = MAP_BORDER[0]
            self.spawn_y = MAP_BORDER[0] + self.wander_range + TILE_SIZE
            
        elif self.point[1] > MAP_BORDER[2] - self.base_sprite.get_height():
            self.point[1] = MAP_BORDER[2] - self.base_sprite.get_height()
            self.spawn_y = MAP_BORDER[2] - self.wander_range - TILE_SIZE
            
        if self.point[0] < MAP_BORDER[1]:
            self.point[0] = MAP_BORDER[1]
            self.spawn_x = MAP_BORDER[1] + self.wander_range + TILE_SIZE
            
        elif self.point[0] > MAP_BORDER[3] - self.base_sprite.get_width():
            self.point[0] = MAP_BORDER[3] - self.base_sprite.get_width()
            self.spawn_x = MAP_BORDER[3] - self.wander_range - TILE_SIZE
            

    def check_aggro(self):
        if self.forget:
            if self.forget_timer > 0:
                self.forget_timer -= 1
            else:
                self.forget = False
        elif abs(self.cord[0] - player.cord[0] - 350) < self.aggro_range and abs(self.cord[1] - player.cord[1] - 350) < self.aggro_range:
            if math.sqrt((self.spawn_x - self.cord[0]) ** 2 + (self.spawn_y - self.cord[1]) ** 2) < self.aggro_distance:
                self.aggro = True
                self.wandering = False
            else:
                self.pick_point()
                self.aggro = False
                self.wandering = True
                self.forget = True
                self.forget_timer = self.forget_timer_max
        else:
            if self.aggro:
                self.pick_point()
            self.wandering = True
            self.aggro = False

    def move(self):
        # print(f"{self.point} \n {self.cord[0]}  {player.cord[0]} \n {self.cord[1]}  {player.cord[1]}")
        self.check_aggro()

        if self.wandering:
            self.speed = self.wander_speed
        if self.aggro:
            self.point = py.math.Vector2(player.cord[0] - player_idle.get_width() // 2 + SCREEN_WIDTH // 2, player.cord[1] - player_idle.get_height() // 2 + SCREEN_HEIGHT // 2)
            self.speed = self.aggro_speed
            self.moving = True

        if self.moving:
            
            self.move_cord = math.sqrt((self.cord[0] - self.point[0]) ** 2 + (self.cord[1] - self.point[1]) ** 2)
            if self.move_cord != 0 and self.move_cord > self.speed:
                self.cord[0] += self.speed * (self.point[0] - self.cord[0]) / self.move_cord 
                self.cord[1] += self.speed * (self.point[1] - self.cord[1]) / self.move_cord
            else:
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
        # self.aggro_distance = 0
        # self.aggro_range = 200 * TILE_SIZE

    # def move(self):
    #     self.cord[0] = 700
    #     self.cord[1] = 700
    #     print(f"{self.point} \n {self.cord[0]}  {player.cord[0]} \n {self.cord[1]}  {player.cord[1]}")

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
            screen.blit(mapseed[count], (x * TILE_SIZE - player.cord[0], y * TILE_SIZE - player.cord[1]))
            count += 1

def show_corners():
    py.draw.rect(screen, WHITE, (MAP_BORDER[1] - player.cord[0], MAP_BORDER[0] - player.cord[1], TILE_SIZE, TILE_SIZE))
    py.draw.rect(screen, WHITE, (MAP_BORDER[1] - player.cord[0], MAP_BORDER[2] - player.cord[1], TILE_SIZE, TILE_SIZE))
    py.draw.rect(screen, WHITE, (MAP_BORDER[3] - player.cord[0], MAP_BORDER[0] - player.cord[1], TILE_SIZE, TILE_SIZE))
    py.draw.rect(screen, WHITE, (MAP_BORDER[3] - player.cord[0], MAP_BORDER[2] - player.cord[1], TILE_SIZE, TILE_SIZE))

def gen_enemies():
    for i in range(10):
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
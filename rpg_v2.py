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
player_health = py.transform.scale(py.image.load('./sprites/player/player_health.png').convert_alpha(), (TILE_SIZE // 2, TILE_SIZE // 2))
skeleton_idle = py.transform.scale(py.image.load('./sprites/enemies/skeleton.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
skeleton_angry = py.transform.scale(py.image.load('./sprites/enemies/skeleton_angry.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
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
        self.type = "player"
        self.base_sprite = player_idle
        self.active_sprite = self.base_sprite
        self.cord = py.math.Vector2(( SCREEN_WIDTH // 2 * (MAP_SCALE - 1), SCREEN_HEIGHT // 2 * (MAP_SCALE - 1)))
        self.true_hitbox = py.rect.Rect(((SCREEN_WIDTH - self.base_sprite.get_width()) // 2, (SCREEN_HEIGHT - self.base_sprite.get_height()) // 2, self.base_sprite.get_width(), self.base_sprite.get_height()))
        self.hitbox = py.rect.Rect(0,0, int(self.base_sprite.get_width() * .50), int(self.base_sprite.get_height() * .50))
        self.hitbox.center = self.true_hitbox.center
        self.speed = 5
        self.dest = py.math.Vector2(self.cord[0], self.cord[1])
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.hp = 3
        self.dead = False
        
    def draw(self):
        screen.blit(self.active_sprite, (SCREEN_WIDTH // 2 - self.base_sprite.get_width() // 2, SCREEN_HEIGHT // 2 - self.base_sprite.get_height() // 2))

    def update_hitbox(self):
        self.true_hitbox = py.rect.Rect(((SCREEN_WIDTH - self.base_sprite.get_width()) // 2, (SCREEN_HEIGHT - self.base_sprite.get_height()) // 2, self.base_sprite.get_width(), self.base_sprite.get_height()))
        self.hitbox.center = self.true_hitbox.center
        if self.hp < 1:
            self.active_sprite = skeleton_idle
        else:
            self.active_sprite = player_idle

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
            if self.dest[1] < MAP_BORDER[0] - 350 + self.base_sprite.get_height() // 2:
                self.dest[1] = MAP_BORDER[0] - 350 + self.base_sprite.get_height() // 2
            else:
                self.dest[1] -= self.speed
        if self.down:
            if self.dest[1] > MAP_BORDER[2] - 350 - self.base_sprite.get_height() // 2:
                self.dest[1] = MAP_BORDER[2] - 350 - self.base_sprite.get_height() // 2
            else:
                self.dest[1] += self.speed
        if self.left:
            if self.dest[0] < MAP_BORDER[1] - 350 + self.base_sprite.get_width() // 2:
                self.dest[0] = MAP_BORDER[1] - 350 + self.base_sprite.get_width() // 2
            else:
                self.dest[0] -= self.speed
        if self.right:
            if self.dest[0] > MAP_BORDER[3] - 350 - self.base_sprite.get_width() // 2:
                self.dest[0] = MAP_BORDER[3] - 350 - self.base_sprite.get_width() // 2
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
        
        self.update_hitbox()

    def hit(self, dmg):

        if self.hp > dmg:
            self.hp -= dmg
            self.dead = False
            
        else:
            self.hp = 0
            self.dead = True

    def reset(self):
        self.cord[1] = SCREEN_HEIGHT // 2 * (MAP_SCALE - 1)
        self.cord[0] = SCREEN_WIDTH // 2 * (MAP_SCALE - 1)
        self.dest = py.math.Vector2(self.cord[0], self.cord[1])
        self.hp = 3
        self.dead = False

class Enemy():

    def __init__(self) -> None:
        self.type = "enemy"
        self.base_sprite = player_idle
        self.active_sprite = self.base_sprite
        self.cord = py.math.Vector2((random.randint(MAP_BORDER[1], MAP_BORDER[2] - self.base_sprite.get_width()), random.randint(MAP_BORDER[0], MAP_BORDER[3] - self.base_sprite.get_height())))
        self.hitbox = py.rect.Rect((self.cord[0] - player.cord[0], self.cord[1] - player.cord[1], self.base_sprite.get_width(), self.base_sprite.get_height()))
        self.friendly_hitbox = py.rect.Rect((0, 0, self.base_sprite.get_width() // 2, self.base_sprite.get_height() // 2))
        self.friendly_hitbox.center = self.hitbox.center
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
        self.stuned = False
        self.stun_time = 15
        self.stun_timer = self.stun_time
        self.wait_time = (self.max_wait_time + self.min_wait_time) // 2
        self.wander_range = 4 * TILE_SIZE
        self.aggro_range = 3 * TILE_SIZE
        self.aggro_distance = 5 * TILE_SIZE
        self.forget = False
        self.forget_timer_max = 30
        self.forget_timer = self.forget_timer_max
        self.flipped = False
        self.dead = False
        self.knockback = 10
        self.hp = 3
        self.dmg = 1
    
    def flip(self):
        if self.point[0] > self.cord[0] and self.flipped == False:
            self.active_sprite = py.transform.flip(self.active_sprite, True, False)
            self.flipped = True

        elif self.point[0] < self.cord[0] - self.speed:
            if self.flipped:
                self.active_sprite = py.transform.flip(self.active_sprite, True, False)
                self.flipped = False

    def draw(self):
        self.flip()
        screen.blit(self.active_sprite, (self.cord[0] - player.cord[0], self.cord[1] - player.cord[1]))

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
            
    def change_sprite(self, sprite):
        if self.flipped:
            self.active_sprite = py.transform.flip(sprite, True, False)
        else:
            self.active_sprite = sprite

    def check_collision(self, target, friendly = False):
        if target.type == "player":
            if self.hitbox.colliderect(player.hitbox):
                self.hit_player()
        elif target.type == "player_projectile":
            pass
        elif friendly:
            if self.friendly_hitbox.colliderect(target.friendly_hitbox):
                if target.hitbox[0] > self.friendly_hitbox[0]:
                    self.apply_force((self.cord[0] - abs(target.hitbox[0] - self.friendly_hitbox[0]), self.cord[1]), 1)

                if target.hitbox[0] < self.friendly_hitbox[0]:
                    self.apply_force((self.cord[0] + abs(target.hitbox[0] - self.friendly_hitbox[0]), self.cord[1]), 1)

                if target.hitbox[1] < self.friendly_hitbox[1]:
                    self.apply_force((self.cord[0], self.cord[1] + abs(target.hitbox[1] - self.friendly_hitbox[1])), 1)

                if target.hitbox[1] > self.friendly_hitbox[1]:
                    self.apply_force((self.cord[0], self.cord[1] - abs(target.hitbox[1] - self.friendly_hitbox[1])), 1)        
        else:
            if self.hitbox.colliderect(target.hitbox):
                if target.hitbox[0] > self.hitbox[0]:
                    self.apply_force((self.cord[0] - abs(target.hitbox[0] - self.hitbox[0]), self.cord[1]), 1)

                if target.hitbox[0] < self.hitbox[0]:
                    self.apply_force((self.cord[0] + abs(target.hitbox[0] - self.hitbox[0]), self.cord[1]), 1)

                if target.hitbox[1] < self.hitbox[1]:
                    self.apply_force((self.cord[0], self.cord[1] + abs(target.hitbox[1] - self.hitbox[1])), 1)

                if target.hitbox[1] > self.hitbox[1]:
                    self.apply_force((self.cord[0], self.cord[1] - abs(target.hitbox[1] - self.hitbox[1])), 1)            

    def hit_player(self):
        if player.hitbox[0] > self.hitbox[0]:
            self.apply_force((self.cord[0] - abs(player.hitbox[0] - self.hitbox[0]), self.cord[1]), self.knockback)

        if player.hitbox[0] < self.hitbox[0]:
            self.apply_force((self.cord[0] + abs(player.hitbox[0] - self.hitbox[0]), self.cord[1]), self.knockback)

        if player.hitbox[1] < self.hitbox[1]:
            self.apply_force((self.cord[0], self.cord[1] + abs(player.hitbox[1] - self.hitbox[1])), self.knockback)

        if player.hitbox[1] > self.hitbox[1]:
            self.apply_force((self.cord[0], self.cord[1] - abs(player.hitbox[1] - self.hitbox[1])), self.knockback)
        
        
        player.hit(self.dmg)
        self.hp -= 1
        if self.hp <= 0:
            self.dead = True
        self.stuned = True

    def update_hitbox(self):
        self.hitbox = py.rect.Rect((self.cord[0] - player.cord[0], self.cord[1] - player.cord[1], self.base_sprite.get_width(), self.base_sprite.get_height()))
        self.friendly_hitbox.center = self.hitbox.center
        self.check_collision(player)

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
                self.change_sprite(skeleton_angry)
            else:
                self.pick_point()
                self.aggro = False
                self.wandering = True
                self.forget = True
                self.forget_timer = self.forget_timer_max
                self.change_sprite(skeleton_idle)

        else:
            if self.aggro:
                self.pick_point()
                self.change_sprite(skeleton_idle)
            self.wandering = True
            self.aggro = False

    def apply_force(self, point, force):
        self.move_cord = math.sqrt((self.cord[0] - point[0]) ** 2 + (self.cord[1] - point[1]) ** 2)
        if self.move_cord != 0 and self.move_cord > self.speed:
            self.cord[0] += self.speed * force * (point[0] - self.cord[0]) / self.move_cord 
            self.cord[1] += self.speed * force * (point[1] - self.cord[1]) / self.move_cord

    def move(self):
        # print(f"{self.point} \n {self.cord[0]}  {player.cord[0]} \n {self.cord[1]}  {player.cord[1]}")
        self.check_aggro()

        if self.wandering:
            self.speed = self.wander_speed
        if self.aggro:
            self.point = py.math.Vector2(player.cord[0] - self.base_sprite.get_width() // 2 + SCREEN_WIDTH // 2, player.cord[1] - self.base_sprite.get_height() // 2 + SCREEN_HEIGHT // 2)
            self.speed = self.aggro_speed
            self.moving = True

        if self.stuned:
            if self.stun_timer > 0:
                self.point[0] = self.cord[0]
                self.point[1] = self.cord[1]
                self.stun_timer -= 1
            else:
                self.stuned = False
                self.stun_timer = self.stun_time

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
            
        self.update_hitbox()
    
    def death_action(self):
        for i in range(random.randint(0, 3)):
            ground_loot.append(Health((self.cord[0] + random.randint(0, TILE_SIZE), self.cord[1] + random.randint(0, TILE_SIZE))))

class Fighter(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.base_sprite = skeleton_idle
        self.active_sprite = self.base_sprite
        # self.aggro_distance = 100 * TILE_SIZE
        # self.aggro_range = 200 * TILE_SIZE

    # def move(self):
    #     self.cord[0] = 700
    #     self.cord[1] = 700
    #     print(f"{self.point} \n {self.cord[0]}  {player.cord[0]} \n {self.cord[1]}  {player.cord[1]}")

class Loot():
    def __init__(self) -> None:
        self.cord = py.math.Vector2(0, 0)
        self.delete = False
        self.base_sprite = player_idle
        self.active_sprite = self.base_sprite
        self.hitbox = py.rect.Rect((self.cord[0] - player.cord[0], self.cord[1] - player.cord[1], self.base_sprite.get_width(), self.base_sprite.get_height()))
        self.pickup_range = 2 * TILE_SIZE
        self.speed = 1
    
    def pickup_action(self):
        self.delete = True

    def pickup(self):
        
        if abs(self.cord[0] - player.cord[0] - 350) < self.pickup_range and abs(self.cord[1] - player.cord[1] - 350) < self.pickup_range:
            self.point = py.math.Vector2(player.cord[0] - self.base_sprite.get_width() // 2 + SCREEN_WIDTH // 2, player.cord[1] - self.base_sprite.get_height() // 2 + SCREEN_HEIGHT // 2)
            
            self.move_cord = math.sqrt((self.cord[0] - self.point[0]) ** 2 + (self.cord[1] - self.point[1]) ** 2)
            if self.move_cord != 0 and self.move_cord > self.speed:
                self.cord[0] += self.speed * (self.point[0] - self.cord[0]) / self.move_cord 
                self.cord[1] += self.speed * (self.point[1] - self.cord[1]) / self.move_cord

        if player.true_hitbox.colliderect(self.hitbox):
            self.pickup_action()

    def draw(self):
        screen.blit(self.active_sprite, (self.cord[0] - player.cord[0], self.cord[1] - player.cord[1]))

    def update(self):
        self.hitbox = py.rect.Rect((self.cord[0] - player.cord[0], self.cord[1] - player.cord[1], self.base_sprite.get_width(), self.base_sprite.get_height()))
        self.active_sprite = self.base_sprite
        self.pickup()
    
class Health(Loot):

    def __init__(self, cord = py.math.Vector2(0, 0)):
        super().__init__()
        self.cord = py.math.Vector2(cord)
        self.base_sprite = py.transform.scale(player_health, (player_health.get_width(), player_health.get_height()))
    
    def pickup_action(self):
        self.delete = True
        player.hp += 1

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

def draw_ui():
    if player.hp > 0:
        for i in range(player.hp):
            screen.blit(player_health, (SCREEN_WIDTH - int(player_health.get_width() * (i + 1) * 1.5), player_health.get_height()))
    else:
        pass

def gen_enemies():
    for i in range(1):
        enemies.append(Fighter())

# Generated Variables
player = Player()

ground_loot = []
enemies = []
gen_enemies()

bg_tile_chance()
render_background()


running = True
while running:

    clock.tick(FPS)

    draw_screen()
    player.draw()

    if len(ground_loot) > 0:
        for loot in ground_loot:
            loot.update()
            loot.draw()
            if loot.delete:
                ground_loot.remove(loot)

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
        for other_enemy in enemies:
            if other_enemy == enemy:
                break
            else:
                enemy.check_collision(other_enemy, True)

        if enemy.dead:
            enemy.death_action()
            enemies.remove(enemy)

    draw_ui()

    py.display.update()
    
py.quit()
import os
import random
import time
from os.path import join

import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()
WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
ENEMY_SCALE = 0.3
EXPLOSION_SCALE = 0.5
PURPLE_SPACE_SHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "enemy1_1.png")),
    (
        int(
            pygame.image.load(os.path.join("images", "enemy1_1.png")).get_width()
            * ENEMY_SCALE
        ),
        int(
            pygame.image.load(os.path.join("images", "enemy1_1.png")).get_height()
            * ENEMY_SCALE
        ),
    ),
)
BLUE_SPACE_SHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "enemy2_1.png")),
    (
        int(
            pygame.image.load(os.path.join("images", "enemy2_1.png")).get_width()
            * ENEMY_SCALE
        ),
        int(
            pygame.image.load(os.path.join("images", "enemy2_1.png")).get_height()
            * ENEMY_SCALE
        ),
    ),
)
GREEN_SPACE_SHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "enemy3_1.png")),
    (
        int(
            pygame.image.load(os.path.join("images", "enemy3_1.png")).get_width()
            * ENEMY_SCALE
        ),
        int(
            pygame.image.load(os.path.join("images", "enemy3_1.png")).get_height()
            * ENEMY_SCALE
        ),
    ),
)

MYSTERY_SHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "mystery.png")),
    (
        int(
            pygame.image.load(os.path.join("images", "mystery.png")).get_width()
            * ENEMY_SCALE
        ),
        int(
            pygame.image.load(os.path.join("images", "mystery.png")).get_height()
            * ENEMY_SCALE
        ),
    ),
)

# Explosion images
ENEMY_EXPLOSION_1 = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "explosionpurple.png")),
    (
        int(
            pygame.image.load(os.path.join("images", "explosionpurple.png")).get_width()
            * EXPLOSION_SCALE
        ),
        int(
            pygame.image.load(
                os.path.join("images", "explosionpurple.png")
            ).get_height()
            * EXPLOSION_SCALE
        ),
    ),
)
ENEMY_EXPLOSION_2 = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "explosionblue.png")),
    (
        int(
            pygame.image.load(os.path.join("images", "explosionblue.png")).get_width()
            * EXPLOSION_SCALE
        ),
        int(
            pygame.image.load(os.path.join("images", "explosionblue.png")).get_height()
            * EXPLOSION_SCALE
        ),
    ),
)
ENEMY_EXPLOSION_3 = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "explosiongreen.png")),
    (
        int(
            pygame.image.load(os.path.join("images", "explosiongreen.png")).get_width()
            * EXPLOSION_SCALE
        ),
        int(
            pygame.image.load(os.path.join("images", "explosiongreen.png")).get_height()
            * EXPLOSION_SCALE
        ),
    ),
)

# Player ship
PLAYER_SHIP = pygame.image.load(os.path.join("images", "ship.png"))

# Lasers
LASER = pygame.image.load(os.path.join("images", "laser.png"))
ENEMY_LASER = pygame.image.load(os.path.join("images", "enemylaser.png"))

# Background
BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "background.jpg")), (WIDTH, HEIGHT)
)

# Load sounds
ENEMY_KILLED = pygame.mixer.Sound("sounds/invaderkilled.wav")
MYSTERY_ENTER = pygame.mixer.Sound("sounds/mysteryentered.wav")
MYSTERY_KILLED = pygame.mixer.Sound("sounds/mysterykilled.wav")
SHIP_EXPLOSION = pygame.mixer.Sound("sounds/shipexplosion.wav")
ENEMY_SHOOT = pygame.mixer.Sound("sounds/shoot.wav")
PLAYER_SHOOT = pygame.mixer.Sound("sounds/shoot2.wav")

# Font
FONT = pygame.font.Font("fonts/space_invaders.ttf", 30)


class Explosion:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.counter = 0
        self.max_counter = 20  # Duration of explosion animation

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        self.counter += 1

    def is_complete(self):
        return self.counter >= self.max_counter


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cooldown_counter >= 30:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x + 22, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1
            if 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT:
                pygame.mixer.Sound.play(ENEMY_SHOOT)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class MysteryEnemy(Ship):
    def __init__(self, y, health=100):
        # Start from outside the left edge of the screen
        super().__init__(-100, y, health)
        self.ship_img = MYSTERY_SHIP
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.score_value = 150  # Higher score for mystery ship

    def move(self, vel):
        self.x += vel  # Horizontal movement

    def is_off_screen(self):
        return self.x > WIDTH


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def shoot(self):
        if self.cooldown_counter == 0:
            laser1 = Laser(self.x + 8, self.y, self.laser_img)
            laser2 = Laser(self.x + self.get_width() - 12, self.y, self.laser_img)
            self.lasers.extend([laser1, laser2])
            self.cooldown_counter = 1
            pygame.mixer.Sound.play(PLAYER_SHOOT)

    def move_lasers(self, vel, objs):
        self.cooldown()
        global explosions, mystery_enemy, score
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        pygame.mixer.Sound.play(ENEMY_KILLED)
                        if obj.ship_img == PURPLE_SPACE_SHIP:
                            explosions.append(
                                Explosion(obj.x, obj.y, ENEMY_EXPLOSION_1)
                            )
                        elif obj.ship_img == BLUE_SPACE_SHIP:
                            explosions.append(
                                Explosion(obj.x, obj.y, ENEMY_EXPLOSION_2)
                            )
                        elif obj.ship_img == GREEN_SPACE_SHIP:
                            explosions.append(
                                Explosion(obj.x, obj.y, ENEMY_EXPLOSION_3)
                            )

                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            score += obj.score_value

                # Check collision with mystery enemy
                if mystery_enemy and laser in self.lasers:
                    if laser.collision(mystery_enemy):
                        explosions.append(
                            Explosion(
                                mystery_enemy.x, mystery_enemy.y, ENEMY_EXPLOSION_1
                            )
                        )
                        score += mystery_enemy.score_value
                        mystery_enemy = None
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(
            window,
            (245, 169, 127),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width(),
                10,
            ),
        )
        pygame.draw.rect(
            window,
            (183, 189, 248),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width() * (self.health / self.max_health),
                10,
            ),
        )


class Enemy(Ship):
    COLOR_MAP = {
        "purple": (PURPLE_SPACE_SHIP, ENEMY_LASER),
        "blue": (BLUE_SPACE_SHIP, ENEMY_LASER),
        "green": (GREEN_SPACE_SHIP, ENEMY_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = Enemy.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.color = color
        # Assign score values based on enemy color
        if color == "purple":
            self.score_value = 30
        elif color == "green":
            self.score_value = 20
        else:  # blue
            self.score_value = 10

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    global score
    FPS = 60
    level = 0
    lives = 10
    score = 0
    main_font = FONT
    lost_font = (FONT, 60)
    global explosions, mystery_enemy

    enemies = []
    explosions = []
    mystery_enemy = None
    wave_length = 5
    enemy_vel = 1
    laser_vel = 5
    player = Player(300, 630)

    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BACKGROUND, (0, 0))
        # Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (243, 139, 168))
        level_label = main_font.render(f"Level: {level}", 1, (242, 205, 205))
        score_label = main_font.render(f"Score: {score}", 1, (242, 205, 205))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (10, 50))
        for enemy in enemies:
            enemy.draw(WIN)
        if mystery_enemy:
            mystery_enemy.draw(WIN)
        for explosion in explosions:
            explosion.draw(WIN)
        player.draw(WIN)

        if lost:
            lost_label = lost_font[0].render("You Lost!", 1, (183, 189, 248))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            # Spawn mystery enemy in levels divisible by 3
            if level % 3 == 0:
                mystery_y = random.randrange(50, 200)
                mystery_enemy = MysteryEnemy(mystery_y)
                pygame.mixer.Sound.play(MYSTERY_ENTER)

            for i in range(wave_length):
                enemy_x = random.randrange(50, WIDTH - 100)
                enemy_y = random.randrange(-1500, -100)
                enemy_color = random.choice(list(Enemy.COLOR_MAP.keys()))
                enemy = Enemy(enemy_x, enemy_y, enemy_color)
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - 5 > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x + 5 + player.get_width() < WIDTH:
            player.x += 5
        if keys[pygame.K_UP] and player.y - 5 > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.y + 5 + player.get_height() + 10 < HEIGHT:
            player.y += 5
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 5 * FPS) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                pygame.mixer.Sound.play(SHIP_EXPLOSION)
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        # Handle mystery enemy
        if mystery_enemy:
            mystery_enemy.move(2)  # Move faster than regular enemies
            if mystery_enemy.is_off_screen():
                mystery_enemy = None
            elif collide(mystery_enemy, player):
                player.health -= 15  # More damage
                pygame.mixer.Sound.play(MYSTERY_KILLED)
                explosions.append(
                    Explosion(mystery_enemy.x, mystery_enemy.y, ENEMY_EXPLOSION_1)
                )
                mystery_enemy = None
        explosions = [
            explosion for explosion in explosions if not explosion.is_complete()
        ]


def main_menu():
    title_font = (FONT, 70)
    subtitle_font = (FONT, 30)
    run = True

    # Enemy score values
    enemy_scores = [
        {"img": PURPLE_SPACE_SHIP, "score": 30, "name": ""},
        {"img": GREEN_SPACE_SHIP, "score": 20, "name": ""},
        {"img": BLUE_SPACE_SHIP, "score": 10, "name": ""},
        {"img": MYSTERY_SHIP, "score": 150, "name": ""},
    ]

    while run:
        WIN.blit(BACKGROUND, (0, 0))
        title_label = title_font[0].render(
            "Press the mouse to begin...", 1, (255, 255, 255)
        )
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 250))
        subtitle = subtitle_font[0].render("Enemy Score Values:", 1, (255, 255, 255))
        WIN.blit(subtitle, (WIDTH / 2 - subtitle.get_width() / 2, 350))
        y_offset = 400
        for enemy in enemy_scores:
            img = pygame.transform.scale(enemy["img"], (50, 50))
            WIN.blit(img, (WIDTH / 2 - 150, y_offset))

            score_text = subtitle_font[0].render(
                f"{enemy['name']}: {enemy['score']} points", 1, (166, 227, 161)
            )
            WIN.blit(score_text, (WIDTH / 2 - 80, y_offset + 15))

            y_offset += 60

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()

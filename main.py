# Welcome to my код, удачи разобраться
# библиотеки
import pygame
import random
import time
import os
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')
# tests

# ------------------------------------------------------------------
# основные переменные
WIDTH = 1280
HEIGHT = 720
FPS = 60
amount_enemy = 20
# ------------------------------------------------------------------
# надписи
TEXT_SCORE = 'SCORE:'
TEXT_RECORD_PLAYER = 'RECORD:'
# ------------------------------------------------------------------
# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# ------------------------------------------------------------------
# музыка
music_list = ['music/1.mp3', 'music/2.mp3', 'music/3.mp3',
              'music/4.mp3', 'music/5.mp3', 'music/6.mp3',
              'music/7.mp3', 'music/8.mp3']
music_round = random.choice(music_list)
pygame.mixer.init()
pygame.mixer.music.load(music_round)
# закоменить строчку ниже, что бы выключить музыку
#pygame.mixer.music.play()
# звуки
cannon_sound_list = ['cannon_pew.wav', 'cannon_paw.wav']
cannon_sound_round = random.choice(cannon_sound_list)
cannon_sound = pygame.mixer.Sound(path.join(sound_dir, cannon_sound_round))
explosion_sound_list = ['explosion.wav', 'explosion1.wav']
explosion_sound_round = random.choice(explosion_sound_list)
explosion_sound = pygame.mixer.Sound(path.join(sound_dir, explosion_sound_round))
# ------------------------------------------------------------------
# базовые настройки
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("100% ЛОВУШКА ТРОЛЛИНГ МАЙНКРАФТ")
clock = pygame.time.Clock()
# ------------------------------------------------------------------
# sozdanie shrifta
font_name = pygame.font.match_font('playbill')


# ------------------------------------------------------------------
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newenemy():
    e = Enemy()
    all_sprites.add(e)
    enemy.add(e)


def health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def cannon_shoot(self):
        bullet = cannons_yadro(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        cannon_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def animation_of_enemy(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.animation_of_enemy()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class cannons_yadro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# спрайты
background_list = ['background.jpg',

                     'background1.jpg',

                   'background2.jpg'
                   ]
background_random = random.choice(background_list)
background = pygame.image.load(path.join(img_dir, background_random)).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "player_cannon.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
meteor_images = []
meteor_list = ['big_green_mob.png', 'big_pink_mob.png', 'mid_blue_mob.png', 'mid_lime_mob.png', 'small_red_mob.png',
               'small_gold_mob.png', 'tiny_green_mob.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

all_sprites = pygame.sprite.Group()
enemy = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(amount_enemy):
    m = Enemy()
    all_sprites.add(m)
    enemy.add(m)
score = 0
# score_img = pygame.image.load(path.join(img_dir, "yandex_score.png")).convert()
# image = pygame.transform.scale(score_img, (50, 38))
# image.set_colorkey(BLACK)
# rect = image.get_rect()
# radius = 20
# rect.centerx = WIDTH / 2
# rect.bottom = HEIGHT - 10
# speedx = 0
# image = pygame.Surface([100, 100])
# image.fill(pygame.Color("red"))
# screen.blit(image, (200, 10))
# screen.blit(score_img, (WIDTH - 100, 10))
# игр цикл
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.cannon_shoot()
    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        explosion_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newenemy()
    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
        if hit.radius >= 30:
            score += 1
            newenemy()
        elif hit.radius > 10 and hit.radius < 30:
            score += 2
            newenemy()
        elif hit.radius <= 10:
            score += 3
            newenemy()
            player.health += 1
#            print(player.health)
        m = Enemy()
        all_sprites.add(m)
        enemy.add(m)
        explosion_sound.play()
        newenemy()
    hits = pygame.sprite.spritecollide(player, enemy, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
#        print(player.health)
        newenemy()
        if player.health <= 0:
            pygame.quit()
            os.system(r'end.py')
#            running = False
    # шрифт
    font = pygame.font.Font(None, 25)
    text = font.render("SCORE:", True, WHITE)
    screen.blit(text, [WIDTH - 120, 10])
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    #    score_img = pygame.image.load(path.join(img_dir, "yandex_score.png")).convert()
    score_img = pygame.image.load(path.join(img_dir, 'yandex_score.png')).convert_alpha()
    screen.blit(score_img, (WIDTH - 120, -30))
    #    record_img.png
#    record_img = pygame.image.load(path.join(img_dir, 'record_img.png')).convert_alpha()
#    screen.blit(record_img, (WIDTH - 100, 40))

    # Счет на данный момент в раунде
    #    draw_text(screen, str(TEXT_SCORE), 15, WIDTH - 100, 10)
    draw_text(screen, str(score), 25, WIDTH - 30, 20)
    health_bar(screen, 5, 5, player.health)
    # подключить БД, лучший счет за все время
    #    draw_text(screen, str(TEXT_RECORD_PLAYER), 15, WIDTH - 110, 50)
    # обнова через 20 сек ГОУ ГОУ ГОУ
    pygame.display.flip()

pygame.quit()

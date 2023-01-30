import pygame
from settings import *
import spritesheet
from projectile import Projectile
from pygame import mixer

BLACK = (0, 0, 0)
pygame.init()
pygame.mixer.init()
mixer.init()

class Hero(pygame.sprite.Sprite):
    def __init__(self, speedx, speedy, facing, all_sprites, bullets, tiles, x, y, aim): # скорость по иксу, скорость по игрику, направление спрайта (лево право), все спрайты отрисовки, группа пуль, группа блоков, координаты, класс прицела
        pygame.sprite.Sprite.__init__(self)
        self.speedx = speedx
        self.speedy = speedy
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.animation_list = []
        self.animation_list.append(idle_list)
        self.animation_list.append(walk_list)
        self.action = 0  # 0-idle, 1-walking
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_rect()[2] * 0.8, self.image.get_rect()[3] * 0.8))
        self.rect = self.image.get_rect()
        self.last_coords = self.rect
        self.facing = 0  # 0 -right, 1-left
        self.shoot_time = pygame.time.get_ticks()
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.tiles = tiles
        self.rect.centerx = x
        self.rect.bottom = y
        self.aim = aim
        self.help_x = 0
        self.help_y = 0
        self.damage = 10
        self.hp = 100
        self.max_hp = 100
        self.collision_time = 500



    def update(self):
        animation_cooldown = 100 # чкорость смены кадров
        if not self.facing: # анимация
            self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], True, False)
            self.image.set_colorkey(BLACK)
        else:
            self.image = self.animation_list[self.action][self.frame_index]
        self.action = 0
        if pygame.time.get_ticks() - self.update_time >= animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

        btn = pygame.key.get_pressed()


        if btn[pygame.K_a]: # движение от нажатой кнопки
            self.rect.x -= self.speedx
            self.action = 1
            self.facing = 0
            self.help_x -= self.speedx
            if pygame.sprite.spritecollide(self, self.tiles, False): # отталкивание от блоков
                self.rect.x += self.speedx
                self.help_x += self.speedx
        if btn[pygame.K_d]:
            self.rect.x += self.speedx
            self.action = 1
            self.facing = 1
            self.help_x += self.speedx
            if pygame.sprite.spritecollide(self, self.tiles, False):
                self.rect.x -= self.speedx
                self.help_x -= self.speedx
        if btn[pygame.K_w]:
            self.rect.y -= self.speedy
            self.action = 1
            self.help_y -= self.speedy
            if pygame.sprite.spritecollide(self, self.tiles, False):
                self.rect.y += self.speedy
                self.help_y += self.speedy
        if btn[pygame.K_s]:
            self.rect.y += self.speedy
            self.action = 1
            self.help_y += self.speedy
            if pygame.sprite.spritecollide(self, self.tiles, False):
                self.rect.y -= self.speedy
                self.help_y -= self.speedy

        if pygame.mouse.get_pressed()[0]: # стрельба
            if pygame.time.get_ticks() - self.shoot_time >= 250:
                self.shoot(self.all_sprites, self.bullets)
                self.shoot_time = pygame.time.get_ticks()

    def shoot(self, group_of_sprite, bullets_sprite): # функция стрельбы
        if self.facing:
            bullet = Projectile(10, self.rect.x + self.rect.w * 0.9, self.rect.y,
                                self.aim.rect.x + self.help_x - self.aim.rect.x * 0.02, self.aim.rect.y + self.help_y -
                                self.aim.rect.y * 0.02, fire_bullet, 90)
        else:
            bullet = Projectile(10, self.rect.x, self.rect.y, self.aim.rect.x + self.help_x + self.aim.rect.x * 0.02,
                                self.aim.rect.y + self.help_y + self.aim.rect.y * 0.02, fire_bullet, 90)
        group_of_sprite.add(bullet)
        bullets_sprite.add(bullet)
        melody = pygame.mixer.Sound('music/Fireball-Magic-Attack-C-www.fesliyanstudios.com.mp3')
        melody.play()

    def take_damage(self, damage):
        if pygame.time.get_ticks() - self.collision_time > 500:  # The time is in ms.
            self.hp -= damage
            self.collision_time = pygame.time.get_ticks()



class Aim(pygame.sprite.Sprite):

    def __init__(self, x, y): # координаты прицела
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/target_20.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (512 * 0.08, 512 * 0.08))
        self.image.set_colorkey(BLACK)
        self.x, self.y = x, y

    def update(self): # обновление расположения прицела
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - 20 + self.x
        self.rect.y = pos[1] - 20 + self.y

screen = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_sheet_idle = pygame.image.load('sprites/mage.png').convert_alpha()
sprite_sheet_walk = pygame.image.load('sprites/mage.png').convert_alpha()

# анимация героя
show_idle = spritesheet.Spritesheet(sprite_sheet_idle)
show_walk = spritesheet.Spritesheet(sprite_sheet_walk)

idle_list = spritesheet.get_animation(show_idle, 64, 128, BLACK, 9, 1, 0)
walk_list = spritesheet.get_animation(show_walk, 64, 128, BLACK, 9, 1, 0)
bullets = pygame.sprite.Group()

fire_bullet = []
for i in range(12): # анимация пулек
    img = pygame.image.load(f"sprites/fire/{i}-PhotoRoom.png")
    img = pygame.transform.scale(img, (img.get_rect()[2] * 0.15, img.get_rect()[3] * 0.15))
    img.set_colorkey(BLACK)
    fire_bullet.append(img)

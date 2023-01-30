import pygame
import spritesheet
import math
from projectile import Projectile
from pygame import mixer

BLACK = (0, 0, 0)
pygame.init()
mixer.init()
pygame.mixer.init()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, enemies, enemy_lst, all_sprites, tiles): # x y - положение , enemies - группа спрайтов врагов, enemy_llst - лист врагов питоновский, группа всех спрайтов
        pygame.sprite.Sprite.__init__(self)
        self.facing = 0
        self.animation_list = []
        self.action = 0  # 0-idle 1-walk 2-death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.vel = vel
        self.float_x = x
        self.float_y = y
        self.hp = 100
        self.enemies = enemies
        self.enemy_lst = enemy_lst
        self.enemies.add(self)
        self.enemy_lst.append(self)
        self.live = True
        self.animation_cooldown = 100
        self.all_sprites = all_sprites
        self.all_sprites.add(self)
        self.tiles = tiles
        self.name = ''
        self.moving = True


    def updater(self, direction_x, direction_y):
        try:
            if not self.facing:
                self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], True, False) # смена кадров анимации
                self.image.set_colorkey(BLACK)
            else:
                self.image = self.animation_list[self.action][self.frame_index]
                self.image.set_colorkey(BLACK)
            if pygame.time.get_ticks() - self.update_time >= self.animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0
                    if self.action == 2:

                        self.kill()
                        melody = pygame.mixer.Sound(self.name)
                        melody.play()


                        for i in range(len(self.enemy_lst)):
                            if id(self) == id(self.enemy_lst[i]):
                                del self.enemy_lst[i]
                                break
        except:
            self.frame_index = 0

        if self.action != 2 and self.moving and ((self.rect.x - direction_x) ** 2 + (self.rect.y - direction_y) ** 2) ** 0.5 <= 640:  # движение врагов
            x_diff = direction_x - self.rect.x
            y_diff = direction_y - self.rect.y

            self.angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(self.angle) * self.vel
            self.change_y = math.sin(self.angle) * self.vel
            prevx = self.rect.x
            prevy = self.rect.y
            self.float_y += self.change_y
            self.float_x += self.change_x
            self.rect.x = self.float_x
            self.rect.y = self.float_y
            if pygame.sprite.spritecollide(self, self.tiles, False):
                self.rect.x = prevx
                self.rect.y = prevy
            if direction_x > self.rect.x:
                self.facing = True
            else:
                self.facing = False
            self.action = 1
        else:
            self.action = 0


        if self.hp <= 0:
            self.action = 2


class Golem(Enemy):

    def __init__(self, x, y, vel, enemies, enemy_lst, all_sprites, bullets, tiles):
        super().__init__(x, y, vel, enemies, enemy_lst, all_sprites, tiles)
        self.action = 0  # 0-idle 1-going 2-dying 3-defending 4-shoot
        self.animation_list = golem_lst
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_cooldown = 150
        self.bullets = bullets
        self.shoot_time = pygame.time.get_ticks()
        self.shooting = False
        self.action = 1
        self.sound_take_damage = 'music/golem_take_damage.wav'
        self.name = 'music/' + (str(self.__class__).split('.')[1][:-2] + '_die.mp3').lower()
        self.flag = False
        self.strike_laser = False

    def updater(self, direction_x, direction_y):
        super().updater(direction_x, direction_y) # наследование движения и анимации


        if pygame.time.get_ticks() - self.shoot_time >= 3000 and self.action != 2 and \
                ((self.rect.x - direction_x) ** 2 + (self.rect.y - direction_y) ** 2) ** 0.5 <= 640: # стрельба
            self.shooting = True
            self.moving = False
            self.shoot_time = pygame.time.get_ticks()
        if self.shooting:
            self.action = 4
        if self.action == 4 and self.frame_index == 8:
            self.shoot(2, direction_x, direction_y, shoot_list1, self.bullets)
            self.shoot_time = pygame.time.get_ticks()
            self.shooting = False
            self.moving = True
            self.frame_index = 0
            self.action = 1


    def shoot(self, vel, direction_x, direction_y, sprite_list, bullets_type): # функция стрельбы
        if not self.facing:
            bullet = Projectile(vel, self.rect.x, self.rect.y + self.rect.y * 0.1, direction_x, direction_y - self.rect.y * 0.1, sprite_list)
        else:
            bullet = Projectile(vel, self.rect.x + self.rect.width, self.rect.y + self.rect.y * 0.1, direction_x, direction_y - self.rect.y * 0.1, sprite_list)
        self.all_sprites.add(bullet)
        bullets_type.add(bullet)
        melody = pygame.mixer.Sound('music/golem_strike.wav')
        melody.play()
        return bullet


class Gladiator(Enemy):

    def __init__(self, x, y, vel, enemies, enemy_lst, all_sprites, tiles, hero_group):
        super().__init__(x, y, vel, enemies, enemy_lst, all_sprites, tiles)

        self.action = 0  # 0-idle 1-going 2-dying 3-defending 4-shoot
        self.animation_list = gladiator_list
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_cooldown = 150
        self.hero_group = hero_group
        self.damage = 15
        self.sound_take_damage = 'music/gladiator_take_damage.wav'
        self.name = 'music/' + (str(self.__class__).split('.')[1][:-2] + '_die.mp3').lower()

    def updater(self, direction_x, direction_y):
        super().updater(direction_x, direction_y)
        if pygame.sprite.spritecollide(self, self.hero_group, False):
            self.action = 3
            self.moving = False
        if self.action == 3 and 3 <= self.frame_index <= 5 and pygame.sprite.spritecollide(self, self.hero_group, False):
            for i in self.hero_group:
                i.take_damage(self.damage)
            melody = pygame.mixer.Sound('music/gladiator_attack.wav')
            melody.play()
        if self.action == 3 and self.frame_index >= 6:
            self.frame_index = 0
            self.moving = True
            self.action = 1
        if self.action != 3:
            self.moving = True


class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, enemies, enemy_lst, hero_group):
        pygame.sprite.Sprite.__init__(self)

        self.facing = 0
        self.animation_list = bat_list
        self.action = 0  # 0-idle 1-walk 2-death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = vel
        self.float_x = x
        self.float_y = y
        self.hp = 100
        self.enemies = enemies
        self.enemy_lst = enemy_lst
        self.enemies.add(self)
        self.enemy_lst.append(self)
        self.live = True
        self.animation_cooldown = 100
        self.hero_group = hero_group
        self.damage = 5
        self.sound_take_damage = 'music/bat_take_damage.mp3'
        self.name = 'music/' + (str(self.__class__).split('.')[1][:-2] + '_die.mp3').lower()

        self.moving = True

    def updater(self, direction_x, direction_y):

        try:
            if not self.facing:
                self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], True, False) # смена кадров анимации
                self.image.set_colorkey(BLACK)
            else:
                self.image = self.animation_list[self.action][self.frame_index]
                self.image.set_colorkey(BLACK)
            if self.hp > 100:
                self.image = pygame.transform.scale(self.image, (self.rect.width * (1 + (self.hp) // 100), self.rect.height * (1 + (self.hp) // 100)))
                self.image.set_colorkey(BLACK)
            if pygame.time.get_ticks() - self.update_time >= self.animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0
                    if self.action == 2:
                        self.kill()
                        melody = pygame.mixer.Sound(self.name)
                        melody.play()

                        for i in range(len(self.enemy_lst)):
                            if id(self) == id(self.enemy_lst[i]):
                                del self.enemy_lst[i]
                                break
        except:
            self.frame_index = 0

        if self.action != 2 and self.moving and ((self.rect.x - direction_x) ** 2 + (self.rect.y - direction_y) ** 2) ** 0.5 <= 640:  # движение врагов
            x_diff = direction_x - self.rect.x
            y_diff = direction_y - self.rect.y

            self.angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(self.angle) * self.vel
            self.change_y = math.sin(self.angle) * self.vel
            self.float_y += self.change_y
            self.float_x += self.change_x
            self.rect.x = self.float_x
            self.rect.y = self.float_y
            if direction_x > self.rect.x:
                self.facing = True
            else:
                self.facing = False
            if self.action != 1:
                self.action = 0

        if self.hp <= 0:
            self.action = 2

        if pygame.sprite.spritecollide(self, self.hero_group, False):
            self.action = 1
            self.moving = False
            for i in self.hero_group:
                i.take_damage(self.damage)
                self.hp += 0.5
        elif self.action != 2:
            self.action = 0
            self.moving = True



sprite_sheet_idle1 = pygame.image.load('sprites/gladiator.png').convert_alpha()
show_idle1 = spritesheet.Spritesheet(sprite_sheet_idle1)
idle_1_list = spritesheet.get_animation(show_idle1, 32, 32, BLACK, 7, 4, 2)

# Sprites for golem
sprite_sheet_idle = pygame.image.load('sprites/Golem1.png').convert_alpha() # пример создания типа анимации бег, стрельба и тд
show_idle = spritesheet.Spritesheet(sprite_sheet_idle)
idle_list = spritesheet.get_animation(show_idle, 54, 50, BLACK, 4, 4, 0)

sprite_sheet_idle = pygame.image.load('sprites/Golem2.png').convert_alpha()
defence = spritesheet.Spritesheet(sprite_sheet_idle)
defence_list = spritesheet.get_animation(defence, 53, 48, BLACK, 8, 4, 0)

sprite_sheet_idle = pygame.image.load('sprites/Golem3.png').convert_alpha()
die = spritesheet.Spritesheet(sprite_sheet_idle)
die_list = spritesheet.get_animation(die, 60, 78, BLACK, 14, 4, 0)

sprite_sheet_idle = pygame.image.load('sprites/Golem4.png').convert_alpha()
shoot = spritesheet.Spritesheet(sprite_sheet_idle)
shoot_list = spritesheet.get_animation(shoot, 77, 49, BLACK, 9, 4, 0)

sprite_sheet_idle = pygame.image.load('sprites/GolemArm.png').convert_alpha()
shoot = spritesheet.Spritesheet(sprite_sheet_idle)
shoot_list1 = spritesheet.get_animation(shoot, 35, 14, BLACK, 6, 4, 0)

golem_lst = []  # добавление всей анимации
golem_lst.append(idle_list)
golem_lst.append(defence_list)
golem_lst.append(die_list)
golem_lst.append(defence_list)
golem_lst.append(shoot_list)

gladiator_list = []
sprite_sheet_idle = pygame.image.load('sprites/gladiator.png').convert_alpha()
idle_gladiator = spritesheet.Spritesheet(sprite_sheet_idle)
idle_gladiator = spritesheet.get_animation(idle_gladiator, 32, 32, BLACK, 5, 4, 0)

sprite_sheet_idle = pygame.image.load('sprites/gladiator.png').convert_alpha()
walk_gladiator = spritesheet.Spritesheet(sprite_sheet_idle)
walk_gladiator = spritesheet.get_animation(walk_gladiator, 32, 32, BLACK, 8, 4, 1)

sprite_sheet_idle = pygame.image.load('sprites/gladiator.png').convert_alpha()
die_gladiator = spritesheet.Spritesheet(sprite_sheet_idle)
die_gladiator = spritesheet.get_animation(die_gladiator, 32, 32, BLACK, 8, 4, 4)

sprite_sheet_idle = pygame.image.load('sprites/gladiator.png').convert_alpha()
attack_gladiator = spritesheet.Spritesheet(sprite_sheet_idle)
attack_gladiator = spritesheet.get_animation(attack_gladiator, 32, 32, BLACK, 7, 4, 2)

gladiator_list.append(idle_gladiator)
gladiator_list.append(walk_gladiator)
gladiator_list.append(die_gladiator)
gladiator_list.append(attack_gladiator)

bat_list = []

sprite_sheet_idle = pygame.image.load('sprites/bat.png').convert_alpha()
bat_fly = spritesheet.Spritesheet(sprite_sheet_idle)
bat_fly = spritesheet.get_animation(bat_fly, 16, 24, BLACK, 5, 4, 1)

sprite_sheet_idle = pygame.image.load('sprites/bat.png').convert_alpha()
bat_attack = spritesheet.Spritesheet(sprite_sheet_idle)
bat_attack = spritesheet.get_animation(bat_attack, 16, 24, BLACK, 5, 4, 0)

sprite_sheet_idle = pygame.image.load('sprites/bat.png').convert_alpha()
bat_die = spritesheet.Spritesheet(sprite_sheet_idle)
bat_die = spritesheet.get_animation(bat_die, 16, 24, BLACK, 5, 4, 2)

bat_list.append(bat_fly)
bat_list.append(bat_attack)
bat_list.append(bat_die)

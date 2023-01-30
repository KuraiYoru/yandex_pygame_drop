import pygame
import math
from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, vel, x, y, direction_x, direction_y, sprite_list=None, rotate=360): # скорость, координаты, направление полета по координатам, спрайт для пуль, поворот спрайта пули
        pygame.sprite.Sprite.__init__(self)
        self.lst = sprite_list[::]
        if self.lst is not None:
            self.image = self.lst[0]
        else:
            self.image = pygame.Surface((5, 5))
            self.image.fill((255, 0, 0))
        self.vel = vel
        self.rect = self.image.get_rect()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.rotate = rotate



        self.rect.x = x
        self.rect.y = y

        self.float_x = x
        self.float_y = y

        x_diff = direction_x - x
        y_diff = direction_y - y

        self.angle = math.atan2(y_diff, x_diff)
        for i in range(len(self.lst)):
            self.lst[i] = pygame.transform.rotate(self.lst[i], self.rotate)
            self.lst[i] = pygame.transform.rotate(self.lst[i], (360 - self.angle * 180 / math.pi) % 360)
            self.lst[i].set_colorkey((0, 0, 0))

            self.rect = self.lst[i].get_rect(center=self.lst[i].get_rect(center=(x, y)).center)
        self.image = self.lst[0]

        self.change_x = math.cos(self.angle) * vel
        self.change_y = math.sin(self.angle) * vel

        # distance_x = a.x - hero.x  Управляемая стрельба
        # distance_y = a.y - hero.y
        # angle = math.atan2(distance_y, distance_x)
        # bullet.x += bullet.vel * math.cos(angle)
        # bullet.y += bullet.vel * math.sin(angle)

    def update(self):
        # анимация пули
        if self.lst is not None:
            animation_cooldown = 100
            self.image = self.lst[self.frame_index]
            if pygame.time.get_ticks() - self.update_time >= animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.lst):
                    self.frame_index = 0
        # полет пули
        self.float_y += self.change_y
        self.float_x += self.change_x

        self.rect.x = int(self.float_x)
        self.rect.y = int(self.float_y)
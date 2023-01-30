import pygame
from settings import *

pygame.init()


class Bar(pygame.sprite.Sprite):
    def __init__(self, hero):
        pygame.sprite.Sprite.__init__(self)


        self.sprites = []
        for i in range(16):
            img = pygame.image.load(f'sprites/healthbar/Health bar{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (WIDTH * 0.2, HEIGHT * 0.1))
            self.sprites.append(img)
        self.image = self.sprites[15]
        self.rect = self.image.get_rect()
        self.hero = hero

    def update(self):
        num = int((len(self.sprites) - 1) * self.hero.hp / self.hero.max_hp) # смена полоски здоровья в зависимости от здоровья
        self.image = self.sprites[num]


    def draw(self, x, y, screen):
        screen.blit(self.image, (x, y))

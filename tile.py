import pygame
from settings import *
# класс блоков


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('sprites/block.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
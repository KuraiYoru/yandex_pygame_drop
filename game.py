import pygame
import sys
from pygame import mixer
from settings import *
from level import Level

from menu import Menu

BLACK = (0, 0, 0)
# TEST
class Game:
    def __init__(self):

        pygame.init()

        pygame.mixer.init()
        mixer.init()
        mixer.music.load('music/song18.mp3')
        self.sound1 = pygame.mixer.Sound('music/song18.mp3')
        self.sound_win = pygame.mixer.Sound('music/win.mp3')
        self.sound_loose = pygame.mixer.Sound('music/game_over.mp3')

        self.sound1.set_volume(0.3)
        self.game_run = False


        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill((50, 50, 50))
        pygame.display.set_caption('Spritesheets')

        bg_img = pygame.image.load('sprites/bg.png').convert_alpha()
        self.bg = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))


        self.fire = []

        self.level = Level(self.screen)
        self.level.visible_sprites.add()
        self.shoot_time = pygame.time.get_ticks()
        self.enemies = self.level.enemies


    def run(self): # основной цикл игры
        i = 0
        paused = False
        pygame.mouse.set_visible(False)
        self.game_run = True
        melody = mixer.Sound('music/stranger-things-124008.mp3')
        melody.set_volume(0.2)
        melody.play(-1)

        while True:
            self.sound1.stop()
            if len(self.enemies) == 0:
                start("You win!")
                melody.stop()
                # self.sound1.stop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                    else:
                        paused = True

            if self.level.hero.hp <= 0:
                start("You lose!")
                melody.stop()
                # self.sound1.stop()

            if not paused:
                self.clock.tick(FPS)
                self.screen.fill((50, 50, 50))
                self.screen.blit(self.bg, (0, i))  # движение заднего фона
                self.screen.blit(self.bg, (0, HEIGHT + i))
                if i == -HEIGHT:
                    self.screen.blit(self.bg, (0, HEIGHT + i))
                    i = 0
                i -= 1

                self.level.run()


                pygame.display.flip()
            else:
                font = pygame.font.Font(None, 128)
                text = font.render("GAME PAUSED!", True, (15, 144, 182))
                text_x = WIDTH // 2 - text.get_width() // 2
                text_y = HEIGHT // 2 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                self.screen.blit(text, (text_x, text_y))
                pygame.draw.rect(self.screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20), 5)
                pygame.display.flip()


def start(condition):
    game = Game()
    game.sound1.play(-1)
    if condition == "You win!":
        game.sound_win.play(1)
    elif condition == "You lose!":
        game.sound_loose.play(1)

    menu = Menu(game.run, game.screen, condition)


if __name__ == "__main__":
    start("")




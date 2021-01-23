import pygame
import os
import time
from os import path

pygame.mixer.init()
sound_dir = path.join(path.dirname(__file__), 'sound')
loading_sound = pygame.mixer.Sound(path.join(sound_dir, 'loading.wav'))

if __name__ == '__main__':

    pygame.init()

    size = width, height = 1280, 720

    screen = pygame.display.set_mode(size)


    def draw(screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 110)
        text = font.render("ЗаГрУзОчКа...", True, (0, 255, 25))
        font1 = pygame.font.Font(None, 30)
        text1 = font1.render('P.s. Нажми на крестик', True, (179, 168, 168))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        text_x1 = width // 1.1 - text1.get_width() // 2
        text_y1 = height // 12 - text1.get_height() // 2
        screen.blit(text, (text_x, text_y))
        screen.blit(text1, (text_x1, text_y1))
        loading_sound.play()

    draw(screen)


    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()
    os.system(r'main.py')


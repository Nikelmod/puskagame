import pygame
#import time
from os import path
pygame.mixer.init()
sound_dir = path.join(path.dirname(__file__), 'sound')
end_sound = pygame.mixer.Sound(path.join(sound_dir, 'end.wav'))

if __name__ == '__main__':

    pygame.init()

    size = width, height = 1280, 720

    screen = pygame.display.set_mode(size)


    def draw(screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 110)
        text = font.render("Ты проиграл(а) дурень!", True, (255, 25, 25))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (255, 26, 24), (text_x - 10, text_y - 10,
                                                 text_w + 20, text_h + 20), 1)
        end_sound.play()


    draw(screen)


    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()


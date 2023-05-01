import pygame

def draw_healthbar(screen, health, x, y):
    ratio = health / 100
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    pygame.draw.rect(screen, RED, (x, y, 400, 40))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 40))


def draw_bg(screen, image):
    screen.blit(image, (0, 0))

def draw_text(screen, font, sentence, text_col, x, y):
    text = font.render(sentence, True, text_col)
    screen.blit(text, (x, y))


def create_rectangle(x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    return rect
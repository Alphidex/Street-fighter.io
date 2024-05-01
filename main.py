import pygame
from game import Game

pygame.init()

# Game Window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Street-fighter.io")  # Screen Title

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Game Class
game = Game()

# Variables
running = True

while running:
    # Refresh at 60 FPS
    clock.tick(FPS)

    # Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    game.run(events)

    if game.exit_game:
        running = False

    # Reset the game once all levels complete
    if game.reset:
        game = Game()

    pygame.display.update()

# Quit Pygame
pygame.quit()


"""
Syntax Issues:
1. Camera Management has copies of map position and boundaries in game.py (function arena) where I'm resetting the
 positions and characters.py, where I'm checking for boundary collisions. For some reason, can't make them constants,
 as they change along with their copies. 

"""
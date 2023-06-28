import pygame
import sys
from game import *

pygame.init()

# Game Window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street-fighter.io")

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.run()

    # Other Methods to exit the game
    if game.exit_game:
        running = False

    # Reset the game once all levels complete
    if game.reset:
        game = Game()

    # Update the screen
    pygame.display.update()

# Get out of pygame
pygame.quit()

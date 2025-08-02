# See:
#  https://dev.to/lovelacecoding/how-to-build-your-first-python-game-a-step-by-step-guide-to-creating-a-simple-shooter-with-pygame-f0k
#
# Install pygame
#
# Create a place to install pygame and
# "activate" it:
#
# $ python3 -m venv venv
# $ . venv/bin/activate
#
# Use pip to install pygame:
#
# $ pip install pygame

import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter Game")

# Set the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player
    pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

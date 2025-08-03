

import pygame
import sys
import random
from sprite import Sprite, V
from enemy import Enemy
from cpu import CPU, Program

# Collision detection function
def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

class Game():
    def __init__(self):
        self.enemies = []
        self.player = None
        self.screen = None
        self.clock = None
        self.frame_rate = 60
        self.dt = 1.0 / self.frame_rate

    def init(self):
        # Initialize PyGame
        pygame.init()


        # Set up the game window
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simple Shooter Game")

        # Set the frame rate
        self.clock = pygame.time.Clock()

        # Player settings
        self.player_width = 50
        self.player_height = 60
        self.player_x = self.screen_width // 2 - self.player_width // 2
        self.player_y = self.screen_height - self.player_height - 10
        self.player_speed = 5

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_speed = 7
        self.bullets = []

        # Enemy settings
        self.enemy_width = 50
        self.enemy_height = 60
        self.enemy_speed = 2.0 * self.frame_rate
        self.enemies = []

        # Spawn an enemy every 2 seconds
        self.enemy_timer = 0
        self.enemy_spawn_time = 2000

    def run(self):
        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Create a bullet at the current player position
                        bullet_x = self.player_x + self.player_width // 2 - self.bullet_width // 2
                        bullet_y = self.player_y
                        self.bullets.append([bullet_x, bullet_y])

            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.player_x > 0:
                self.player_x -= self.player_speed
            if keys[pygame.K_d] and self.player_x < self.screen_width - self.player_width:
                self.player_x += self.player_speed

            # Move players, etc.
            self.tick(self.dt)

            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            # Draw characters:
            self.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate at 60 FPS
            self.clock.tick(self.frame_rate)

    def tick(self, dt: float):
            # Update bullet positions
            for bullet in self.bullets:
                bullet[1] -= self.bullet_speed
            self.bullets = [bullet for bullet in self.bullets if bullet[1] > 0]

            # Update enemy positions and spawn new ones
            current_time = pygame.time.get_ticks()
            if current_time - self.enemy_timer > self.enemy_spawn_time:
                enemy_x = random.randint(0, self.screen_width - self.enemy_width)
                enemy_y = - self.enemy_height
                color = (255, 0, 0)
                sprite = Sprite(V(self.enemy_width, self.enemy_height), color)
                program = Program(
                    [
                        ('const', V(-100.0, 0.0)),
                        ('const', V( 100.0, 0.0)),
                        'rand',
                        'acc',
                        ('const', 1.5),
                        'sleep',

                        ('const', V(0.0, -15.0)),
                        ('const', V(0.0,  75.0)),
                        'rand',
                        'acc',
                        ('const', 1.5),
                        'sleep',
                    ]
                )
                enemy = Enemy(
                    V(enemy_x, enemy_y),
                    V(0.0, self.enemy_speed),
                    sprite,
                    program,
                )
                self.enemies.append(enemy)
                self.enemy_timer = current_time

            for enemy in self.enemies:
                enemy.tick(dt)

            # Check for collisions
            for bullet in self.bullets[:]:
                for enemy in self.enemies[:]:
                    rect_1 = (bullet[0], bullet[1], self.bullet_width, self.bullet_height)
                    rect_2 = enemy.sprite.rect().as_tuple()
                    if check_collision(rect_1, rect_2):
                        self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        break

            # Remove enemies that are off the screen
            enemies = [enemy for enemy in self.enemies if enemy.pos.y < self.screen_height]

    def draw(self):
            # Draw the player
            pygame.draw.rect(
                self.screen,
                (0, 128, 255),
                (self.player_x, self.player_y, self.player_width, self.player_height)
            )

            # Draw the bullets
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, (255, 255, 255), (bullet[0], bullet[1], self.bullet_width, self.bullet_height))

            # Draw the enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)

if __name__ == '__main__':
    game = Game()
    game.init()
    game.run()

import sys
import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from timer import Duration
from sprite import Sprite, Rect, V
from enemy import Enemy
from bullet import Bullet
from player import Player
from cpu import CPU, Program
from functools import cached_property
import pdb # ; pdb.set_trace()

# Collision detection function
def check_collision(rect1, rect2):
    return pygame.Rect(rect1.as_tuple()).colliderect(pygame.Rect(rect2.as_tuple()))

class Game():
    def __init__(self):
        self.enemies: list = []
        self.bullets: list = []
        self.player: Player = None
        self.screen = None
        self.clock = None
        self.frame_rate = 60
        self.dt = self.t0_ms = self.t1_ms = None

    @cached_property
    def screen_size(self):
        return V(self.screen_width, self.screen_height)

    @cached_property
    def screen_bounds(self):
        return Rect(V(0, 0), V(self.screen_width, self.screen_height))

    @cached_property
    def enemy_bounds(self):
        return Rect(- self.screen_size, self.screen_size * 3)

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
        self.player_speed = self.player_width * 10
        self.player = self.make_player()

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_speed = 7 * 50
        self.bullets = []

        # Enemy settings
        self.enemy_width = 50
        self.enemy_height = 60
        self.enemy_speed = self.enemy_width * 1.0
        self.enemies = []

        # Spawn an enemy every 2 seconds
        self.enemy_timer = 0
        self.enemy_spawn_time = 2000

    #############################################################

    def run(self):
        # Main game loop
        self.t1_ms = pygame.time.get_ticks()
        pygame.time.wait(100)
        while True:
            self.t0_ms = self.t1_ms
            self.t1_ms = pygame.time.get_ticks()
            self.dt = (self.t1_ms - self.t0_ms) / 1000.0

            self.events = list(pygame.event.get())
            self.keys_pressed = pygame.key.get_pressed()

            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Create a bullet at the current player position
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player_shoot(self.player)

            # Move players, etc.
            self.tick()

            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            # Draw characters:
            self.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate at 60 FPS
            self.clock.tick(self.frame_rate)

    #############################################################

    def tick(self):
        # Update player position:
        player = self.player
        self.tick_player(player)
        # self.player.think(dt)

        # Update bullet positions:
        for bullet in self.bullets:
            self.tick_entity(bullet)
        self.bullets = [bullet for bullet in self.bullets if self.enemy_bounds.contains(bullet.pos)]

        # Spawn enemy:
        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_timer > self.enemy_spawn_time:
            enemy = self.make_enemy()
            self.enemies.append(enemy)
            self.enemy_timer = current_time

        # Update enemy positions and spawn new ones
        for enemy in self.enemies:
            self.tick_entity(enemy)
            # enemy.think(dt)

        # Remove enemies that are off the screen
        self.enemies = [enemy for enemy in self.enemies if self.enemy_bounds.contains(enemy.pos)]

        # Check for collisions
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                rect_1 = bullet.sprite.rect
                rect_2 = enemy.sprite.rect
                if check_collision(rect_1, rect_2):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break

    #############################################################

    def draw(self):
        screen = self.screen

        # Draw the bullets
        for bullet in self.bullets:
            bullet.draw(screen)

        # Draw the player
        self.player.draw(screen)

        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw(screen)

    #############################################################

    def tick_player(self, player):
        player_pos_ = player.pos
        self.player_control(player)
        self.tick_entity(player)
        # self.player.think(dt)
        if not self.screen_bounds.contains(player.pos):
            player.pos = player_pos_
            player.vel = V()

    def player_control(self, player):
        'Handle player movement.'
        vel = V()
        if self.screen_bounds.contains(player.pos):
            keys = self.keys_pressed
            if keys[pygame.K_a]:
                vel.x -= player.quickness
            if keys[pygame.K_d]:
                vel.x += player.quickness
            if keys[pygame.K_w]:
                vel.y -= player.quickness
            if keys[pygame.K_s]:
                vel.y += player.quickness
        player.vel = vel

    def player_shoot(self, player):
        'Player shoots.'
        bullet_x = player.pos.x
        bullet_y = player.rect.top
        bullet_color = (255, 255, 255)
        bullet = Bullet(
            V(bullet_x, bullet_y),
            V(0.0, - self.bullet_speed),
            Sprite(
                V(self.bullet_width, self.bullet_height),
                bullet_color,
            ),
            game=self,
        )
        self.bullets.append(bullet)

    def tick_entity(self, entity):
        'Tick entity behavior.'
        entity.dt = self.dt
        entity.tick()

    def make_player(self):
        player_x = self.screen_width // 2 - self.player_width // 2
        player_y = self.screen_height - self.player_height - 10
        player_color = (0, 128, 255)
        sprite = Sprite(
            V(self.player_width, self.player_height),
            player_color,
        )
        player = Player(
            V(player_x, player_y),
            V(0.0, 0.0),
            sprite,
            quickness=self.player_speed,
        )
        player.game = self
        return player

    def make_enemy(self):
        enemy_x = random.randint(self.enemy_width, self.screen_width - self.enemy_width)
        enemy_y = - self.enemy_height
        enemy_color = (255, 0, 0)
        sprite = Sprite(
            V(self.enemy_width, self.enemy_height),
            enemy_color,
        )
        enemy = Enemy(
            V(enemy_x, enemy_y),
            V(0.0, self.enemy_speed),
            sprite,
            player=self.player,
            programs=self.make_enemy_programs(),
            max_speed=self.enemy_speed * 4,
            game=self,
        )
        return enemy

    def make_enemy_programs(self):
        programs = [
            Program(
                'randomize_direction',
                [
                    # Accelerate random X direction:
                    ('const', V(-50.0, 0.0)),
                    ('const', V( 50.0, 0.0)),
                    'rand',
                    'acc',
                    ('const', 0.5),
                    'sleep',

                    # Accelerate random Y direction:
                    ('const', V(0.0, -50.0)),
                    ('const', V(0.0,  50.0)),
                    'rand',
                    'acc',
                    ('const', 0.5),
                    'sleep',
                ],
            ),
            Program(
                'avoid_bullets',
                [
                    ('const', V(0.1, 0.1)),
                    # 'rand',
                    'sleep',
                    ('call', 'avoid_bullets'),
                ]
            ),
            Program(
                'move_toward_player',
                [
                    ('const', V(0.2, 0.9)),
                    'rand',
                    'sleep',

                    ('const', 0.1),
                    'sleep',
                    ('call', 'move_toward_player'),
                    ('const', 0.1),
                    'sleep',
                    ('call', 'move_toward_player'),
                    ('const', 0.1),
                    'sleep',
                    ('call', 'move_toward_player'),
                ],
            ),
        ]
        return programs

if __name__ == '__main__':
    game = Game()
    game.init()
    game.run()

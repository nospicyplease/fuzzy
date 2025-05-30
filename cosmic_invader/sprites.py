"""Sprite classes for Cosmic Invader."""

from __future__ import annotations

import pygame
from typing import List

from .resources import load_image

GRID_WIDTH = 40
GRID_HEIGHT = 20
CELL_WIDTH = 24
CELL_HEIGHT = 27


class Player(pygame.sprite.Sprite):
    """The player's ship."""

    def __init__(self, bullet_group: pygame.sprite.Group, images: List[pygame.Surface]):
        super().__init__()
        self.images = images
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (GRID_WIDTH * CELL_WIDTH // 2, (GRID_HEIGHT - 2) * CELL_HEIGHT)
        self.bullets = bullet_group
        self.cooldown = 0.0
        self.anim_time = 0.0
        self.frame_time = 0.1

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_LEFT] and self.rect.left > CELL_WIDTH:
            self.rect.x -= CELL_WIDTH
        if keys[pygame.K_RIGHT] and self.rect.right < (GRID_WIDTH - 1) * CELL_WIDTH:
            self.rect.x += CELL_WIDTH
        if keys[pygame.K_SPACE] and self.cooldown <= 0.0:
            bullet = Bullet(self.rect.centerx, self.rect.top - CELL_HEIGHT // 2)
            self.bullets.add(bullet)
            self.cooldown = 0.2
        self.cooldown -= dt

        self.anim_time += dt
        if self.anim_time >= self.frame_time:
            self.anim_time -= self.frame_time
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]


class Alien(pygame.sprite.Sprite):
    """An alien enemy."""

    def __init__(self, images: List[pygame.Surface], x: int, y: int):
        super().__init__()
        self.images = images
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.grid_x = x
        self.grid_y = y
        self.update_position()
        self.anim_time = 0.0
        self.frame_time = 0.2

    def update_position(self) -> None:
        self.rect.topleft = (self.grid_x * CELL_WIDTH, self.grid_y * CELL_HEIGHT)

    def update(self, dt: float) -> None:
        self.anim_time += dt
        if self.anim_time >= self.frame_time:
            self.anim_time -= self.frame_time
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]


class Bullet(pygame.sprite.Sprite):
    """Projectile fired by the player."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = load_image('assets/bullet.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.grid_y = self.rect.y // CELL_HEIGHT

    def update(self, dt: float) -> None:
        self.rect.y -= CELL_HEIGHT
        self.grid_y = self.rect.y // CELL_HEIGHT
        if self.rect.bottom < CELL_HEIGHT:
            self.kill()


class BackgroundLayer:
    """Scrolling background layer."""

    def __init__(self, image: pygame.Surface, speed: float):
        self.image = image
        self.speed = speed
        self.offset = 0.0
        self.width = image.get_width()
        self.height = image.get_height()

    def update(self, dt: float) -> None:
        self.offset = (self.offset + self.speed * dt) % self.height

    def draw(self, surface: pygame.Surface) -> None:
        y = -self.offset
        while y < RESOLUTION[1]:
            surface.blit(self.image, (0, y))
            y += self.height

RESOLUTION = (960, 540)

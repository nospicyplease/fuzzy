import pygame
from .utils import load_image

GRAVITY = 0.8
MAX_FALL_SPEED = 12

class Enemy(pygame.sprite.Sprite):
    """Simple walking enemy."""
    def __init__(self, pos, image_path="assets/enemy.png"):
        super().__init__()
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = -1
        self.speed = 2
        self.vel_y = 0

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

    def update(self, level):
        # horizontal movement
        self.rect.x += self.direction * self.speed
        for tile in level.get_collidable_tiles(self.rect):
            if self.direction > 0:
                self.rect.right = tile.left
                self.direction = -1
            elif self.direction < 0:
                self.rect.left = tile.right
                self.direction = 1

        # vertical movement
        self.apply_gravity()
        self.rect.y += self.vel_y
        for tile in level.get_collidable_tiles(self.rect):
            if self.vel_y > 0:
                self.rect.bottom = tile.top
                self.vel_y = 0
            elif self.vel_y < 0:
                self.rect.top = tile.bottom
                self.vel_y = 0

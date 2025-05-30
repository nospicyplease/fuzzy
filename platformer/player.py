import pygame
from .utils import load_image

GRAVITY = 0.8
MAX_FALL_SPEED = 12

class Player(pygame.sprite.Sprite):
    """Player controlled character."""
    def __init__(self, pos, image_path="assets/player.png"):
        super().__init__()
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(topleft=pos)
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 16
        self.on_ground = False

    def handle_input(self, keys):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed if dx == 0 else dx
        return dx

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

    def update(self, keys, level):
        dx = self.handle_input(keys)
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()

        # horizontal movement
        self.rect.x += dx
        for tile in level.get_collidable_tiles(self.rect):
            if dx > 0:
                self.rect.right = tile.left
            elif dx < 0:
                self.rect.left = tile.right

        # vertical movement
        self.apply_gravity()
        self.rect.y += self.vel_y
        collided = False
        for tile in level.get_collidable_tiles(self.rect):
            collided = True
            if self.vel_y > 0:
                self.rect.bottom = tile.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = tile.bottom
                self.vel_y = 0
        if not collided:
            self.on_ground = False

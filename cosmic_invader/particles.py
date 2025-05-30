"""Particle effects for Cosmic Invader."""

from __future__ import annotations

import pygame
from typing import List

from .resources import load_spritesheet


class Explosion(pygame.sprite.Sprite):
    """Animated explosion sprite using a spritesheet."""

    def __init__(self, pos: pygame.Vector2, frames: List[pygame.Surface]):
        super().__init__()
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0.0
        self.frame_time = 0.04

    def update(self, dt: float) -> None:
        self.timer += dt
        while self.timer >= self.frame_time:
            self.timer -= self.frame_time
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
                return
            self.image = self.frames[self.index]
            self.rect = self.image.get_rect(center=self.rect.center)

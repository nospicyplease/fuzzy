import pygame
import os


def load_image(path, size=(32, 32), color=(255, 0, 0)):
    """Load an image or create a colored placeholder."""
    base = os.path.dirname(__file__)
    full_path = os.path.join(base, path)
    if os.path.exists(full_path):
        return pygame.image.load(full_path).convert_alpha()
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

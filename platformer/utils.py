import os
import pygame

def load_image(name, size, color):
    """Load image from assets or create a placeholder surface."""
    path = os.path.join(os.path.dirname(__file__), 'assets', name)
    try:
        image = pygame.image.load(path).convert_alpha()
    except Exception:
        image = pygame.Surface(size)
        image.fill(color)
    return image

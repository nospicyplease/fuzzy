import pygame
import os

def load_image(path, size=(32,32), col=(255,0,255)):
    """Load an image or return colored placeholder surface if file missing."""
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception:
        surf = pygame.Surface(size)
        surf.fill(col)
        return surf

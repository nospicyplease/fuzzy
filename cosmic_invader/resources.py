"""Resource loading helpers for Cosmic Invader."""

from __future__ import annotations

import pygame
from typing import Dict, List, Tuple, Optional

_image_cache: Dict[str, pygame.Surface] = {}


def load_image(path: str, colorkey: Optional[Tuple[int, int, int]] = None) -> pygame.Surface:
    """Load an image from disk, caching the result.

    Args:
        path: Path to the image file.
        colorkey: Color to treat as transparent. If None, alpha is preserved.

    Returns:
        Loaded ``pygame.Surface``.
    """
    if path not in _image_cache:
        image = pygame.image.load(path)
        if colorkey is not None:
            image = image.convert()
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        _image_cache[path] = image
    return _image_cache[path]


def load_spritesheet(path: str, rows: int, cols: int) -> List[pygame.Surface]:
    """Load a spritesheet and split it into frames.

    Args:
        path: Path to the spritesheet image.
        rows: Number of rows in the atlas.
        cols: Number of columns in the atlas.

    Returns:
        List of frames as ``pygame.Surface`` objects.
    """
    sheet = load_image(path)
    width = sheet.get_width() // cols
    height = sheet.get_height() // rows
    frames = []
    for j in range(rows):
        for i in range(cols):
            rect = pygame.Rect(i * width, j * height, width, height)
            frame = sheet.subsurface(rect).copy()
            frames.append(frame)
    return frames

import pygame
import os
from enemy import Enemy

TILE_SIZE = 32

class Level:
    """Map that holds tiles, enemies, and goal."""
    def __init__(self, map_data):
        self.map_data = map_data
        self.width = len(map_data[0]) * TILE_SIZE
        self.height = len(map_data) * TILE_SIZE

        base = os.path.dirname(__file__)
        self.ground_img = pygame.image.load(os.path.join(base, 'assets', 'ground.png')).convert_alpha()
        self.platform_img = pygame.image.load(os.path.join(base, 'assets', 'platform.png')).convert_alpha()
        self.flag_img = pygame.image.load(os.path.join(base, 'assets', 'flagpole.png')).convert_alpha()

        self.tiles = []  # list of dict {'rect': rect, 'img': surface}
        self.enemy_positions = []
        self.flag_rect = None
        self.start_pos = (0, 0)
        self._parse_map()

    def _parse_map(self):
        for row_index, row in enumerate(self.map_data):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'G':
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.tiles.append({'rect': rect, 'img': self.ground_img})
                elif cell == 'P':
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.tiles.append({'rect': rect, 'img': self.platform_img})
                elif cell == 'F':
                    self.flag_rect = self.flag_img.get_rect(bottomleft=(x, y + TILE_SIZE))
                elif cell == 'E':
                    self.enemy_positions.append((x, y))
                elif cell == 'S':
                    self.start_pos = (x, y)

    def create_enemies(self):
        enemies = pygame.sprite.Group()
        for pos in self.enemy_positions:
            enemies.add(Enemy(pos))
        return enemies

    def get_collidable_tiles(self, rect):
        return [t['rect'] for t in self.tiles if rect.colliderect(t['rect'])]

    def draw(self, surface, offset_x):
        for tile in self.tiles:
            rect = tile['rect'].copy()
            rect.x -= offset_x
            surface.blit(tile['img'], rect)
        if self.flag_rect:
            rect = self.flag_rect.copy()
            rect.x -= offset_x
            surface.blit(self.flag_img, rect)

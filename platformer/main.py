import pygame
from .player import Player
from .level import Level, TILE_SIZE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Basic tile map. S=start, G=ground, P=platform, E=enemy, F=flag
MAP_DATA = [
    "............................................................................................",
    "............................................................................................",
    "............................P...............................................................",
    ".................................................................E..........................",
    "..........................................P.................................................",
    ".........................................................F..................................",
    "................................................P........................................S..",
    "............................................................................................",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
]


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    level = Level(MAP_DATA)
    player = Player(level.start_pos)
    enemies = level.create_enemies()

    all_sprites = pygame.sprite.Group(player, enemies)

    running = True
    win = False
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys, level)
        enemies.update(level)

        # Check collision with enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            # Reset player to start if hit
            player.rect.topleft = level.start_pos
            player.vel_y = 0

        # Check for level completion
        if level.flag_rect and player.rect.colliderect(level.flag_rect):
            win = True
            running = False

        # Camera follows player
        offset_x = player.rect.centerx - SCREEN_WIDTH // 2
        offset_x = max(0, min(offset_x, level.width - SCREEN_WIDTH))

        screen.fill((92, 148, 252))  # sky blue background
        level.draw(screen, offset_x)
        for sprite in all_sprites:
            rect = sprite.rect.copy()
            rect.x -= offset_x
            screen.blit(sprite.image, rect)

        pygame.display.flip()

    if win:
        font = pygame.font.SysFont(None, 72)
        text = font.render("You Win!", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        pygame.display.flip()
        pygame.time.wait(3000)
    pygame.quit()


if __name__ == "__main__":
    main()

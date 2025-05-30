"""Pygame remake of the terminal Cosmic Invader game."""

from __future__ import annotations

import pygame
import pygame.freetype
from typing import List

from .resources import load_image, load_spritesheet
from .sprites import (
    Player,
    Alien,
    Bullet,
    BackgroundLayer,
    GRID_WIDTH,
    GRID_HEIGHT,
    CELL_WIDTH,
    CELL_HEIGHT,
    RESOLUTION,
)
from .particles import Explosion

TICK_TIME = 0.1


def create_aliens(frames: List[pygame.Surface], num: int) -> pygame.sprite.Group:
    group = pygame.sprite.Group()
    padding = (GRID_WIDTH - num) // 2
    y = 2
    for i in range(num):
        alien = Alien(frames, padding + i, y)
        group.add(alien)
    return group


def apply_bloom(surface: pygame.Surface) -> pygame.Surface:
    """Simple bloom effect using scaled blurring."""
    small = pygame.transform.smoothscale(surface, (surface.get_width() // 2, surface.get_height() // 2))
    blur = pygame.transform.smoothscale(small, surface.get_size())
    bloom = surface.copy()
    bloom.blit(blur, (0, 0), special_flags=pygame.BLEND_ADD)
    return bloom


def apply_scanlines(surface: pygame.Surface) -> None:
    """Overlay scanlines onto the given surface."""
    line = pygame.Surface((surface.get_width(), 2), pygame.SRCALPHA)
    line.fill((0, 0, 0, 40))
    for y in range(0, surface.get_height(), 4):
        surface.blit(line, (0, y))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
    render = pygame.Surface(RESOLUTION)
    clock = pygame.time.Clock()

    font = pygame.freetype.Font("assets/ui_font.ttf", 48)

    player_frames = load_spritesheet("assets/player.png", 1, 4)
    alien_frames = load_spritesheet("assets/alien.png", 1, 4)
    explosion_frames = load_spritesheet("assets/explosion.png", 5, 5)

    far = BackgroundLayer(load_image("assets/starfield_far.png"), 10)
    mid = BackgroundLayer(load_image("assets/starfield_mid.png"), 20)
    near = BackgroundLayer(load_image("assets/starfield_near.png"), 40)

    bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    aliens = create_aliens(alien_frames, 8)
    player = Player(bullets, player_frames)

    alien_dir = 1
    running = True
    win = False
    logic_accum = 0.0
    score = 0
    display_score = 0
    shake = 0.0

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        keys = pygame.key.get_pressed()
        logic_accum += dt
        while logic_accum >= TICK_TIME:
            logic_accum -= TICK_TIME
            # player input
            if keys[pygame.K_LEFT] and player.rect.left > CELL_WIDTH:
                player.rect.x -= CELL_WIDTH
            if keys[pygame.K_RIGHT] and player.rect.right < (GRID_WIDTH - 1) * CELL_WIDTH:
                player.rect.x += CELL_WIDTH
            if keys[pygame.K_SPACE] and player.cooldown <= 0.0:
                bullet = Bullet(player.rect.centerx, player.rect.top - CELL_HEIGHT // 2)
                bullets.add(bullet)
                player.cooldown = 0.2
            player.cooldown -= TICK_TIME

            # update bullets
            for bullet in list(bullets):
                bullet.rect.y -= CELL_HEIGHT
                if bullet.rect.bottom < CELL_HEIGHT:
                    bullet.kill()
                    continue
                bullet_x = bullet.rect.centerx // CELL_WIDTH
                bullet_y = bullet.rect.centery // CELL_HEIGHT
                hit = None
                for alien in aliens:
                    if alien.grid_x == bullet_x and alien.grid_y == bullet_y:
                        hit = alien
                        break
                if hit:
                    aliens.remove(hit)
                    explosion = Explosion(hit.rect.center, explosion_frames)
                    explosions.add(explosion)
                    bullets.remove(bullet)
                    score += 1

            # update aliens
            moved = []
            edge = False
            for alien in aliens:
                nx = alien.grid_x + alien_dir
                if nx <= 1 or nx >= GRID_WIDTH - 1:
                    edge = True
                moved.append((alien, nx))
            if edge:
                for alien in aliens:
                    alien.grid_y += 1
                alien_dir *= -1
            for alien, nx in moved:
                alien.grid_x = nx if not edge else alien.grid_x
            for alien in aliens:
                alien.update_position()
                if alien.grid_y >= GRID_HEIGHT - 2:
                    running = False
                    shake = 0.5

            if not aliens:
                running = False
                win = True

        # per-frame updates
        far.update(dt)
        mid.update(dt)
        near.update(dt)
        player.update(dt, keys)
        aliens.update(dt)
        bullets.update(dt)
        explosions.update(dt)

        if display_score < score:
            display_score += 1

        render.fill((0, 0, 0))
        far.draw(render)
        mid.draw(render)
        near.draw(render)
        aliens.draw(render)
        bullets.draw(render)
        explosions.draw(render)
        render.blit(player.image, player.rect)
        font.render_to(render, (10, 10), f"Score {display_score}", (255, 255, 255))

        frame = apply_bloom(render)
        apply_scanlines(frame)

        if shake > 0.0:
            shake -= dt
            offset_x = int((shake * 10) * (-1 if int(shake * 20) % 2 else 1))
            offset_y = int((shake * 10) * (-1 if int(shake * 15) % 2 else 1))
            shaken = pygame.Surface(RESOLUTION)
            shaken.blit(frame, (offset_x, offset_y))
            frame = shaken

        scaled = pygame.transform.smoothscale(frame, screen.get_size())
        screen.blit(scaled, (0, 0))
        pygame.display.flip()

    # final screen
    render.fill((0, 0, 0))
    text = "YOU WIN!" if win else "GAME OVER"
    rect = font.get_rect(text)
    pos = (RESOLUTION[0] // 2 - rect.width // 2, RESOLUTION[1] // 2 - rect.height // 2)
    font.render_to(render, pos, text, (255, 255, 255))
    frame = apply_bloom(render)
    apply_scanlines(frame)
    scaled = pygame.transform.smoothscale(frame, screen.get_size())
    screen.blit(scaled, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()


if __name__ == "__main__":
    main()

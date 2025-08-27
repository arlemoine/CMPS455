import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Window size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Float Movement & Collisions Demo")

clock = pygame.time.Clock()

# World scaling / camera
camera_x, camera_y = 0.0, 0.0  # top-left of camera in world coords
scale = 1  # 1 world unit = 1 pixel

# Player setup
player = {"x": 400.0, "y": 300.0, "radius": 15.0, "speed": 200.0}  # speed in units/sec

# Enemies
enemies = []
for _ in range(10):
    enemies.append({
        "x": random.uniform(0, 2000),
        "y": random.uniform(0, 2000),
        "radius": 20
    })

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement (arrow keys)
    keys = pygame.key.get_pressed()
    dx, dy = 0.0, 0.0
    if keys[pygame.K_RIGHT]:
        dx -= 1
    if keys[pygame.K_LEFT]:
        dx += 1
    if keys[pygame.K_DOWN]:
        dy -= 1
    if keys[pygame.K_UP]:
        dy += 1
    # Normalize to prevent faster diagonal
    if dx != 0 or dy != 0:
        length = math.hypot(dx, dy)
        dx /= length
        dy /= length
    # Update float positions
    player["x"] += dx * player["speed"] * dt
    player["y"] += dy * player["speed"] * dt

    # Camera follows player (centered)
    camera_x = player["x"] - WIDTH / 2
    camera_y = player["y"] - HEIGHT / 2

    # Clear screen
    screen.fill((30, 30, 30))

    # Draw enemies
    for e in enemies:
        # Collision check (circle)
        dist = math.hypot(e["x"] - player["x"], e["y"] - player["y"])
        color = (255, 0, 0) if dist < player["radius"] + e["radius"] else (0, 200, 0)
        screen_x = int((e["x"] - camera_x) * scale)
        screen_y = int((e["y"] - camera_y) * scale)
        pygame.draw.circle(screen, color, (screen_x, screen_y), int(e["radius"]*scale))

    # Draw player
    player_screen_x = int((player["x"] - camera_x) * scale)
    player_screen_y = int((player["y"] - camera_y) * scale)
    pygame.draw.circle(screen, (0, 0, 255), (player_screen_x, player_screen_y), int(player["radius"]*scale))

    pygame.display.flip()

pygame.quit()

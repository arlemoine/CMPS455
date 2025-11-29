import pygame
import random
import sys

# --- Game Setup ---
pygame.init()
# Larger window, 16:9 aspect ratio, close to full screen
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner with Monster Chase")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont(None, 48)

# Player
player_width, player_height = 40, 100  # taller player for ducking
player_x = 200
player_y = HEIGHT - player_height - 100
player_vel_y = 0
GRAVITY = 1
jump_power = -18
on_ground = True
is_ducking = False
duck_height = 50

# Monster
monster_width, monster_height = 60, 100
monster_x = 50
monster_y = HEIGHT - monster_height - 100
monster_speed = 9  # match player's top speed

# Obstacles
obstacles = []
spawn_timer = 0

# Speeds
base_speed = monster_speed  # top speed = monster
speed = base_speed
speed_penalty = 0

# Camera offset
camera_offset = 250  # see more behind player

# Ground
GROUND_HEIGHT = 100

# Score
score = 0

# --- Game Loop ---
run = True
while run:
    clock.tick(60)
    WIN.fill(WHITE)

    # --- Events ---
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Jump
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = jump_power
        on_ground = False
        is_ducking = False

    # Duck
    if keys[pygame.K_DOWN] and on_ground:
        is_ducking = True
    else:
        is_ducking = False

    # --- Physics ---
    player_vel_y += GRAVITY
    player_y += player_vel_y

    # Ground collision
    if player_y >= HEIGHT - player_height - GROUND_HEIGHT:
        player_y = HEIGHT - player_height - GROUND_HEIGHT
        player_vel_y = 0
        on_ground = True

    # Speed penalty
    if speed_penalty > 0:
        speed_penalty -= 0.1
    else:
        speed_penalty = 0
    speed = base_speed - speed_penalty

    # Spawn obstacles
    spawn_timer += 1
    if spawn_timer > 60:
        spawn_timer = 0
        obstacle_type = random.choice(['jump', 'duck', 'hole'])
        x_pos = player_x + WIDTH + camera_offset
        if obstacle_type == 'jump':
            h = random.randint(40, 80)
            obstacles.append([x_pos, HEIGHT - h - GROUND_HEIGHT, 30, h, 'jump'])
        elif obstacle_type == 'duck':
            obstacles.append([x_pos, HEIGHT - 180 - GROUND_HEIGHT, 30, 60, 'duck'])
        elif obstacle_type == 'hole':
            obstacles.append([x_pos, HEIGHT - GROUND_HEIGHT, 100, GROUND_HEIGHT, 'hole'])

    # Move obstacles
    for obs in obstacles:
        obs[0] -= speed

    # Remove offscreen obstacles
    obstacles = [o for o in obstacles if o[0] > -150]

    # Monster movement
    monster_x += speed * 0.4

    # Player rect
    current_height = duck_height if is_ducking else player_height
    player_rect = pygame.Rect(player_x, player_y + (player_height - current_height), player_width, current_height)
    monster_rect = pygame.Rect(monster_x, monster_y, monster_width, monster_height)

    # Collision
    for obs in obstacles:
        obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])
        if player_rect.colliderect(obs_rect):
            if obs[4] == 'jump' and not on_ground:
                pass
            elif obs[4] == 'duck' and is_ducking:
                pass
            elif obs[4] == 'hole' and player_rect.bottom < HEIGHT - GROUND_HEIGHT:
                pass
            else:
                speed_penalty = 5

    # Monster catches player
    if player_rect.colliderect(monster_rect):
        print(f"GAME OVER! Final Score: {int(score)}")
        pygame.quit()
        sys.exit()

    # Camera simulation
    cam_shift = speed - 5
    for obs in obstacles:
        obs[0] -= cam_shift
    monster_x -= cam_shift

    # Draw ground
    pygame.draw.rect(WIN, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    # Draw player
    pygame.draw.rect(WIN, GREEN, player_rect)
    # Draw monster
    pygame.draw.rect(WIN, RED, monster_rect)
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(WIN, BLACK, pygame.Rect(obs[0], obs[1], obs[2], obs[3]))

    # Score
    score += 0.1
    score_text = font.render(f"Score: {int(score)}", True, BLUE)
    WIN.blit(score_text, (20, 20))

    # Controls
    controls_text = font.render("SPACE: Jump | DOWN: Duck", True, BLUE)
    WIN.blit(controls_text, (20, 60))

    pygame.display.update()

pygame.quit()

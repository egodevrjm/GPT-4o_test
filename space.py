import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 7

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
ENEMY_SPEED = 2

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont('Arial', 24)

# Load images
player_img = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_img.fill(GREEN)

enemy_img = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_img.fill(WHITE)

bullet_img = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
bullet_img.fill(RED)

# Game variables
player_x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10

bullets = []
enemies = []
enemy_direction = 1
score = 0

# Create enemies
def create_enemies():
    enemies = []
    for row in range(5):
        for col in range(10):
            enemy_x = col * (ENEMY_WIDTH + 10) + 50
            enemy_y = row * (ENEMY_HEIGHT + 10) + 50
            enemies.append(pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT))
    return enemies

enemies = create_enemies()

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player_y, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append(bullet)

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
        player_x += PLAYER_SPEED

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies:
        enemy.x += ENEMY_SPEED * enemy_direction

    # Change enemy direction at edges
    if any(enemy.x >= SCREEN_WIDTH - ENEMY_WIDTH or enemy.x <= 0 for enemy in enemies):
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += ENEMY_HEIGHT

    # Check for bullet collision with enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_img, bullet.topleft)

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_img, enemy.topleft)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
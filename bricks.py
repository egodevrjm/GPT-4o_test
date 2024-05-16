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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, YELLOW]

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 10

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 5

# Brick settings
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLUMNS = 10

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Breaker")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont('Arial', 24)

# Game variables
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - 50

ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = BALL_SPEED
ball_dy = -BALL_SPEED

bricks = []
score = 0
level = 1

# Create bricks
def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick_x = col * (BRICK_WIDTH + 5) + 35
            brick_y = row * (BRICK_HEIGHT + 5) + 50
            bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks

bricks = create_bricks()

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x += PADDLE_SPEED

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
        ball_dx = -ball_dx
    if ball_y <= BALL_RADIUS:
        ball_dy = -ball_dy

    # Ball collision with paddle
    if (paddle_x < ball_x < paddle_x + PADDLE_WIDTH) and (paddle_y < ball_y < paddle_y + PADDLE_HEIGHT):
        ball_dy = -ball_dy

    # Ball collision with bricks
    for brick in bricks:
        if brick.collidepoint(ball_x, ball_y):
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 10
            break

    # Check if ball is out of bounds
    if ball_y > SCREEN_HEIGHT:
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_dx = BALL_SPEED * random.choice([-1, 1])
        ball_dy = -BALL_SPEED
        score = 0
        bricks = create_bricks()
        level = 1

    # Check if all bricks are destroyed
    if not bricks:
        level += 1
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_dx = BALL_SPEED * random.choice([-1, 1])
        ball_dy = -BALL_SPEED
        bricks = create_bricks()

    # Draw paddle
    pygame.draw.rect(screen, YELLOW, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, random.choice(COLORS), brick)

    # Draw score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 100, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
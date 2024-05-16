import pygame
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60

# Ball dimensions
BALL_SIZE = 10

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 35)

# Game objects
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
player_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Speeds
ball_speed_x = 7
ball_speed_y = 7
paddle_speed = 7

# Scores
player_score = 0
opponent_score = 0

# Video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('pong_game.mp4', fourcc, 30.0, (WIDTH, HEIGHT))

def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (WIDTH//2 + 20, 10))
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (WIDTH//2 - 50, 10))

def move_ball():
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    if ball.left <= 0:
        player_score += 1
        reset_ball()

    if ball.right >= WIDTH:
        opponent_score += 1
        reset_ball()

def move_paddles():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and opponent_paddle.top > 0:
        opponent_paddle.y -= paddle_speed
    if keys[pygame.K_s] and opponent_paddle.bottom < HEIGHT:
        opponent_paddle.y += paddle_speed
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += paddle_speed

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1
    ball_speed_y *= -1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_ball()
    move_paddles()
    draw_objects()

    # Capture the frame
    frame = pygame.surfarray.array3d(screen)
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    out.write(frame)

    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Clean up
pygame.quit()
out.release()
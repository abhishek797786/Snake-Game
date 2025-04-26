import pygame
import random

# Initialize Pygame
pygame.init()
# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 270, 15
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 20
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
MAX_LEVEL = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (255, 255, 0)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_level(level):
    paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
    ball_speed = [random.choice((BALL_SPEED_X, -BALL_SPEED_X)), BALL_SPEED_Y]
    
    bricks = []
    for i in range(10):
        for j in range(6):
            brick = pygame.Rect(i * (BRICK_WIDTH + 2), j * (BRICK_HEIGHT + 2) + 50, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    
    return paddle, ball, ball_speed, bricks

# Game variables
level = 1
lives = 3
score = 0
game_over = False

paddle, ball, ball_speed, bricks = reset_level(level)

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += PADDLE_SPEED
        
        # Move the ball
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]
        
        # Collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        
        # Collision with paddle
        if ball.colliderect(paddle) and ball_speed[1] > 0:
            ball_speed[1] = -ball_speed[1]
        
        # Collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speed[1] = -ball_speed[1]
                score += 10
        
        # Level completion
        if len(bricks) == 0:
            level += 1
            if level > MAX_LEVEL:
                game_over = True
            else:
                paddle, ball, ball_speed, bricks = reset_level(level)
        
        # Ball out of bounds
        if ball.top >= HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                paddle, ball, ball_speed, bricks = reset_level(level)
    
    # Draw everything
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.circle(screen, RED, ball.center, BALL_RADIUS)
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
        
    
    draw_text(f"Score: {score}", WHITE, 10, 10)
    draw_text(f"Lives: {lives}", WHITE, WIDTH - 120, 10)
    if game_over:
        draw_text("Game Over!", WHITE, WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Press SPACE to play again", WHITE, WIDTH // 2 - 180, HEIGHT // 2 + 50)
    
    pygame.display.flip()
    clock.tick(60)

    # Game over handling
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            level = 1
            lives = 3
            score = 0
            game_over = False
            paddle, ball, ball_speed, bricks = reset_level(level)

pygame.quit()
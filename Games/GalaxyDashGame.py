import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Space Runner")
clock = pygame.time.Clock()

# Fonts and Colors
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
RED = (255, 50, 50)
CYAN = (0, 255, 255)

# Load music
try:
    pygame.mixer.music.load("win.wav")
    pygame.mixer.music.play(-1)
except:
    print("Music file not found.")

# Player
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 5
boost_active = False
boost_timer = 0
shield_active = False
shield_timer = 0
lives = 0

# Game variables
asteroids = []
stars = []
extra_lives = []
score = 0
high_score = 0
game_over = False

# Create stars and asteroids
def spawn_asteroid():
    x = random.randint(0, WIDTH - 40)
    rect = pygame.Rect(x, -40, 40, 40)
    asteroids.append(rect)

def spawn_star():
    x = random.randint(0, WIDTH - 20)
    rect = pygame.Rect(x, -20, 20, 20)
    stars.append(rect)

def spawn_extra_life():
    x = random.randint(20, WIDTH - 40)
    rect = pygame.Rect(x, -20, 30, 30)
    extra_lives.append(rect)

def reset_game():
    global asteroids, stars, extra_lives, player_x, player_y, score, game_over, boost_active, boost_timer, lives, shield_active, shield_timer
    asteroids = []
    stars = []
    extra_lives = []
    player_x = WIDTH // 2
    player_y = HEIGHT - 60
    score = 0
    game_over = False
    boost_active = False
    boost_timer = 0
    lives = 0
    shield_active = False
    shield_timer = 0

# Draw triangle spaceship
def draw_spaceship(x, y):
    points = [(x, y), (x - 20, y + 40), (x + 20, y + 40)]
    pygame.draw.polygon(screen, NEON_PINK if boost_active else NEON_BLUE, points)
    if shield_active:
        pygame.draw.circle(screen, (0, 255, 255, 80), (x, y + 20), 40, 4)

# Draw game
def draw_game():
    screen.fill((10, 10, 30))
    draw_spaceship(player_x, player_y)

    for asteroid in asteroids:
        pygame.draw.circle(screen, RED, asteroid.center, 20)
    for star in stars:
        pygame.draw.circle(screen, NEON_GREEN, star.center, 10)
    for life in extra_lives:
        pygame.draw.polygon(screen, NEON_PINK, [(life.centerx, life.top), (life.left, life.bottom), (life.right, life.bottom)])

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 40))
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 70))

    if boost_active:
        boost_text = font.render("BOOST!", True, CYAN)
        screen.blit(boost_text, (WIDTH - 150, 10))

    pygame.display.update()

# Show Game Over Screen
def show_game_over():
    screen.fill((10, 10, 30))
    over_text = big_font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    prompt_text = font.render("Press R to Replay or Q to Quit", True, NEON_BLUE)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.update()

spawn_timer = 0
running = True
while running:
    clock.tick(60)
    if not game_over:
        spawn_timer += 1
        if spawn_timer % 40 == 0:
            spawn_asteroid()
        if spawn_timer % 80 == 0:
            spawn_star()
        if spawn_timer % 500 == 0:
            spawn_extra_life()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= player_speed * (2 if boost_active else 1)
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 20:
            player_x += player_speed * (2 if boost_active else 1)
        if keys[pygame.K_SPACE]:
            boost_active = True
            boost_timer = 60

        if boost_timer > 0:
            boost_timer -= 1
        else:
            boost_active = False

        if shield_timer > 0:
            shield_timer -= 1
        else:
            shield_active = False

        for asteroid in asteroids[:]:
            asteroid.y += 5
            if math.hypot(asteroid.centerx - player_x, asteroid.centery - player_y) < 30:
                if shield_active:
                    asteroids.remove(asteroid)
                else:
                    asteroids.remove(asteroid)
                    lives -= 1
                    if lives < 0:
                        game_over = True
                        if score > high_score:
                            high_score = score
            elif asteroid.top > HEIGHT:
                asteroids.remove(asteroid)

        for star in stars[:]:
            star.y += 3
            if math.hypot(star.centerx - player_x, star.centery - player_y) < 30:
                stars.remove(star)
                score += 10
            elif star.top > HEIGHT:
                stars.remove(star)

        for life in extra_lives[:]:
            life.y += 2
            if math.hypot(life.centerx - player_x, life.centery - player_y) < 30:
                extra_lives.remove(life)
                lives += 1
                shield_active = True
                shield_timer = 180
            elif life.top > HEIGHT:
                extra_lives.remove(life)

        draw_game()

    else:
        show_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    running = False

pygame.quit()
sys.exit()
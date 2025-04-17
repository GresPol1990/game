import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Nikodem vs Iga: Demo')

# Player properties
player_size = 50
player_x, player_y = 100, SCREEN_HEIGHT - player_size - 10
player_vel_y = 0
gravity = 0.5
is_grounded = True
speed = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# Game objects
enemies = []
legos = []
score = 0
clock = pygame.time.Clock()

# Sounds (placeholder files)
try:
    jump_sound = pygame.mixer.Sound('jump.wav')
    collect_sound = pygame.mixer.Sound('collect.wav')
    death_sound = pygame.mixer.Sound('death.wav')
except pygame.error:
    print("Nie udało się załadować plików dźwiękowych.")
    jump_sound = collect_sound = death_sound = None

# Functions
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

def draw_enemy(enemy):
    pygame.draw.rect(screen, RED, (enemy[0], enemy[1], player_size, player_size))

def draw_lego(lego):
    pygame.draw.rect(screen, GREEN, (lego[0], lego[1], 20, 20))

def add_enemy():
    x = SCREEN_WIDTH
    y = SCREEN_HEIGHT - player_size - random.randint(50, 150)
    enemies.append([x, y])

def add_lego():
    x = SCREEN_WIDTH + random.randint(0, 200)
    y = SCREEN_HEIGHT - 20 - random.randint(50, 150)
    legos.append([x, y])

def handle_collisions():
    global score
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    # Collision with enemies
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], player_size, player_size)
        if player_rect.colliderect(enemy_rect):
            if death_sound:
                death_sound.play()
            print("KUPA! Spróbuj jeszcze raz!")
            return True
    # Collision with LEGO
    for lego in legos[:]:
        lego_rect = pygame.Rect(lego[0], lego[1], 20, 20)
        if player_rect.colliderect(lego_rect):
            legos.remove(lego)
            score += 10
            if collect_sound:
                collect_sound.play()
            print("Coo! ...jajeczko")
    return False

def restart_game():
    global player_x, player_y, player_vel_y, is_grounded, enemies, legos, score
    player_x, player_y = 100, SCREEN_HEIGHT - player_size - 10
    player_vel_y = 0
    is_grounded = True
    enemies = []
    legos = []
    score = 0

# Main loop
running = True
add_enemy()
add_lego()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_SPACE] and is_grounded:
        player_vel_y = -10
        is_grounded = False
        if jump_sound:
            jump_sound.play()

    # Gravity & ground check
    player_vel_y += gravity
    player_y += player_vel_y
    if player_y >= SCREEN_HEIGHT - player_size - 10:
        player_y = SCREEN_HEIGHT - player_size - 10
        player_vel_y = 0
        is_grounded = True

    # Limit player movement
    if player_x < 0:
        player_x = 0
    if player_x > SCREEN_WIDTH - player_size:
        player_x = SCREEN_WIDTH - player_size

    # Spawn logic
    if len(enemies) < 5 and random.randint(1, 50) == 1:
        add_enemy()
    if len(legos) < 3 and random.randint(1, 50) == 1:
        add_lego()

    # Collisions
    if handle_collisions():
        font = pygame.font.SysFont('Arial', 36)
        screen.fill(WHITE)
        screen.blit(font.render(f'Koniec gry! Wynik: {score}', True, (0, 0, 0)), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        restart_game()

    # Remove off-screen objects
    enemies = [enemy for enemy in enemies if enemy[0] > -player_size]
    legos = [lego for lego in legos if lego[0] > -20]

    # Draw
    screen.fill(WHITE)
    draw_player(player_x, player_y)
    for enemy in enemies:
        draw_enemy(enemy)
        enemy[0] -= speed // 2
    for lego in legos:
        draw_lego(lego)
        lego[0] -= speed
    # Score
    font = pygame.font.SysFont('Arial', 24)
    screen.blit(font.render(f'Wynik: {score}', True, (0,0,0)), (10,10))
    pygame.display.flip()

pygame.quit()
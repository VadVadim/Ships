import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1200, 700

BLACK = 0, 0, 0
RED = 220, 20, 20
GREEN = 0, 90, 0
BLUE = 70, 70, 255
YELLOW = 255, 200, 0

font = pygame.font.SysFont('Verdana', 20)
game_over_font = pygame.font.SysFont('Verdana', 50)

sea = pygame.display.set_mode(screen)
pygame.display.set_caption('Ships')

bg = pygame.transform.scale(pygame.image.load('sea.jpg').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 2

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)

CREATE_MISSILE = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_MISSILE, 10000)

player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(), (300, 150))
player_rect = pygame.Rect(0, 350, *player.get_size())
player_speed = 10

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy' + str(random.randint(1, 3)) +'.png').convert_alpha(), (180, 180))
    enemy_rect = pygame.Rect(width-100, random.randint(100, height-200), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_missile():
    missile = pygame.transform.scale(pygame.image.load('missile.png').convert_alpha(), (100, 50))
    missile_rect = pygame.Rect(width, random.randint(100, height-200), *missile.get_size())
    missile_speed = random.randint(2, 5)
    return [missile, missile_rect, missile_speed]

enemies = []
missiles = []

is_working = True

while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_MISSILE:
            missiles.append(create_missile())
    
    pressed_keys = pygame.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()
    
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    sea.blit(bg, (bgX, 0))
    sea.blit(bg, (bgX2, 0))
    sea.blit(player, player_rect)

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        sea.blit(enemy[0], enemy[1])

        for missile in missiles:
            missile[1].centerx = enemy[1].centerx
            missile[1].centery = enemy[1].centery
            missile[2] += 1
            missile[1] = missile[1].move(-missile[2], 0)
            sea.blit(missile[0], missile[1])

            if missile[1].left < -500:
                missiles.pop(missiles.index(missile))

            if player_rect.colliderect(missile[1]):
                is_working = False
                sea.blit(game_over_font.render('Game Over', True, BLACK), (width - 700, height - 350))

        if enemy[1].left < -100:
            enemies.pop(enemies.index(enemy))
        
        if player_rect.colliderect(enemy[1]):
            sea.blit(game_over_font.render('Dangerous!!!', True, RED), (width - 700, height - 100))

        if player_rect.collidepoint(enemy[1].centerx, enemy[1].centery):
            is_working = False
            sea.blit(game_over_font.render('Game Over', True, BLACK), (width - 700, height - 350))

    if pressed_keys[K_UP] and not player_rect.top <= 150:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)    

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)
    
    pygame.display.flip()
import pygame
import objects
import random

screen_size = (1280, 720)
game_size = (6400, 720)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
players = pygame.sprite.Group()
coins = pygame.sprite.Group()
platforms = pygame.sprite.Group()
player = objects.Player(120, 50, game_size)
players.add(player)
f = pygame.font.SysFont('arial', 30)

cam = objects.Camera(screen_size, game_size, player)

def create_plat(x, y, players):
    platform = objects.Platform(x, y, players)
    platforms.add(platform)
create_plat(0, 592, players)
create_plat(1280, 592, players)
create_plat(2560, 592, players)
create_plat(3840, 592, players)
create_plat(5120, 592, players)

start_position = (200, 200)
recordik = open('record.txt', 'a+')
rec = recordik.readline()
est = 10
recrd = objects.Record(screen, screen_size, game_size, player, recordik, est, f)

for i in range(5):
    for j in range(5):
        coin = objects.Coin(start_position[0] + j * 50, start_position[1] + i * 50, players)
        coins.add(coin)

keys = {}
print(rec)
is_run = True
while is_run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False

        if event.type == pygame.KEYDOWN:
            keys[event.key] = True

        if event.type == pygame.KEYUP:
            keys[event.key] = False

    if keys.get(pygame.K_ESCAPE, False):
        is_run = False

    players.update(keys)

    coins.update()
    platforms.update()
    cam.update()
    recrd.update()


    screen.fill((143, 255, 255))
    coins.draw(screen)

    players.draw(screen)
    platforms.draw(screen)

    pygame.display.flip()
recordik.close()

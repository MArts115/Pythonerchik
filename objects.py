import pygame
from pygame.sprite import AbstractGroup
import random

class Player(pygame.sprite.Sprite):
    count_coins: int
    count_image: int
    images: []
    velocity: [float, float]
    boost: [float, float]

    def __init__(self, position_x, position_y, game_size: (int, int)):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load('mario-2.png'), pygame.image.load('mario-1.png'),
                       pygame.image.load('mario-0.png'), pygame.image.load('mario.png'),
                       pygame.image.load('mario0.png'), pygame.image.load('mario1.png'),
                       pygame.image.load('mario2.png')]
        for i in range(7):
            self.image = self.images[i]
            self.rect = self.images[i].get_rect()
        self.position = pygame.Rect(position_x, position_y, self.rect.w, self.rect.h)
        self.count_coins = 0
        self.velocity = [0, 0]
        self.boost = [0, 0.3]
        self.game_size = game_size
        self.count_image = 3

    def update(self, keys):
        self.rect.x = self.position.x - Camera.instance.position.x
        self.rect.y = self.position.y - Camera.instance.position.y

        if keys.get(pygame.K_UP):
            self.velocity[1] = -5
            max(self.velocity[1], 20)
        if keys.get(pygame.K_LEFT, False):
            max(self.boost[0], -5)
            self.boost[0] = -0.3

        elif keys.get(pygame.K_RIGHT, False):
            self.boost[0] = 0.3
            min(self.boost[0], 5)
            self.count_image += 1
            if self.count_image > 6:
                self.count_image = 4
            self.image = self.images[random.randint(4, 6)]

        else:
            self.boost[0] = 0
            self.velocity[0] = 0
        self.velocity[0] += self.boost[0]
        self.velocity[1] += self.boost[1]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position.x = max(self.position.x, 0)
        self.position.y = max(self.position.y, 0)
        self.position.right = min(self.position.right, self.game_size[0])
        self.position.bottom = min(self.position.bottom, self.game_size[1])
        self.image = self.images[3]


class Coin(pygame.sprite.Sprite):
    def __init__(self, position_x: int, position_y: int, player_group: AbstractGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("coin.png")
        aspect = self.image.get_rect().h / self.image.get_rect().w
        self.image = pygame.transform.scale(self.image, (20, int(20 * aspect)))
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)
        self.position = pygame.Rect(position_x, position_y, self.rect.w, self.rect.h)
        self.players: list[Player] = player_group

    def update(self):
        self.rect.x = self.position.x - Camera.instance.position.x
        self.rect.y = self.position.y - Camera.instance.position.y

        hits: list[Player] = pygame.sprite.spritecollide(self, self.players, False, pygame.sprite.collide_mask)
        if hits:
            hits[0].count_coins += 1
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, position_x: int, position_y: int, player_group: AbstractGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("nis.png")
        self.rect = self.image.get_rect()
        self.position = pygame.Rect(position_x, position_y, self.rect.w, self.rect.h)
        self.players: list[Player] = player_group

    def update(self):
        self.rect.x = self.position.x - Camera.instance.position.x
        self.rect.y = self.position.y - Camera.instance.position.y

        hits: list[Player] = []
        for i in self.players:
            if self.position.colliderect(i.position) == 1:
                hits.append(i)

        for i in hits:
            a = abs(self.position.left - i.position.right)
            b = abs(self.position.right - i.position.left)
            c = abs(self.position.bottom - i.position.top)
            d = abs(self.position.top - i.position.bottom)
            mn = min(a, b, c, d)
            if mn == a:
                i.position.right = self.position.left
                i.velocity[0] = 0
            elif mn == b:
                i.position.left = self.position.right
                i.velocity[0] = 0
            elif mn == c:
                i.position.top = self.position.bottom
                i.velocity[1] = 0
            else:
                i.position.bottom = self.position.top
                i.velocity[1] = 0


class Camera(pygame.sprite.Sprite):
    instance = None

    def __init__(self, screen_size: (int, int), game_size: (int, int), target: pygame.sprite.Sprite):
        pygame.sprite.Sprite.__init__(self)
        if not Camera.instance:
            Camera.instance = self

        self.screen_size = screen_size
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.position = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        self.game_size = game_size
        self.target = target
        self.rec_pos = pygame.Rect(1180, 20, self.rect.w, self.rect.h)

    def update(self):
        self.position.x = max(self.target.position.centerx - self.screen_size[0] // 2, 0)
        self.position.y = max(self.target.position.centery - self.screen_size[1] // 2, 0)
        self.position.right = min(self.position.right, self.game_size[0])
        self.position.bottom = min(self.position.bottom, self.game_size[1])

class Record(pygame.sprite.Sprite):
    def __init__(self, screen, screen_size: (int, int), game_size: (int, int), target: pygame.sprite.Sprite, recordick,
                 rec, f):
        self.scr = screen
        self.screen_size = screen_size
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.position = pygame.Rect(1180, 20, self.rect.w, self.rect.h)
        self.game_size = game_size
        self.target = target
        self.recordick = recordick
        self.rec = rec
        self.f = f
        self.rec_text = f.render(str(rec), 1, (100, 200, 150))

    def update(self):
        self.position.y = max((self.target.position.centery - self.screen_size[1] // 2) + 20, 0)
        self.position.x = max((self.target.position.centerx - self.screen_size[0] // 2) + 1180, 0)
        self.position.right = min(self.position.right - 100, self.game_size[0] - 100)
        self.position.bottom = min(self.position.bottom - 760, self.game_size[1] - 760)
        self.scr.blit(self.rec_text, (self.position.x, self.position.y))

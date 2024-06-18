import pygame
import sys
import time
from math import fabs
from settings import HEIGHT, WIDTH, FPS
from player import Player
from platform import Platform
from pygame.locals import *
from platformer.game import Game
from platformer.player import Player
from platformer.object import Object
import random
import settings

class Platform(Object):
    def __init__(self, x, y, sprite_file, vx=0, vy=0, width=None, height=None):
        super().__init__(x, y, sprite_file, vx, vy, width, height)

class JumpGame(Game):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Jump game", FPS)
        self.new_state("Intro", self.init_intro, self.intro)
        self.set_state("Intro")
        self.new_state("Game", self.init_game, self.game_script)

    def init_intro(self):
        self.knight = Object(200, 200, "knight.png")
        self.add_object(self.knight)

    def intro(self):
        if self.key_pressed(pygame.K_SPACE):
            self.set_state("Game")
        self.knight.vel = (random.randrange(-1, 1), random.randrange(-1, 1))
        time.sleep(1)

    def init_game(self):
        self.clear()
        self.add_object(Object(0, 0, "pop.png"))
        self.add_object(Platform(0, 410, "bip.png", width=WIDTH))
        self.player = Object(200, 40, "knight.png ")
        self.player.on_ground = False
        self.add_object(self.player)

    def game_script(self):
        if self.key_pressed(pygame.K_LEFT):
            self.player.vel[0] = -settings.SPEED
        elif self.key_pressed(pygame.K_RIGHT):
            self.player.vel[0] = settings.SPEED
        elif self.key_pressed(pygame.K_SPACE) and self.player.on_ground:
            self.player.vel[1] = -settings.JUMP
            self.player.on_ground = False
        for o in self.get_collision(self.player):
            if type(o) == Platform:
                self.player.pos[1] = o.rect[1] - self.player.height
                self.player.on_ground = True
                self.player.vel[1] = 0
        self.player_move()

    def player_move(self):
        if not self.player.on_ground:
            self.player.vel[1] += settings.G
        if self.player.vel[0] < 0:
            self.player.vel[0] *= settings.FRIC
        elif self.player.vel[0] > 0:
            self.player.vel[0] *= settings.FRIC
        if fabs(self.player.vel[0]) < 0.6:
            self.player.vel[0] = 0
        if self.player.pos[0] > WIDTH:
            self.player.pos[0] = 0
        if self.player.pos[0] < 0:
            self.player.pos[0] = WIDTH

j = JumpGame()
j.run()

"""
vec = pygame.math.Vector2  # 2 for two dimensional

background = pygame.image.load("pop.png")

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()

def check(platform, groupies):
    #if pygame.sprite.spritecollideany(platform, groupies):
    #    return True
    #else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (
                    abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        return False
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = None
        C = True

        while C:
            p = Platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
           # print('pl', p.rect.top, p.rect.bottom)
            #for pl in platforms:
             #   print('platforms', pl.rect.top, pl.rect.bottom)
            C = check(p, platforms)

        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)


PT1 = Platform(450, 80)
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

P1 = Player(platforms, coins)

all_sprites.add(PT1)
all_sprites.add(P1)
platforms.add(PT1)

for x in range(random.randint(4,5)):
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        C = check(pl, platforms)
    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)


while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            display_surface.fill((255, 0, 0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

        for coin in coins:
            coin.rect.y += abs(P1.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()

    plat_gen()
    displaysurface.blit(background, (0, 0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123, 255, 0))
    displaysurface.blit(g, (WIDTH / 2, 10))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    for coin in coins:
        displaysurface.blit(coin.image, coin.rect)
        coin.update()

    pygame.display.update()
    FramePerSec.tick(FPS)
"""
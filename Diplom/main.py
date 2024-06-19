import pygame
import sys
import time
from settings import HEIGHT, WIDTH, FPS
from plat import Platform
from pygame.locals import *
from platformer.game import Game
from platformer.object import Object, Text
from player import Player
from plat import Platform
import random
import settings

class Coin(Object):
    def __init__(self, x, y, sprite_file, vx=0, vy=0, width=None, height=None):
        super().__init__(x, y, sprite_file, vx, vy, width, height)
        
class JumpGame(Game):
    '''
    Игра, демонстрирующая движок
    '''
    BACKGROUND = "pop.png" # файлы картинок
    PLATFORM = "bip.png"
    PLAYER = "knight.png"
    COIN = "Coin.png"

    START_X = 200 # начальная позиция игрока
    START_Y = 300
    COIN_SCORE = 5 # очков за монету

    def __init__(self):
        '''
        Инициализация игры, создание состояний
        '''
        super().__init__(WIDTH, HEIGHT, "Jump game", FPS)
        self.new_state("Intro", self.init_intro, self.intro)
        self.set_state("Intro")
        self.new_state("Game", self.init_game, self.game_script)
        self.score = 0

    def init_intro(self):
        '''
        Начало заставки
        '''
        self.knight = Object(self.START_X, self.START_Y, self.PLAYER)
        self.add_object(self.knight)

    def intro(self):
        '''
        Сценарий заставки
        '''
        if self.key_pressed(pygame.K_SPACE):
            self.set_state("Game")
        self.knight.vel = [random.randrange(-1, 1), random.randrange(-1, 1)]
        time.sleep(1)

    def init_game(self):
        '''
        Начало игры
        '''
        self.clear() # очистка объектов
        self.add_object(Object(0, 0, self.BACKGROUND)) # фон
        self.make_platforms()
        self.player = Player(self.START_X, self.START_Y, self.PLAYER)
        self.player.on_ground = False
        self.add_object(self.player)
        t = Text(WIDTH / 2, 10, "Verdana", 20, (123, 255, 0), \
                 lambda: str(self.score))
        self.add_object(t)

    def make_platforms(self):
        self.add_object(Platform(WIDTH / 2 - 225, HEIGHT - 20, self.PLATFORM, width=450, height=80))
        for i in range(random.randint(4,5)):
            while True:
                x = random.randint(0, WIDTH - 10)
                y = random.randint(0, HEIGHT - 30)
                speed = random.randint(-1, 1)
                p = Platform(x, y, self.PLATFORM, vx=speed)
                col = self.get_collision(p, Platform)
                if len(col) == 0:
                    self.add_object(p)
                    if speed == 0:
                        self.add_object(Coin(x + width / 2, y - 50, self.COIN))
                    break

    def game_script(self):
        '''
        Сценарий игры, выполняется каждый кадр
        '''
        # обработка управления игрока
        if self.key_pressed(pygame.K_LEFT):
            self.player.acc[0] = -settings.ACC
        if self.key_pressed(pygame.K_RIGHT):
            self.player.acc[0] = settings.ACC
        if self.key_pressed(pygame.K_SPACE) and self.player.on_ground:
            self.player.vel[1] = -settings.JUMP
            self.player.on_ground = False
        self.player_collision()
        self.player_move()

    def player_collision(self):
        '''
        Логика столкновений игрока с объектами игры.

        С платформой игрок сталкивается только при движении вниз, и тогда он становится на нее, гравитация не действует. Если пересечений нет, то игрок падает.
        Если платформа движется, то игрок перемещается вместе с ней
        Монету игрок забирает.
        '''
        plat_col = self.get_collision(self.player, Platform)
        if len(plat_col) == 0:
            self.player.on_ground = False # падение
        else:
            if self.player.vel[1] > 0:
                self.player.pos[1] = plat_col[0].rect[1] - self.player.height + 1
                self.player.on_ground = True
                self.player.vel[1] = 0
            self.player.pos[0] += plat_col[0].vel[0]
        coins_col = self.get_collision(self.player, Coin)
        if len(coins_col) > 0:
            self.remove_object(coins_col[0])
            self.score += self.COIN_SCORE

    def player_move(self):
        '''
        Логика движения игрока.

        Гравитация если не стоит на платформе. Перемещение по кругу влево-вправо.
        Замедление горизонтального движения.
        '''
        if not self.player.on_ground:
            self.player.vel[1] += settings.G
        if self.player.pos[0] > WIDTH:
            self.player.pos[0] = 0
        if self.player.pos[0] < 0:
            self.player.pos[0] = WIDTH
        self.player.acc[0] += self.player.vel[0] * settings.FRIC                

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

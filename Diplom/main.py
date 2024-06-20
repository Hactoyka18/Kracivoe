import pygame
import time
from settings import HEIGHT, WIDTH, FPS
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
    START_Y = 400
    COIN_SCORE = 5 # очков за монету

    def __init__(self):
        '''
        Инициализация игры, создание состояний
        '''
        super().__init__(WIDTH, HEIGHT, "Jump game", FPS)
        self.new_state("Intro", self.init_intro, self.intro)
        self.set_state("Intro")
        self.new_state("Game", self.init_game, self.game_script)
        self.new_state("End game", self.end_game, self.start_new_game)
        self.score = 0

    def init_intro(self):
        '''
        Начало заставки
        '''
        self.clear()
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
        self.score = 0
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
        '''
        Генерация начальных платформ
        '''
        self.add_object(Platform(0, HEIGHT - 20, self.PLATFORM, width=450, height=80))
        for i in range(random.randint(4,5)):
            self.new_platform(0, HEIGHT - 30)

    def new_platform(self, min_y, max_y):
        '''
        Создание новой платформы с монеткой

        :param min_y: минимальная координата платформы
        :param max_y: максимальная координата платформы
        '''
        while True:
            x = random.randint(0, WIDTH - 10)
            y = random.randint(min_y, max_y)
            width = random.randint(50, 120)
            speed = random.randint(-1, 1)
            p = Platform(x, y, self.PLATFORM, vx=speed, width=width)
            p.pos[1] -= 40
            p.height += 40
            col = self.get_collision(p, Platform)
            if len(col) == 0:
                p.pos[1] += 40
                p.height -= 40
                self.add_object(p)
                if speed == 0:
                    self.add_object(Coin(x + width / 2, y - 50, self.COIN))
                break

    def update_platforms(self):
        '''
        Генерация дополнительных платформ, чтобы их число было 6
        '''
        platforms = self.get_objects([Platform])
        if len(platforms) < 6:
            self.new_platform(-50, 0)

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
        self.platforms_move()
        self.update_platforms()

    def player_collision(self):
        '''
        Логика столкновений игрока с объектами игры.

        С платформой игрок сталкивается только при движении вниз, и тогда он становится на нее, гравитация не действует.
        Если пересечений нет, то игрок падает.
        Если платформа движется, то игрок перемещается вместе с ней
        Монету игрок забирает.
        '''
        plat_col = self.get_collision(self.player, Platform)
        if len(plat_col) == 0:
            self.player.on_ground = False  # падение
        else:
            if self.player.vel[1] > 0 and \
               self.player.pos[1] + self.player.height < plat_col[0].pos[1] + plat_col[0].height:
                self.player.pos[1] = plat_col[0].rect[1] - self.player.height + 1
                self.player.on_ground = True
                self.player.vel[1] = 0
                self.score += 1
            self.player.pos[0] += plat_col[0].vel[0]
        coins_col = self.get_collision(self.player, Coin)
        if len(coins_col) > 0:
            self.remove_object(coins_col[0])
            self.score += self.COIN_SCORE

    def player_move(self):
        '''
        Логика движения игрока.

        Гравитация если не стоит на платформе. Перемещение по кругу влево-вправо.
        Замедление горизонтального движения. Если упал, то конец игры.
        '''
        if not self.player.on_ground:
            self.player.vel[1] += settings.G
        if self.player.pos[0] > WIDTH:
            self.player.pos[0] = 0
        if self.player.pos[0] < 0:
            self.player.pos[0] = WIDTH
        self.player.acc[0] += self.player.vel[0] * settings.FRIC
        if self.player.pos[1] >= HEIGHT:
            time.sleep(0.5)
            self.set_state("End game")

    def platforms_move(self):
        '''
        Перемещение платформ с монетами вниз, когда игрок перемещается вверх
        '''
        if self.player.pos[1] <= HEIGHT / 3:
            vel = abs(self.player.vel[1])
            self.player.pos[1] += vel
            for o in self.get_objects([Platform, Coin]):
                o.pos[1] += vel
                if o.pos[1] >= HEIGHT:
                    self.remove_object(o)

    def end_game(self):
        self.add_object(Text(50, 30, "Verdana", 30, (255, 0, 0), lambda : "YOU DIE"))
        self.remove_object(self.player)

    def start_new_game(self):
        if self.key_pressed(pygame.K_SPACE):
            time.sleep(0.5)
            self.set_state("Intro")

j = JumpGame()
j.run()
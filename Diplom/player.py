from platformer.object import Object

class Player(Object):
    '''
    Класс игрока
    '''
    def __init__(self, x, y, sprite_file, vx=0, vy=0, width=None, height=None):
        super().__init__(x, y, sprite_file, vx, vy, width, height)

    def update(self):
        '''
        Метод обновления состояния игрока
        '''
        super().update()
        self.acc[0] = 0 # сброс горизонтального ускорения для остановки
'''
import pygame
from settings import WIDTH, ACC, FRIC

class Player(pygame.sprite.Sprite):

    def __init__(self, platforms, coins):
        super().__init__()
        self.surf = pygame.image.load("knight.png")
        self.rect = self.surf.get_rect()
        self.vec = pygame.math.Vector2
        self.pos = self.vec((10, 360))
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)
        self.jumping = False
        self.score = 0
        self.platforms = platforms
        self.coins = coins
        Player.P1 = self

    def move(self):
        self.acc = self.vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False'''

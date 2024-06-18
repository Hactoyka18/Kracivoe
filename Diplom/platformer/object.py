import pygame

class Object():
    def __init__(self, x, y, sprite_file, vx=0, vy=0, width=None, height=None):
        '''
        Класс объекта, который будет изменяться методами игровой системы и методами графической системы

        :param x: координата x
        :param y: координата y
        :param z: координата z
        '''
        self.pos = [x, y]
        self.vel = [vx, vy]
        self.image = pygame.image.load(sprite_file)
        self.width = width if width is not None else self.image.get_width()
        self.height = height if height is not None else self.image.get_height()
        self.surf = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
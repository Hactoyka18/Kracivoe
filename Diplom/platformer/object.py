import pygame

class Object():
    '''
    Класс игорового объекта
    '''
    def __init__(self, x, y, sprite_file, vx=0, vy=0, width=None, height=None):
        '''
        Создать объект с начальными параметрами. Объект может быть растянут
        по ширине и высоте

        :param x: координата x
        :param y: координата y
        :param sprite_file: имя файла спрайта
        :param vx: скорость x
        :param vy: скорость y
        :param width: ширина объекта, если не задана, то берется из спрайта
        :param height: высота объекта, если не задана, то берется из спрайта
        '''
        self.pos = [x, y]
        self.vel = [vx, vy]
        self.acc = [0, 0]
        self.image = pygame.image.load(sprite_file)
        self.width = width if width is not None else self.image.get_width()
        self.height = height if height is not None else self.image.get_height()
        self.surf = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def update(self):
        '''
        Обновляет состояние объекта каждый кадр.
        '''
        self.vel[0] += self.acc[0] # скорость прирастает с ускорением
        self.vel[1] += self.acc[1]
        self.pos[0] += self.vel[0] + 0.5 * self.acc[0] # позиция увеличивается со скоростью и усорением
        self.pos[1] += self.vel[1] + 0.5 * self.acc[1]
        # обновление прямоугольника объекта
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)


class Text(Object):
    '''
    Текстовый объект. Настраивается на функцию получения строки.
    '''
    def __init__(self, x, y, font, size, color, func):
        '''
        Создать текстовый объект

        :param x: координата x
        :param y: координата y
        :font: имя шрифта
        :size: размер шрифта
        :color: цвет текста
        :func: функция получения строки текста для реактивного обновления
        '''
        self.x = x
        self.y = y
        self.font = font
        self.size = size
        self.color = color
        self.func = func
        self.text = ""
        
    def update(self):
        '''
        Обновить текст из функции
        '''
        self.text = self.func()

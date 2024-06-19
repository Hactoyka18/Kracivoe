from platformer.object import Object

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
        self.func = func
        self.text = ""
        
    def update(self):
        '''
        Обновить текст из функции
        '''
        self.text = self.func()

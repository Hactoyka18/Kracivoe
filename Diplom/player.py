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


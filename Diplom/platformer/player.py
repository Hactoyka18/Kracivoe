from .object import Object

class Player(Object):
    G = 0.5
    def update(self):
        super().update()
        self.vel = (self.vel[0], self.vel[1] + self.G)
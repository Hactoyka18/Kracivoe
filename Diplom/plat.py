import random
from platformer.object import Object
from settings import WIDTH, HEIGHT


class Platform(Object):
    def __init__(self, x, y, sprite_file, vx=0, vy=0, width=None, height=None):
        w = random.randint(50, 120) if width is None else width
        super().__init__(x, y, sprite_file, vx, vy, w, height)

    def update(self):
        super().update()
        if self.vel[0] > 0 and self.pos[0] > WIDTH:
            self.pos[0] = -self.width
        if self.vel[0] < 0 and self.pos[0] + self.width < 0:
            self.pos[0] = WIDTH

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
'''
class Platform(pygame.sprite.Sprite):
    def __init__(self, width=0, height=18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("bip.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))

        self.point = True
        self.moving = True
        self.speed = random.randint(-1, 1)



        if (self.speed == 0):
            self.moving == False

    def move(self):
        hits = self.rect.colliderect(Player.P1.rect)
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if hits:
                Player.P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateCoin(self):
        if (self.speed == 0):
            Player.P1.coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))



'''

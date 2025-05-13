from character import Character

class Enemy(Character):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.health = 100
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction

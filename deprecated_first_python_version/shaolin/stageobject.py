from object import Object

class StageObject(Object):

    def __init__(self, image, x, y):
        Object.__init__(self)
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y - 13
        self.dy = 0
        self.z = -y


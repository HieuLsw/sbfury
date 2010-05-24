from PySFML import sf
import common

class Shadow(sf.Sprite):

    def __init__(self, shaolin):
        image = common.load_image("shadow.png")
        self.shaolin = shaolin
        sf.Sprite.__init__(self, image)
        self.SetCenter(58, 20)

    def update(self):
        self.SetPosition(self.shaolin.x, self.shaolin.y)

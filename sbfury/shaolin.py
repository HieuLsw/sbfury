from PySFML import sf
import common

class Shaolin(sf.Sprite):

    def __init__(self):
        image = common.load_sheet("../data/shaolin/stand.png", 4, 1)
        sf.Sprite.__init__(self, image.image)
        image.Assign(self)
        self.image = image
        self.SetPosition(200, 200)

    def update(self, dt):
        pass

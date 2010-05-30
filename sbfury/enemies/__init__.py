import sprite

class Enemy(sprite.Sprite):

    def __init__(self, must_be_updated=False):
        super(Enemy, self).__init__(must_be_updated=must_be_updated)
        self.flip = True

import fat
import hannia

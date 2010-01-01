from PySFML import sf
import common
import animation

class Shaolin(sf.Sprite):

    def __init__(self):
        image = common.load_sheet("../data/shaolin/stand.png", 4, 1)
        sf.Sprite.__init__(self, image.image)
        image.Assign(self)
        self.image = image
        self.SetPosition(200, 200)
        self._load_animations()
        self.set_animation('stand')

    def _load_animations(self):

        image = common.load_sheet("../data/shaolin/stand.png", 4, 1)
        
        self.animations = {
                'stand': animation.Animation(image, 0.20, [0, 1, 2, 3]),
                }

    def set_animation(self, animation_name):
        self.animation = self.animations[animation_name]

    def update(self, dt):
        self.update_animation(dt)

    def update_animation(self, dt):
        self.animation.update(dt)
        self.animation.Assign(self)

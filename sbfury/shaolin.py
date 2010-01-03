from PySFML import sf
import common
import animation
import states

class Shaolin(sf.Sprite):

    def __init__(self, control):
        self.control = control

        image = common.load_sheet("../data/shaolin/stand.png", 4, 1)
        self.image = image
        sf.Sprite.__init__(self, image.image)
        image.Assign(self)

        self.SetPosition(200, 400)
        self._load_animations()
        self.set_animation('stand')

        self.change_state(states.Starting(self))
        self.last_attack = (0, 0)
        self.dy = 0

    def _load_animations(self):
        animation_defines = [
                # (name, frames, delay per frame)
                ('stand', 4, 1),
                ('attack1', 2, 0.05),
                ('attack2', 2, 0.05),
                ('attack3', 2, 0.05),
                ('attack4', 2, 0.1),
                ('attackjumprun', 2, 1),
                ('attackjumpstand', 2, 1),
                ('attackjumpwalk', 2, 1),
                ('attackrun', 1, 1),
                ('attacktake', 1, 1),
                ('ground', 1, 1),
                ('groundtostand', 1, 1),
                ('hardhit', 2, 1),
                ('hitstand1', 2, 1),
                ('hitstand2', 2, 1),
                ('jumpstand', 3, 1),
                ('jumpwalk', 3, 1),
                ('run', 4, 0.03),
                ('special', 5, 1),
                ('stand', 4, 1),
                ('starting', 3, 1),
                ('take', 1, 1),
                ('throw', 3, 1),
                ('walk', 4, 0.2),
                ]

        # each elements has an animation like: 'stand': AnimationObject()...
        self.animations = {}

        for (name, frames, delay) in animation_defines:
            filename = "shaolin/%s.png" %(name)
            sheet = common.load_sheet(filename, frames, 1)
            self.animations[name] = animation.Animation(sheet, delay, range(frames))
        
        #self.animations = {
        #        'stand': animation.Animation(image, 0.20, [0, 1, 2, 3]),
        #        }

    def set_animation(self, animation_name):
        self.animation = self.animations[animation_name]

    def update(self, dt):
        self.state.update(dt)
        '''
        self.update_animation(dt)

        if self.control.left:
            self.Move(-dt * 200, 0)
            self.FlipX(True)
        elif self.control.right:
            self.Move(dt * 200, 0)
            self.FlipX(False)

        if self.control.up:
            self.Move(0, -dt * 200)
        elif self.control.down:
            self.Move(0, dt * 200)
        '''


    def update_animation(self, dt):
        was_restarted = self.animation.update(dt)
        self.animation.Assign(self)
        return was_restarted

    def change_state(self, new_state):
        self.state = new_state

    def set_flip(self, flip):
        self.FlipX(flip)

    def move(self, dx, dy):
        self.Move(dx, dy)

    def are_in_flood(self):
        return self.dy > 0

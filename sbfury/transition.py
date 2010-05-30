from cocos.scenes.transitions import *
from cocos.actions import *

class MoveDown(TransitionScene):

    def __init__(self, dst, duration, src=None):
        super(MoveDown, self).__init__(dst, duration, src)
        self.in_scene.position = 0, -480
        self.schedule(self.step)

    def start(self):
        self.add(self.in_scene, z=0)
        self.add(self.out_scene, z=1)

    def step(self, dt):
        speed = 480 * 2
        delta = speed * dt

        if self.out_scene.y > 480:
            self.out_scene.y = 480
            self.in_scene.y = 0
            self.finish()
        else:
            self.out_scene.y += delta
            self.in_scene.y += delta

class MoveUp(MoveDown):

    def __init__(self, *args, **kargs):
        super(MoveUp, self).__init__(*args, **kargs)
        self.in_scene.position = 0, +480

    def step(self, dt):
        speed = 480 * 2
        delta = speed * dt

        if self.out_scene.y < -480:
            self.out_scene.y = -480
            self.in_scene.y = 0
            self.finish()
        else:
            self.out_scene.y -= delta
            self.in_scene.y -= delta

class MoveLeft(MoveDown):

    def __init__(self, *args, **kargs):
        super(MoveLeft, self).__init__(*args, **kargs)
        self.in_scene.position = 640, 0

    def step(self, dt):
        speed = 640 * 2
        delta = speed * dt

        if self.out_scene.x < -640:
            self.out_scene.x = -640
            self.in_scene.x = 0
            self.finish()
        else:
            self.out_scene.x -= delta
            self.in_scene.x -= delta

class MoveRight(MoveDown):

    def __init__(self, *args, **kargs):
        super(MoveRight, self).__init__(*args, **kargs)
        self.in_scene.position = -640, 0

    def step(self, dt):
        speed = 640 * 2
        delta = speed * dt

        if self.out_scene.x > 640:
            self.out_scene.x = 640
            self.in_scene.x = 0
            self.finish()
        else:
            self.out_scene.x += delta
            self.in_scene.x += delta

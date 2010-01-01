# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from pyglet.gl import *
import cocos
import common
import config


class State:

    def __init__(self, target):
        self.target = target

    def update(self, dt):
        pass

    def on_control_press(self, map):
        pass

    def on_control_release(self, map):
        pass

    def on_collision_send(self, other_sprite):
        pass

    def on_collision_receive(self, other_sprite, force):
        """Returns True if collision do something."""
        pass


class Sprite(cocos.sprite.Sprite):

    def __init__(self, image=None, must_be_updated=False, *args, **kwargs):

        if not image:
            image = common.load_image('none.png')

        super(Sprite, self).__init__(image, *args, **kwargs)
        self.set_collision(None)
        self.distance_to_floor = 0
        self.shadow = False
        self.move(0, 0)

        if must_be_updated:
            self.schedule(self.update)

    def update_animation(self, dt, repeat=True):
        """Update animation state. Returns True if animation are done."""
        if self.animation.update(dt, self.flip, repeat=repeat):
            return True

        self.image = self.animation.image

    def set_frame(self, index):
        self.animation.set_frame(index, self.flip)
        self.image = self.animation.image

    def set_state(self, state):
        self._state = state

    def update(self, dt):
        self._state.update(dt)

    def on_collision_receive(self, other_sprite, collision_force):
        return self._state.on_collision_receive(other_sprite, collision_force)
        #print "I am are:", self, "\t\tand the other sprite are:", other_sprite

    def on_collision_send(self, other_sprite):
        self._state.on_collision_send(other_sprite)
        #print "I am are:", self, "\t\tand i send a collision to:", other_sprite

    def set_collision(self, rect, force=1):
        """Set collisionable area and force magnitude.

            `rect`: tuple
                collision area
            `force`: int
                force magnitude, it can be 1, 2, 3, 4 (max)."""

        self.rect_collision = rect

        if force in [1, 2, 3, 4]:
            self.collision_force = force
        else:
            raise ValueError("Collision force are not in [1, 4] range.")

    def draw(self):
        self.image.blit(self.x, self.y + self.distance_to_floor)

        if config.SHOW_CONTROL_POINTS:
            common.draw_point(self.x, self.y + self.distance_to_floor)

        if config.SHOW_COLLISION_BOXES and self.rect_collision:
            rect = self.get_rect_collision_world_position()
            common.draw_collision(*rect)

    def get_rect_collision_world_position(self):
        x, y, w, h = self.rect_collision

        if self.flip:
            x += self.x - w
        else:
            x += self.x

        y += self.y + h +  self.distance_to_floor
        return x, y, w, h

    def move(self, dx, dy):
        x, y = self.position
        speed = 300
        to_x, to_y = x + speed * dx, y + speed * dy

        if to_y <= 10:
            to_y = 10
        elif to_y >= 230:
            to_y = 230

        if to_x <= 10:
            to_x = 10
        elif to_x >= 5200:
            to_x = 5200

        self.position = to_x, to_y

        if self.shadow:
            self.shadow.position = to_x, to_y + 1
            self.shadow.scale = (1 - self.distance_to_floor / 400.0)


    def get_collision_receive_area(self):
        w, h = self.image.width, self.image.height
        x, y = self.x, self.y + self.distance_to_floor
        return x - w / 2, y, w, h

if __name__ == '__main__':
    common.director.init(resizable=True)

    sprite = Sprite()
    sprite.position = 300, 300
    layer = cocos.layer.ColorLayer(100, 100, 100, 255)
    scene = cocos.scene.Scene(layer)
    layer.add(sprite)

    common.director.run(scene)

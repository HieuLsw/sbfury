# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from random import randint
import cocos.layer


#from cocos.actions import *
#from pyglet.gl import *
import sprite
import animation

import common


class HitEffect(sprite.Sprite):
    """Show a impact effect for collisions."""

    def __init__(self, x, y):
        self.animation = animation.Animation("hits.png", 5, 0.05)
        super(HitEffect, self).__init__(must_be_updated=True)
        self.image = self.animation.image
        self.position = x, y
        common.sound.play('punch1')

    def update(self, dt):
        """Update animation state. Returns True if animation are done."""

        if self.animation.update(dt):
            self._kill()
            return

        self.image = self.animation.image

    #def draw(self):
    #    # FIX: this is a bugfix for nvidia old drivers.
    #    glColor4f(1, 1, 1, 1)
    #    glColor4f(1, 1, 1, 1)

    def _kill(self):
        self.parent.remove(self)


class CollisionManager(cocos.layer.Layer):
    """Handle collision between sprite objects."""

    def __init__(self):
        super(CollisionManager, self).__init__()
        self.objects_group_a = []
        self.objects_group_b = []
        self.schedule(self.update)

    def add_player(self, sprite):
        self.objects_group_a.append(sprite)

    def add_enemy(self, sprite):
        self.objects_group_b.append(sprite)

    def update(self, dt):
        """Do collision check."""

        for a in self.objects_group_a:
            for b in self.objects_group_b:

                if self._get_collision(send=a, receive=b):
                    a.on_collision_send(b)

                    if b.on_collision_receive(a, a.collision_force):
                        self._create_collision_effect((a.x, a.y), a.flip)
                elif self._get_collision(send=b, receive=a):

                    b.on_collision_send(a)

                    if a.on_collision_receive(b, b.collision_force):
                        self._create_collision_effect((a.x, a.y), a.flip)

                    
    def _create_collision_effect(self, (x, y), flip):
        x += randint(-30, 30)
        y += randint(-20, 20)

        if flip:
            dx = -80
        else:
            dx = 90

        self.add(HitEffect(x + dx, y + 80))

    def _get_collision(self, send, receive):
        """Checks collision between two sprites.

        :Parameters:
            `send`: Sprite
                Sprite that send a rectangle collision.
            `receive`: Sprite
                Sprite that receive the attack of sprite `a`.
        """

        if send.rect_collision and self.are_close_in_z_plane(send, receive):
            x0, y0, w0, h0 = send.get_rect_collision_world_position()
            x1, y1, w1, h1 = receive.get_collision_receive_area()

            if (x0 < x1 < x0 + w0) or (x1 < x0 < x1 + w1):
                if (y0 < y1 < y0 + h0) or (y1 < y0 < y1 + h1):
                    return True

    def are_close_in_z_plane(self, sprite_a, sprite_b):
        if abs(sprite_a.y - sprite_b.y) < 30:
            return True

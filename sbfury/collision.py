# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from random import randint

import cocos.layer
from cocos.actions import *
from pyglet.gl import *

import common

class LeptonHitEffect(cocos.sprite.Sprite):
    """Show a impact effect for collisions."""

    def __init__(self, x, y):
        image = common.load_image('effects/hit.png')

        r = randint(200, 255)
        g = randint(200, 255)
        b = randint(200, 255)

        super(HitEffect, self).__init__(image, color=(r, g, b))
        self.position = x, y
        speed = 0.3
        self.scale = 0
        self.do(RotateBy(130, duration=speed) | 
                ScaleTo(2, duration=speed) |
                FadeOut(duration=speed) +
                CallFunc(self._kill))

    def draw(self):
        # FIX: this is a bugfix for nvidia old drivers.
        glColor4f(1, 1, 1, 1)
        cocos.sprite.Sprite.draw(self)
        glColor4f(1, 1, 1, 1)

    def _kill(self):
        self.parent.remove(self)

class HitEffect(cocos.sprite.Sprite):
    """Show a impact effect for collisions."""

    def __init__(self, x, y):
        image = common.load_image('effects/hit.png')

        r = randint(200, 255)
        g = randint(200, 255)
        b = randint(200, 255)

        super(HitEffect, self).__init__(image, color=(r, g, b))
        self.position = x, y
        speed = 0.3
        self.scale = 0
        self.do(RotateBy(130, duration=speed) | 
                ScaleTo(2, duration=speed) |
                FadeOut(duration=speed) +
                CallFunc(self._kill))

    def draw(self):
        # FIX: this is a bugfix for nvidia old drivers.
        glColor4f(1, 1, 1, 1)
        cocos.sprite.Sprite.draw(self)
        glColor4f(1, 1, 1, 1)

    def _kill(self):
        self.parent.remove(self)


class CollisionManager(cocos.layer.Layer):
    """Gestiona colisiones entre el protagonistra y los Enemigos.
    
    Este objeto tiene dos listas ``objects_group_a`` y ``objects_group_b``.

    Cada vez que se actualiza el objeto se busca si los sprites
    de un grupo emiten colisiones para sprites del otro grupo. Y además
    se fija si efectivamente esas emisiones de colisiones realmente
    afectan a algun personaje.
    """

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
        """Avisa a los personajes que se intercambian colisiones."""

        for a in self.objects_group_a:
            for b in self.objects_group_b:

                # si un objeto del grupo 'a' le pega a uno del grupo 'b'...
                if self._get_collision(send=a, receive=b):
                    # le avisa a los dos objetos que existe una colisión.
                    a.on_collision_send(b)

                    if b.on_collision_receive(a, a.collision_force):
                        self._create_collision_effect((b.x, b.y))

                elif self._get_collision(send=b, receive=a):
                    b.on_collision_send(a)

                    if a.on_collision_receive(b, b.collision_force):
                        self._create_collision_effect((a.x, a.y))
                    
    def _create_collision_effect(self, (x, y)):
        "Genera un efecto de golpe ante la colisión."

        x += randint(-30, 30)
        y += randint(-20, 20)
        self.add(LeptonHitEffect(x, y + 110))

    def _get_collision(self, send, receive):
        """Analiza si existe una colision entre dos personajes.

        Para que exista un colision entre un sprite y otro, el
        emisor tiene que tener un atributo llamado ``rect_collision``
        que esté justo solapado con el rectángulo del receptor, 
        rectángulo que se obtiene con el método
        ``get_collision_receive_area``. """
        
        if send.rect_collision and self.are_close_in_z_plane(send, receive):
            x0, y0, w0, h0 = send.get_rect_collision_world_position()
            x1, y1, w1, h1 = receive.get_collision_receive_area()

            if (x0 < x1 < x0 + w0) or (x1 < x0 < x1 + w1):
                if (y0 < y1 < y0 + h0) or (y1 < y0 < y1 + h1):
                    return True

    def are_close_in_z_plane(self, sprite_a, sprite_b):
        """Indica si los dos personajes estan cerca respecto del plano z.
        
        El plano z es el de profundidad, y es el que depermina si una
        colision es posible o no.
        """
        if abs(sprite_a.y - sprite_b.y) < 30:
            return True

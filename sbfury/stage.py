# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import cocos
import partial_image
from cocos.actions import *

import layer
import common
import config
import collision


class Stage(cocos.layer.Layer):
    """Es un componente de la escena Game que muestra el escenario y adminitra colisiones.

    Stage es uno de los componentes principales, porque conoce
    al objeto que tiene que seguir la cámara, imprime el escenario
    simulando un scroll horizontal y además gestiona colisiones.
    """

    def __init__(self, number, object_to_follow):
        super(Stage, self).__init__()
        self.have_extra_layer = False
        self._create_layers(number)
        self._create_collision_manager()
        self.schedule(self.update)
        self.object_to_follow = object_to_follow
        self.camera_x = 0.0
        # TODO: store the level number.

    def update(self, dt):
        dx = self._get_camera_motion() * dt * 4
        self.camera_x -= dx

        if self.camera_x > 4600:
            self.camera_x = 4600
            dx = 0
        elif self.camera_x < 1:
            self.camera_x = 0
            dx = 0

        # Back layers
        self.layer_3.x += dx / 4
        self.layer_2.x += dx / 2

        # Floor and decoration
        if config.PERSPECTIVE_FLOOR:
            self.layer_0.x += dx / 2.25

            if self.have_extra_layer:
                self.extra_layer_1.x += dx / 2.25 - dt * 40
                self.extra_layer_2.x += dx / 2.25 - dt * 80
        else:
            self.layer_0.x += dx

        self.layer_1.x += dx

        # Frontal
        if config.SHOW_FRONT_LAYER:
            self.layer_4.x += dx * 1.8

        self.main_layer.x += dx
        self.collision_manager.x += dx

    def _get_camera_motion(self):
        delta = (self.object_to_follow.x - 320 - self.camera_x)
        return - delta

    def _create_layers(self, number):
        prefix = 'stages/%d/layer_' %(number)

        ima = partial_image.PartialImage(prefix + '3')
        self.layer_3 = layer.PartialImageLayer(ima, top=True)

        ima = partial_image.PartialImage(prefix + '2')
        self.layer_2 = layer.PartialImageLayer(ima, top=True)

        ima = partial_image.PartialImage(prefix + '1')
        self.layer_1 = layer.PartialImageLayer(ima, top=True)

        if config.PERSPECTIVE_FLOOR:
            ima = partial_image.PartialImage(prefix + '0')
            self.layer_0 = layer.PartialImageLayer3D(ima, -0, -13)

            try:
                ima = partial_image.PartialImage(prefix + '5')
                self.extra_layer_1 = layer.PartialImageLayer3D(ima, -0, -40)

                #ima = image.PartialImage(prefix + '5')
                self.extra_layer_2 = layer.PartialImageLayer3D(ima, -0, -40)

                self.have_extra_layer = True

                speed = 0.5
                move = MoveBy((-30, 0), duration=speed)
                move2 = MoveBy((-30, 0), duration=speed / 2.0)

                #self.extra_layer_1.do(Repeat(move))
                #self.extra_layer_2.do(Repeat(move2))

                #self.add(self.extra_layer_1, z=-0.5)
                #self.add(self.extra_layer_2, z=-0.4)
            except OSError:
                pass

        else:
            ima = partial_image.PartialImage(prefix + '0')
            self.layer_0 = layer.PartialImageLayer(ima, -0, -42)

        self.main_layer = layer.OrderlyLayer()

        '''
        self.add(self.layer_3, z=-1)
        self.add(self.layer_2, z=-0.9)
        self.add(self.layer_1, z=-0.8)
        self.add(self.layer_0, z=-0.7)
        '''

        self.add(self.main_layer)

        if config.SHOW_FRONT_LAYER:
            ima = partial_image.PartialImage(prefix + '4')
            self.layer_4 = layer.PartialImageLayer(ima, top=False)
            self.add(self.layer_4, z=1)

    def draw(self):
        self.layer_3.draw()
        self.layer_2.draw()
        self.layer_1.draw()
        self.layer_0.draw()
        #self.main_layer.draw()

        if config.PERSPECTIVE_FLOOR:
            if self.have_extra_layer:
                self.extra_layer_1.draw()
                self.extra_layer_2.draw()

        if config.SHOW_FRONT_LAYER:
            self.layer_4.draw()

    def add_element(self, element):
        """Agrega un elemento como un sprite o nodo al layer principal.

        Este método se tiene que llamar con cualquier personaje
        que se quiera insertar en el escenario, como un enemigo o
        el protagonista."""
        self.main_layer.add(element)

    def _create_collision_manager(self):
        "Genera el administrador de colisiones, que avisa a los personajes ante colisiones."
        self.collision_manager = collision.CollisionManager()
        self.add(self.collision_manager, z=1)


if __name__ == '__main__':
    import common

    class CameraControl(cocos.layer.Layer):
        is_event_handler = True

        def __init__(self):
            super(CameraControl, self).__init__()
            self.x = 500
            self.y = 0

        def on_mouse_motion(self, x, y, dx, dy):
            self.x += dx

    common.director.init(resizable=True)
    control = CameraControl()
    stage = Stage(1, object_to_follow=control)
    stage.add(control)
    common.director.run(cocos.scene.Scene(stage))

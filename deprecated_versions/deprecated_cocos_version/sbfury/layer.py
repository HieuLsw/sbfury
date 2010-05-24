# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from pyglet.gl import *
import cocos
from cocos.euclid import *

import common
from pyglet.gl import *

class OrderlyLayer(cocos.layer.Layer):
    """Show childrens in order, using the `y` attribute."""

    def __init__(self):
        super(OrderlyLayer, self).__init__()

    def visit(self):
        """Call the `draw` method of every children."""
        self.children.sort(self._cmp)

        glPushMatrix()
        self.transform()

        for z, c in self.children:
            c.draw()

        glPopMatrix()

    def _cmp(self, a, b):
        if a[1].y <= b[1].y:
            return 1
        else:
            return -1


class ImageLayer(cocos.layer.Layer):

    def __init__(self, path_or_image, dx=0, dy=0, top=False):
        super(ImageLayer, self).__init__()

        if isinstance(path_or_image, str):
            self.image = common.load_image(path_or_image)
        else:
            self.image = path_or_image

        self.x = dx
        self.y = dy

        if top:
            self.y = 480 - self.image.height

    def draw(self):
        self.image.blit(self.x, self.y)


class PartialImageLayer(ImageLayer):

    def __init__(self, image, top, dx=0, dy=0):
        super(PartialImageLayer, self).__init__(image, top, dx, dy)

        if top:
            self.y = 480 - self.image.height

    def draw(self):
        x, y = self.position
        self.image.blit((-x, 0), (0, y), 800)

'''
class ImageLayer3D(ImageLayer):

    def __init__(self, path_or_image, dx=0, dy=0):
        super(ImageLayer3D, self).__init__(path_or_image, dx, dy)
        self.camera.eye = Point3(320, 0, 200)
        self.scale = 0.8

    def draw(self):
        glPushMatrix()
        self.transform()
        self.image.blit(self.x, self.y)
        glPopMatrix()
'''


class PartialImageLayer3D(ImageLayer):

    def __init__(self, image, dx=0, dy=0):
        super(PartialImageLayer3D, self).__init__(image, dx, dy)

    def draw(self):
        x, y = self.position
        glPushMatrix()
        glRotatef(35, -1, 0, 0)
        glScalef(1.45, 1.45, 0)
        glTranslatef(-98, -63, 0)
        self.image.blit((-x*2.25, 0), (0, y), 800)
        glPopMatrix()


if __name__ == '__main__':
    import image
    common.director.init(resizable=True)

    layer0 = cocos.layer.ColorLayer(100, 100, 100, 255)
    ima = image.PartialImage('stages/1/layer_3')
    layer = PartialImageLayer(ima, top=True)
    scene = cocos.scene.Scene(layer0, layer)

    common.director.run(scene)

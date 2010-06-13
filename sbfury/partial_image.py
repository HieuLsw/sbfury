# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import pyglet

import common

class PartialImage:

    def __init__(self, directory):
        dirname = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.join(dirname, '..', 'data', directory)
        names_list = [f for f in os.listdir(directory) if 'png' in f]
        names_list.sort()
        self.images = [common.load_image(directory + '/' + name) 
                for name in names_list]
        self.width = self.images[0].width
        self.height = self.images[0].height

    def blit(self, (x, y), (dst_x, dst_y), width):
        """Blit this image into video surface.

        :Parameters:
            `(x, y)`: tuple of int
                top left corner of this image (reference point to read).
            `(dst_x, dst_y)`: tuple of int
                destination point
            `width`: int
                amuont of horizontal pixels to read.
        """

        while width > 0:
            index = x / self.width
            # Transform to infinite (ciclical) image.
            index = int(index) % len(self.images)
            delta_x = x % self.width

            try:
                self.images[index].blit(dst_x - delta_x, dst_y)
            except IndexError:
                pass

            width -= self.width
            dst_x += self.width
            x += self.width


if __name__ == '__main__':
    from pyglet.gl import *
    import cocos

    common.director.init(resizable=True)
    ima = PartialImage('stages/1/layer_3')


    class Layer(cocos.layer.Layer):

        def __init__(self, ima):
            cocos.layer.Layer.__init__(self)
            self.position = 0, 0
            self.image = ima
            
        def draw(self):
            #x, y = self.position
            glPushMatrix()
            self.transform()
            self.image.blit((12, 0), (0, 0), 500)
            glPopMatrix()


    scene = cocos.scene.Scene(Layer(ima))
    common.director.run(scene)

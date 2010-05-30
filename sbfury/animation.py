# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import pyglet
import common

# Anchor values
CENTER, BOTTOM = 1, 2


class Animation:
    '''Represent an animation sequence.

    Only `image` attribute are public.'''

    def __init__(self, path, frames, delay=0.1, anchor=BOTTOM):
        self._image_grid = self._load_image(path, frames, flip=False)
        self._image_grid_flip = self._load_image(path, frames, flip=True)
        self._delay = delay
        self._frames = frames
        self._step = 0
        self._frame = 0
        self.image = self._image_grid[0]
        self._set_anchor(anchor)

    def _set_anchor(self, anchor):
        '''Set an `anchor` for any frame in animation.'''

        w = self.image.width
        h = self.image.height

        if anchor == BOTTOM:
            x = w / 2
            y = 10
        elif anchor == CENTER:
            x = w / 2
            y = h / 2
        else:
            raise Exception("invalid anchor %d" % anchor)

        w = self.image.width

        for image_frame in self._image_grid:
            image_frame.anchor_x = x
            image_frame.anchor_y = y

        for image_frame in self._image_grid_flip:
            image_frame.anchor_x = x
            image_frame.anchor_y = y

    def _load_image(self, path, frames, flip=False):
        '''Creates the image grid.'''

        image = common.load_image(path)

        if flip:
            image = image.get_texture().get_transform(flip_x=True)

        return pyglet.image.ImageGrid(image, rows=1, columns=frames)

    def update(self, dt, flip=False, repeat=True):
        '''Update `image` attribute.

        :Parameters:
            `dt`: float
                delta time.
            `flip`: bool
                if sprite must be horizontal flip.
            `repeat`: bool
                if animation must be restarted at end.

        Returns True if animation was restarted.
        '''
        self._step += dt

        if self._step > self._delay:
            self._step -= self._delay
            self._frame += 1

            if self._frame >= self._frames:
                if repeat:
                    self._frame = 0
                else:
                    self._frame = self._frames -1

                if flip:
                    self.image = self._image_grid_flip[self._frame]
                else:
                    self.image = self._image_grid[self._frame]

                return True
            else:

                if flip:
                    self.image = self._image_grid_flip[self._frame]
                else:
                    self.image = self._image_grid[self._frame]

                return False

        if flip:
            self.image = self._image_grid_flip[self._frame]
        else:
            self.image = self._image_grid[self._frame]

        return False

    def set_frame(self, index, flip=False):
        if flip:
            self.image = self._image_grid_flip[index]
        else:
            self.image = self._image_grid[index]

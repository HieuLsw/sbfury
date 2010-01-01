# -*- encoding: utf-8 -*-
# Shaolin's Blind Fury
#
# Copyright 2008 - Hugo Ruscitti
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
sys.path.append('./')

import cocos
from cocos.director import director
from cocos.sprite import Sprite
from cocos.actions import *

from test import *

import common
import shaolin
import control


if __name__ == '__main__':
    common.director.init(resizable=True)

    shaolin = shaolin.shaolin.Shaolin()
    control = control.Control(shaolin)

    layer = cocos.layer.ColorLayer(100, 100, 100, 255)
    scene = cocos.scene.Scene(layer)
    layer.add(shaolin)
    layer.add(control)

    common.director.run(scene)

# ----------------------------------------------------------------------------
# cocos2d
# Copyright (c) 2008 Daniel Moisset, Ricardo Quesada, Rayentray Tappa, Lucio Torre
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright 
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of cocos2d nor the names of its
#     contributors may be used to endorse or promote products
#     derived from this software without specific prior written
#     permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
'''Pause scene'''

__docformat__ = 'restructuredtext'

from cocos.director import director
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.sprite import Sprite

import pyglet

from pyglet.gl import *

'''
__pause_scene_generator__ = None

def get_pause_scene():
    return __pause_scene_generator__()
    
def set_pause_scene_generator(generator):
    global __pause_scene_generator__
    __pause_scene_generator__ = generator
    
def default_pause_scene():
    x,y = director.get_window_size()
    texture = pyglet.image.Texture.create_for_size(
                    GL_TEXTURE_2D, x, 
                    y, GL_RGBA)
    texture.blit_into(pyglet.image.get_buffer_manager().get_color_buffer(), 0,0,0)
    return PauseScene(
        texture, ColorLayer(25,25,25,205), PauseLayer()
        )
set_pause_scene_generator( default_pause_scene )
'''

class PauseScene(Scene):
    '''Pause Scene'''
    def __init__(self):
        super(PauseScene, self).__init__()
        self.add(PauseLayer())
        self.add(ColorLayer(25,25,25,205), z=1)
        
    def draw(self):
        super(PauseScene, self).draw()
        
        
class PauseLayer(Layer):
    '''Layer that shows the text 'PAUSED'
    '''
    is_event_handler = True     #: enable pyglet's events

    def __init__(self, background=None, *layers):
        super(PauseLayer, self).__init__(*layers)

        if not background:
            screenshot = self._create_screenshot()
            self.add(screenshot, z=-1)
        
        x,y = director.get_window_size()
        
        ft = pyglet.font.load('Arial', 36)
        self.text = pyglet.font.Text(ft, 
            'PAUSED', halign=pyglet.font.Text.CENTER)
        self.text.x = x/2
        self.text.y = y/2
        
    def draw(self):
        self.text.draw()
        
    def on_key_press(self, k, m):
        if k == pyglet.window.key.P and m == pyglet.window.key.MOD_ACCEL:
            director.pop()
            return True
            
    def _create_screenshot(self):
        buffer = pyglet.image.BufferManager()
        image = buffer.get_color_buffer()

        width, height = director.window.width, director.window.height 
        actual_width, actual_height = director.get_window_size()

        out = Sprite(image)
        out.position = actual_width / 2, actual_height / 2
        out.scale = max(actual_width / float(width), actual_height / float(height))

        return out

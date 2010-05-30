import sys
sys.path.append('./')

import pyglet
import cocos

import config
import common
import sprite
import animation
import shadow
import shaolin

import collision
import enemies


if __name__ == '__main__':
    import control
    common.director.init(resizable=True)

    shaolin = shaolin.shaolin.Shaolin()
    control = control.Control(shaolin)

    layer = cocos.layer.ColorLayer(100, 100, 100, 255)
    scene = cocos.scene.Scene(layer)

    fat = enemies.fat.Fat()
    layer.add(fat)

    layer.add(shaolin)
    layer.add(control)
    layer.add(shaolin.shadow)

    collision_manager = collision.CollisionManager()
    collision_manager.add_player(shaolin)
    collision_manager.add_enemy(fat)
    layer.add(collision_manager, z=1)

    common.director.run(scene)

import pyglet

import config
import common
import scene

def main():
    #pyglet.options['debug_gl'] = config.DEBUG_GL

    window = common.director.init(resizable=config.RESIZABLE, vsync=config.VSYNC)

    if config.DEBUG:
        first_scene = scene.game.Game(level=1)
    else:
        first_scene = scene.logo.Logo()

    if config.NEW_PYGLET_LOOP:
        print "Using new pyglet loop."
        common.director.run(first_scene)
    else:
        from pyglet.clock import tick
        print "Using old pyglet loop method."

        while not window.has_exit:
            #dt = tick()
            #update(dt)

            window.switch_to()
            try:
                window.dispatch_events()
            except:
                pass
            window.dispatch_event('on_draw')
            window.flip()
            #window.clear()
            #draw()
            window.flip()

if __name__ == "__main__":
    main()

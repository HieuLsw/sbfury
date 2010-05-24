import pyglet

import config
import common
import scene

def main():
    #pyglet.options['debug_gl'] = config.DEBUG_GL

    window = common.director.init(resizable=True, vsync=config.VSYNC)

    if config.NEW_PYGLET_LOOP:
        print "Using new pyglet loop."

        common.director.run(scene.logo.Logo())
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

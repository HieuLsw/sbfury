import scene
import common
import scene
import config

window = common.director.init(resizable=True, vsync=config.VSYNC)

if config.MOVE_WINDOW:
    window.set_location(300, 200)

common.director.run(scene.game.Game())

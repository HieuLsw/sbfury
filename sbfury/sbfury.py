from PySFML import sf
from time import time
import sys
import common
import control

import shaolin

def get_tick():
    "Retorna el tiempo actual en milisegundos."
    return int(time() * 1000)

FPS = 60
TICK_STEP = 1000 / FPS

FULLSCREEN = False

if FULLSCREEN:
    app = sf.RenderWindow(sf.VideoMode(720, 480), "sbfury", sf.Style.Fullscreen)
else:
    app = sf.RenderWindow(sf.VideoMode(720, 480), "sbfury", sf.Style.Titlebar)
    app.SetPosition(300, 200)


# Es el contenedor del evento.
event = sf.Event()
input = app.GetInput()

clock = sf.Clock()
color = sf.Color(200, 200, 200)

app.UseVerticalSync(False)

control = control.Control(input)

player = shaolin.Shaolin(control)
next_tick = get_tick()

while True:
    app.Clear(color)
    app.Draw(player)
    app.Draw(player.shadow)

    while get_tick() > next_tick:

        while app.GetEvent(event):

            if event.Type == sf.Event.KeyPressed:
                if event.Key.Code == sf.Key.Escape:
                    app.Close()
                    sys.exit(0)
            elif event.Type == sf.Event.Closed:
                sys.exit(0)

        next_tick += TICK_STEP
        control.update()
        player.update()

    app.Display()

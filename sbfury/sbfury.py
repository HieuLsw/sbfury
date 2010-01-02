from PySFML import sf
import sys
import common
import control

import shaolin


FULLSCREEN = False

if FULLSCREEN:
    app = sf.RenderWindow(sf.VideoMode(720, 480), "sbfury", sf.Style.Fullscreen)
else:
    app = sf.RenderWindow(sf.VideoMode(720, 480), "sbfury")
    app.SetPosition(300, 200)


# Es el contenedor del evento.
event = sf.Event()
input = app.GetInput()

clock = sf.Clock()
color = sf.Color(200, 200, 200)

app.UseVerticalSync(True)

control = control.Control(input)

player = shaolin.Shaolin(control)

while True:
    dt = app.GetFrameTime()
    app.Clear(color)
    app.Draw(player)

    control.update(dt)
    player.update(dt)

    while app.GetEvent(event):

        if event.Type == sf.Event.KeyPressed:
            if event.Key.Code == sf.Key.Escape:
                app.Close()
                sys.exit(0)
        elif event.Type == sf.Event.Closed:
            sys.exit(0)

    app.Display()

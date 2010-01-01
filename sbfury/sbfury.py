from PySFML import sf
import sys
import common

import shaolin


app = sf.RenderWindow()
app.Create(sf.VideoMode(720, 480), "sbfury")
app.SetPosition(300, 200)

# Es el contenedor del evento.
event = sf.Event()
input = app.GetInput()

clock = sf.Clock()
color = sf.Color(200, 200, 200)

app.UseVerticalSync(True)


player = shaolin.Shaolin()

while True:
    dt = app.GetFrameTime()
    app.Clear(color)
    app.Draw(player)

    player.update(dt)

    while app.GetEvent(event):

        if event.Type == sf.Event.KeyPressed:
            if event.Key.Code == sf.Key.Escape:
                app.Close()
                sys.exit(0)
        elif event.Type == sf.Event.Closed:
            sys.exit(0)

    app.Display()

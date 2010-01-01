from PySFML import sf
import sys

app = sf.RenderWindow()
app.Create(sf.VideoMode(720, 480), "sbfury")

# Es el contenedor del evento.
event = sf.Event()
input = app.GetInput()

clock = sf.Clock()
color = sf.Color(200, 200, 200)

app.UseVerticalSync(True)

while True:
    dt = app.GetFrameTime()
    app.Clear(color)


    while app.GetEvent(event):

        if event.Type == sf.Event.KeyPressed:
            if event.Key.Code == sf.Key.Escape:
                app.Close()
                sys.exit(0)
        elif event.Type == sf.Event.Closed:
            sys.exit(0)


    app.Display()

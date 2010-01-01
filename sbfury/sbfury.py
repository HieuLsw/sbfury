from PySFML import sf
import sys
import common

app = sf.RenderWindow()
app.Create(sf.VideoMode(720, 480), "sbfury")

# Es el contenedor del evento.
event = sf.Event()
input = app.GetInput()

clock = sf.Clock()
color = sf.Color(200, 200, 200)

app.UseVerticalSync(True)


image = common.load_image("logo.png")
sprite = sf.Sprite(image)

while True:
    dt = app.GetFrameTime()
    app.Clear(color)

    app.Draw(sprite)


    while app.GetEvent(event):

        if event.Type == sf.Event.KeyPressed:
            if event.Key.Code == sf.Key.Escape:
                app.Close()
                sys.exit(0)
        elif event.Type == sf.Event.Closed:
            sys.exit(0)


    app.Display()

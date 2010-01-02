from PySFML import sf

class Control:

    def __init__(self, input):
        self.input = input
        self.update(0)

    def update(self, dt):

        if self.input.IsKeyDown(sf.Key.Left):
            self.left = True
        else:
            self.left = False

        if self.input.IsKeyDown(sf.Key.Right):
            self.right = True
        else:
            self.right = False

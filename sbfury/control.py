from PySFML import sf

class Control:

    def __init__(self, input):
        self.input = input
        self._create_map()
        self.update(0)

    def _create_map(self):
        self.map = {
                'left': sf.Key.Left,
                'right': sf.Key.Right,
                'up': sf.Key.Up,
                'down': sf.Key.Down,
                }

    def update(self, dt):

        for k, v in self.map.items():
            if self.input.IsKeyDown(v):
                setattr(self, k, True)
            else:
                setattr(self, k, False)


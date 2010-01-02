# License: Public Domain
# Author: Hugo Ruscitti (http://www.losersjuegos.com.ar)

from PySFML import sf

class ImageSheet:

    def __init__(self, image, cols=1, rows=1):
        self.image = image
        self.len_frames = cols * rows
        self.cols = cols
        self.rows = rows
        self.frame_width = image.GetWidth() / cols
        self.frame_height = image.GetHeight() / rows
        self.sub_rect = sf.IntRect(0, 0, self.frame_width, self.frame_height)
        self.SetFrameIndex(0)

    def get_center(self):
        return self.frame_width / 2, self.frame_height - 10

    def SetFrameIndex(self, index):
        self.index = index

        frame_col = index % self.cols
        frame_row = index / self.cols

        dx = frame_col * self.frame_width - self.sub_rect.Left
        dy = frame_row * self.frame_height - self.sub_rect.Top

        self.sub_rect.Offset(dx, dy)

    def Assign(self, sprite):
        "Sets the sprite's image with animation state."

        sprite.SetImage(self.image)
        sprite.SetSubRect(self.sub_rect)

    def NextFrame(self):
        has_restarted = False
        current_index = self.index + 1

        if current_index >= self.len_frames:
            current_index = 0
            has_restarted = True

        self.SetFrameIndex(current_index)
        return has_restarted

    def GetFrameIndex(self):
        return self.index

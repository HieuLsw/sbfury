from pygame.sprite import Sprite

class Text(Sprite):

    def __init__(self, font, fps, string):
        Sprite.__init__(self)
        self.font = font
        self.fps = fps
        self.cache_status = fps.status
        self.string = string
        self._create_image()
        self.z = -90


    def update(self):
        if self.cache_status != self.fps.status:
            self._create_image()

    def _create_image(self):
        self.cache_status = self.fps.status
        self.image = self.font.render(self.string % (self.cache_status))
        self.rect = self.image.get_rect()
        self.rect.right = 630
        self.rect.top = 10

import pygame

class Font:

    def __init__(self):
        pygame.font.init()
        self.small = pygame.font.Font(None, 25)
        self.sizes = {0: self.small}

    def render(self, text, size=0, color=(255, 255, 255)):
        return self.sizes[size].render(text, 1, color)


if __name__ == '__main__':
    f = Font()

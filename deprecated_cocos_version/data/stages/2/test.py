import pygame

screen = pygame.display.set_mode((640, 480))
quit = False

layer_0 = pygame.image.load('layer_0.png')
layer_1 = pygame.image.load('layer_1.png')
layer_2 = pygame.image.load('layer_2.png')
layer_3 = pygame.image.load('layer_3.png')
x = 0

while not quit:
    x -= 0.1

    screen.blit(layer_0, (x, 0))
    screen.blit(layer_1, (x, 0))
    screen.blit(layer_2, (x, 0))
    screen.blit(layer_3, (x, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True
        elif e.type == pygame.KEYDOWN:
            quit = True

    pygame.time.delay(1)
    pygame.display.flip()

#include "SDL.h"
#include "glSDL.h"

#if HAS_SDL_OPENGL_H
#include "SDL_opengl.h"
#else
#ifdef WIN32
#include <windows.h>
#endif
#if defined(__APPLE__) && defined(__MACH__)
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#else
#include <GL/gl.h>
#include <GL/glu.h>
#endif
#endif

void update_events(void)
{
    SDL_Event event;

    while (SDL_PollEvent(&event))
    {
        switch (event.type)
        {
            case SDL_QUIT:
                exit(0);
                break;

            case SDL_KEYDOWN:
                if (event.key.keysym.sym == SDLK_ESCAPE)
                    exit(0);
                break;
        }
    }
}


int main(char argc, char * argv[])
{
    SDL_Surface * screen;
    SDL_Surface * image;
    int flags = SDL_DOUBLEBUF;
    long tick1, tick2;
    int quit = 0;
    float dt = 0.01;

    float angle = 0.0;

    if (SDL_Init(SDL_INIT_VIDEO) == -1)
    {
        printf("Error al iniciar la biblioteca.\n");
    }

    tick1 = SDL_GetTicks();
    atexit(SDL_Quit);

#ifdef HAVE_OPENGL
    flags |= SDL_DOUBLEBUF | SDL_GLSDL;

    screen = SDL_SetVideoMode(640, 480, 0, flags);
    SDL_WM_SetCaption("Using opengl", NULL);
#else
    screen = SDL_SetVideoMode(640, 480, 0, flags);
    SDL_WM_SetCaption("Using software surfaces", NULL);
#endif

    if (! screen)
    {
        printf("No se puede definir el modo de video. \n");
    }

    image = IMG_Load("test.png");

    while (! quit)
    {
        SDL_Rect rect = {50, 50, 0, 0};
        tick2 = SDL_GetTicks();
        dt += ((tick2 - tick1) * 0.001f - dt) * 0.1;
        tick1 = tick2;

        angle += dt * 600;
        glSDL_SetRotation(angle);
        glSDL_SetScale(angle / 600.0, angle / 600.0);

        SDL_BlitSurface(image, NULL, screen, &rect);
        SDL_Flip(screen);

        update_events();
    }


    return 0;
}

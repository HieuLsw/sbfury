/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include <iostream>
#include "director.h"

#ifdef HAVE_OPENGL
    #include "SDL/SDL_opengl.h"
#endif

using namespace std;

Director :: Director(struct Config * config)
{
    int flags = SDL_DOUBLEBUF | SDL_GLSDL;
    int width = 640;
    int height = 480;

    if (config->fullscreen)
    {
        flags |= SDL_FULLSCREEN;
        flags |= SDL_HWSURFACE;
    }

    this->running = true;

    if (SDL_Init(SDL_INIT_EVERYTHING) < 0)
        cout << "Failed to create video" << endl;

    if (config->widescreen)
    {
        width = int(width * 1.2f);
        printf("el ancho ahora es de: %d\n", width);
    }

    if (config->small)
    {
        width /= 2;
        height /= 2;
    }

    this->small_video_mode = config->small;
    this->flat_floor = config->flat_floor;

    screen = SDL_SetVideoMode(width, height, 0, flags);

    if (! screen)
        printf("Can't set video mode: %s \n", SDL_GetError());

    SDL_WM_SetCaption("Shaolin's Blind Fury - C test", NULL);
    set_2d_camera();
}


Director :: ~Director()
{
    SDL_Quit();
}


void Director :: change_scene(Scene * scene)
{
    this->scene = scene;
}

// Time based loop

void Director :: run(void)
{
    long tick1, tick2;
    float dt = 0.01;
    long last_tick;
    int fps = 0;

    tick1 = SDL_GetTicks();
    last_tick = tick1;

    while (this->running)
    {
        tick2 = SDL_GetTicks();

        dt += ((tick2 - tick1) * 0.001f - dt) * 0.1;
        tick1 = tick2;

        process_events();
        control.update(dt);
        this->scene->update(dt);

        if (tick2 - last_tick > 1000.0)
        {
            char buffer [128];
#ifdef HAVE_OPENGL
            sprintf(buffer, "OpenGL, FPS: %d", fps);
#else
            sprintf(buffer, "SDL, FPS: %d", fps);
#endif
            SDL_WM_SetCaption(buffer, NULL);
            fps = 0;
            last_tick += 1000.0;
        }

        // Draw
        this->scene->draw(screen);
        SDL_Flip(screen);
        fps += 1;
    }

    delete this->scene;
}

void Director :: process_events(void)
{
    while (SDL_PollEvent(&event))
    {
        switch (event.type)
        {
            case SDL_QUIT:
                this->running = false;
                break;

            case SDL_KEYDOWN:
                if (event.key.keysym.sym == SDLK_ESCAPE)
                    this->running = false;
                break;
        }
    }
}

void Director :: run_without_time(void)
{
}


void Director :: set_2d_camera(void)
{
#ifdef HAVE_OPENGL
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    if (small_video_mode)
        glOrtho(0, screen->w * 2.0f, screen->h * 2.0f, 0, -1.0, 1.0);
    else
        glOrtho(0, screen->w, screen->h, 0, -1.0, 1.0);


    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, 0.0f);
    glDisable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);
    glFlush();
#endif
}

void Director :: set_3d_camera(void)
{
#ifdef HAVE_OPENGL
    int width = screen->w;
    int height = screen->h;
    int ow = width;
    int oh = height;
    float scale = 1.0;

    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    if (small_video_mode)
        scale = 0.5;

    gluPerspective(60, scale*width/height, 0.1, 3000.0);

    glMatrixMode(GL_MODELVIEW);


    gluLookAt(ow/2.0, oh/2.0, oh/1.1566, \
               ow / 2.0, oh / 2.0, 0, \
               0.0, 1.0, 0.0);
    glFlush();
#endif
}

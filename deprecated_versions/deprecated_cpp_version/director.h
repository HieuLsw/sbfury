/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _DIRECTOR_H
#define _DIRECTOR_H

#include "SDL/SDL.h"
#include "glSDL.h"

#include "scene.h"
#include "control.h"

#include "config.h"

class Director
{
    public:
        SDL_Surface * screen;
        SDL_Event event;
        Control control;

        Director(struct Config * config);
        ~Director();

        void change_scene(Scene * scene);
        void run_without_time(void);
        void run();

        void set_2d_camera(void);
        void set_3d_camera(void);

        bool flat_floor;

    private:
        bool running;
        Scene * scene;
        bool small_video_mode;

        void process_events();
};

#endif

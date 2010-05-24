/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "sprite.h"
#include "director.h"

class Stage
{
    public:
        Stage(Director * director, Sprite * object_to_follow);
        ~Stage();

        void draw(SDL_Surface * screen);
        void update(float dt);
        void set_right_bound(float right_x);

        float x;

    private:
        Sprite * object_to_follow;
        Director * director;

        float to_x;
        void set_camera_position(float to_x);
        void center_camera_to_show_object(void);
        void set_object_bounds(void);

        SDL_Surface * layer_0;
        SDL_Surface * layer_1;
        SDL_Surface * layer_2;
        SDL_Surface * layer_3;
        SDL_Surface * layer_4;

        int screen_width;
        float right_bound;
};

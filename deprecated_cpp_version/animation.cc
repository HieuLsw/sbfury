/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include <iostream>
#include "animation.h"
#include "common.h"
#include "SDL_rotozoom.h"

using namespace std;

Animation :: Animation(SDL_Surface * image, int frames, float speed)
{
    // si la superficie es externa no la libera.
    must_free_surface = false;
    init(image, frames, speed);
}

Animation :: Animation(const char * path, int frames, float speed)
{
    // si la superficie es interna la libera.
    must_free_surface = true;
    SDL_Surface * image = load_image(path, false);
    init(image, frames, speed);
}

void Animation :: init(SDL_Surface * image, int frames, float speed)
{
    this->frame_width = image->w / frames;
    this->frame_height = image->h;
    this->w = this->frame_width;
    this->h = this->frame_height;
    this->image_width = image->w;

    this->frames = frames;
    this->step = 0;
    this->speed = speed;

    this->image = image;
    this->image_flip = rotozoomSurfaceXY(image, 0, -1, 1, 0);
}

void Animation :: reset(void)
{
    this->step = 0;
}

Animation :: ~Animation()
{
    //if (must_free_surface)
    //    SDL_FreeSurface(image);

    // la segunda superficie simpre es interna, se debe liberar.
    //SDL_FreeSurface(image_flip);
}

int Animation :: update(float dt)
{
    step += dt * speed;

    if (step >= frames)
    {
        step = 0;
        return 1;
    }

    return 0;
}

void Animation :: draw(SDL_Surface * screen, int x, int y, bool flip, int dx)
{
    SDL_Rect src = {int(step) * frame_width, 0, frame_width, frame_height};
    SDL_Rect dst = {x + dx, y, 0, 0};

    if (!flip)
        SDL_BlitSurface(image, &src, screen, &dst);
    else
    {
        src.x = image_width - int(step + 1) * frame_width;
        SDL_BlitSurface(image_flip, &src, screen, &dst);
    }
}

void Animation :: set_frame(int index)
{
    step = (float) index;
}

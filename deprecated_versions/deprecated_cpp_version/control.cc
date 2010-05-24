/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "SDL/SDL.h"
#include "control.h"

Control :: Control()
{
    up = false;
    down = false;
    left = false;
    right = false;
    attack = false;
    jump = false;

    move = false;
}

void Control :: update(float dt)
{
    key = SDL_GetKeyState(NULL);

    up = (key[SDLK_UP] || key[SDLK_k]);
    down = (key[SDLK_DOWN] || key[SDLK_j]);
    left = (key[SDLK_LEFT] || key[SDLK_h]);
    right = (key[SDLK_RIGHT] || key[SDLK_l]);

    move = (up || down || left || right);

    attack = (key[SDLK_s]);
    jump = (key[SDLK_a]);
}

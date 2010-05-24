/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _COMMON_H
#define _COMMON_H

#include "glSDL.h"
#include "SDL/SDL.h"
#include <iostream>
#include "sprite.h"


using namespace std;

SDL_Surface * load_image(const char * path, bool convert);
int compare_sprites(Sprite * a, Sprite * b);
bool are_in_collision(SDL_Rect * a, SDL_Rect * b);


#endif

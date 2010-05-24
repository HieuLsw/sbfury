/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _GROUP_H
#define _GROUP_H

#include "SDL/SDL.h"
#include <list>
#include "sprite.h"

using namespace std;

class Group
{
    public:
        Group();
        ~Group();

        void add(Sprite * sprite);
        void killall(void);
        void update(float dt);
        void draw(SDL_Surface * screen, int x);
        void sort(void);

        list <Sprite *> sprites;
        list <Sprite *> :: iterator i;
};

#endif

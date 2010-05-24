/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "group.h"
#include "common.h"

Group :: Group()
{
}

Group :: ~Group()
{
    killall();
}

void Group :: add(Sprite * sprite)
{
    sprites.push_back(sprite);
}

void Group :: killall(void)
{
    for (i = sprites.begin(); i != sprites.end(); i++)
    {
        delete *i;
    }
}

void Group :: update(float dt)
{
    for (i = sprites.begin(); i != sprites.end(); i++)
        (*i)->update(dt);
}

void Group :: draw(SDL_Surface * screen, int x)
{
    for (i = sprites.begin(); i != sprites.end(); i++)
        (*i)->draw(screen, x);
}

void Group :: sort(void)
{
    sprites.sort(compare_sprites);
}

/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "glSDL.h"
#include "shadow.h"
#include "common.h"

Shadow :: Shadow(Sprite * sprite): Sprite(0, 0)
{
    object_to_follow = sprite;
    animation = new Animation("shadow.png", 1, 1);
    anchor_x = animation->w / 2;
    anchor_y = animation->h - 20;
}

Shadow :: ~Shadow()
{
    delete animation;
}

void Shadow :: update(float dt)
{
    x = object_to_follow->x;
    y = object_to_follow->y;
}

void Shadow :: draw(SDL_Surface * screen, int dx)
{
    float scale = - 0.0025 * object_to_follow->distance_to_floor + 1;

    glSDL_SetScale(scale, scale);
    Sprite::draw(screen, dx);
    glSDL_ResetState();
}

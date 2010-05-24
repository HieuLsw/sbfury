/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _SCENE_H
#define _SCENE_H

#include "common.h"

class Director;

class Scene
{
    public:
        Scene(Director * director);
        virtual ~Scene();
        virtual void update(float dt) = 0;
        virtual void draw(SDL_Surface * screen) = 0;

        Director * director;
};

#endif

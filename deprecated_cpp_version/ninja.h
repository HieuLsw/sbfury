/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _NINJA_C
#define _NINJA_C

#include "SDL/SDL.h"
#include "enemy.h"
#include "animation.h"


class Ninja : public Enemy
{
    public:
        Ninja(Shaolin * shaolin, Group * enemies, Group * objects);
        ~Ninja();

        void update(float dt);

    private:
        void load_animations(void);
};

#endif

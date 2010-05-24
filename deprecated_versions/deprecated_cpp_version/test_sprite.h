/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "sprite.h"

class TestSprite : public Sprite
{
    public:
        TestSprite();
        ~TestSprite();

        void update(float dt);
};

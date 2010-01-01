/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "test_sprite.h"
#include "common.h"

TestSprite :: TestSprite() : Sprite(200, 300)
{
    animation = new Animation("shaolin/stand.png", 4, 5);
    this->anchor_x = animation->w / 2;
    this->anchor_y = animation->h - 8;
    this->flip = true;
}

TestSprite :: ~TestSprite()
{
}

void TestSprite :: update(float dt)
{
    animation->update(dt);
}

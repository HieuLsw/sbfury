/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "ninja.h"
#include "animation.h"

Ninja :: Ninja(Shaolin * shaolin, Group * enemies, Group * objects) : Enemy(shaolin, enemies, objects)
{
    load_animations();
    change_animation(get_animation("hardhit"));
    x = 300;
    y = 300;
}

Ninja :: ~Ninja()
{
}

void Ninja :: update(float dt)
{
    if (x > shaolin->x)
        flip = true;
    else
        flip = false;

    if (are_hit_me(shaolin))
        x += 50;
}

void Ninja :: load_animations(void)
{
    animations["stand"]     = new Animation("ninja/stand.png", 1, 6);
    animations["hitstand1"] = new Animation("ninja/hitstand1.png", 1, 6);
    animations["hitstand2"] = new Animation("ninja/hitstand2.png", 1, 6);
    animations["hardhit"]   = new Animation("ninja/hardhit.png", 4, 6);
    animations["ground"]    = new Animation("ninja/ground.png", 1, 6);

    animations["ground_to_stand"] = new Animation("ninja/ground_to_stand.png", 3, 6);
}

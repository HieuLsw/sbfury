/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "shaolin.h"
#include "common.h"

Shaolin :: Shaolin(Director * director) : Actor(0, 0)
{
    this->x = 100;
    this->y = 350;
    this->animation = NULL;
    this->keys = NULL;
    this->control = & director->control;
    load_animations();

    change_state(new Stand(this));
}

Shaolin :: ~Shaolin()
{
}

void Shaolin :: load_animations(void)
{
    animations["walk"]    = new Animation("shaolin/walk.png", 4, 6);
    animations["stand"]   = new Animation("shaolin/stand.png", 4, 5);
    animations["attack1"] = new Animation("shaolin/attack1.png", 2, 15);
    animations["attack2"] = new Animation("shaolin/attack2.png", 4, 15);
    animations["attack3"] = new Animation("shaolin/attack3.png", 4, 15);
    animations["attack4"] = new Animation("shaolin/attack4.png", 4, 15);

    animations["jump"]    = new Animation("shaolin/jump.png", 3, 6);

    animations["attackjump"] = new Animation("shaolin/attackjump.png", 2, 7);
    animations["attackrun"]  = new Animation("shaolin/attackrun.png", 1, 5);
    animations["attacktake"] = new Animation("shaolin/attacktake.png", 1, 5);
    animations["ground"]     = new Animation("shaolin/ground.png", 1, 5);
    animations["groundtostand"] = new Animation("shaolin/groundtostand.png", 1, 5);
    animations["hardhit"]   = new Animation("shaolin/hardhit.png", 2, 5);
    animations["hitstand1"] = new Animation("shaolin/hitstand1.png", 2, 5);
    animations["hitstand2"] = new Animation("shaolin/hitstand2.png", 2, 5);
    animations["run"]       = new Animation("shaolin/run.png", 4, 5);
    animations["special"]   = new Animation("shaolin/special.png", 5, 5);
    animations["starting"]  = new Animation("shaolin/starting.png", 3, 5);
    animations["take"]      = new Animation("shaolin/take.png", 1, 5);
    animations["throw"]     = new Animation("shaolin/throw.png", 3, 5);
}


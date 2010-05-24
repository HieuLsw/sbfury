/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "enemy.h"

Enemy :: Enemy(Shaolin * shaolin, Group * enemies, Group * objects) : Actor(0, 0)
{
    this->shaolin = shaolin;
    this->enemies = enemies;
    this->objects = objects;
}

Enemy :: ~Enemy()
{
}

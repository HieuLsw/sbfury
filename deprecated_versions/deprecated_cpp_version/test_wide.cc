/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "director.h"
#include "game.h"
#include "scene.h"

int main(int argc, char * argv [])
{
    Director * director;
    Scene * scene;

    director = new Director(true);
    scene = new Game(director);

    director->change_scene(scene);
    director->run();
}

/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include <iostream>
#include <GL/gl.h>
#include "game.h"
#include "shaolin.h"
#include "shadow.h"

// temporal
#include "ninja.h"

#include "test_sprite.h"

using namespace std;

Game :: Game(Director * director) : Scene(director)
{
    Sprite * tmp;

    shaolin = new Shaolin(director);

    group.add(shaolin);
    group.add(new Shadow(shaolin));

    stage = new Stage(director, shaolin);
    // temporal
    tmp = new Ninja(shaolin, & enemies, NULL);
    group.add(tmp);
    enemies.add(tmp);
    group.add(new Shadow(tmp));
}


Game :: ~Game()
{
    // delete shaolin (ya se libera desde el grupo)
    // TODO: no liberar los elementos de enemies, ya que
    //       todos estos forman parte del grupo 'group', y
    //       por lo tanto se liberan dos veces.
    
    delete stage;
}

void Game :: update(float dt)
{
    group.update(dt);
    stage->update(dt);
}

void Game :: draw(SDL_Surface * screen)
{
    stage->draw(screen);

    group.sort();
    group.draw(screen, -stage->x);
}

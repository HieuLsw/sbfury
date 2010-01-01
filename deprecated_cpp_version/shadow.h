/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _SHADOW_H
#define _SHADOW_H

#include "sprite.h"

/**
 * Represeta la sombra que sigue al personaje y los enemigos.
 *
 * Si el sistema soporta opengl, la sombra del personaje se
 * mostrará mas pequeña cuando el personaje se aleja del
 * suelo.
 */
class Shadow: public Sprite
{
    public:
        Shadow(Sprite * sprite);
        ~Shadow();

        Sprite * object_to_follow;
        void update(float dt);
        void draw(SDL_Surface * screen, int dx);
};

#endif

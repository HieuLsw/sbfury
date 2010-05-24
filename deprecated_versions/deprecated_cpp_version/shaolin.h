/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _SHAOLIN_C
#define _SHAOLIN_C

#include "SDL/SDL.h"
#include "actor.h"
#include "states.h"
#include "control.h"
#include "director.h"


/**
 * Representa al personaje protagonista del juego.
 *
 * Este objeto tiene varias animaciones y estados que hereda de la clase
 * Actor. Vea el archivo 'states.h' para mas detalles.
 */
class Shaolin : public Actor
{
    public:
        Shaolin(Director * director);
        ~Shaolin();

        Uint8 * keys;
        Control * control;

    private:
        virtual void load_animations(void);
};

#endif

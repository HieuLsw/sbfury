/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _ACTOR_H
#define _ACTOR_H

#include "common.h"
#include <map>
#include "sprite.h"
#include "animation.h"

class State;

/**
 * Representa un personaje que tiene estados y animaciones.
 *
 * Esta clase define los aspectos generales de un personaje del escenario,
 * contiene una lista de estados y animaciones para cada uno de estos estados.
 *
 * La clase que herede de aquí debe redefinir el método ''load_animations''
 * para cargar sus propias animaciones.
 */
class Actor : public Sprite
{
    public:
        Actor(float x, float y);
        virtual ~Actor();

        void change_state(State * new_state);
        virtual void update(float dt);

        Animation * get_animation(string name);


    protected:

        State * state;
        map <string,Animation*> animations;

        virtual void load_animations(void);
};

#endif

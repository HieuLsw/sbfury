/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _ENEMY_C
#define _ENEMY_C

#include "SDL/SDL.h"
#include "actor.h"
#include "animation.h"

// referencia a otros
#include "shaolin.h"
#include "group.h"

class State;

/**
 * Representa a todos los enemigos del juego.
 *
 * Un enemigo conoce a los siguientes objetos para relacionarse:
 *
 *      - shaolin: el protagonista que controla el jugador.
 *      - enemies: el resto de los enemigos.
 *      - objetos: todos los objetos del escenario.
 * 
 * La referencia la protagonista la necesita para controlar sus
 * movimientos y para comprobar si recibe un golpe de su parte.
 *
 * Las referencias a los grupos de enemigos y objetos las utiliza
 * para colisiones, por ejemplo, si el personaje es arrojado al
 * escenario, este debería golpear con el cuerpo a otros enemigos
 * e incluso destruir cualquier objeto del escenario como cajas
 * o cestos de basura.
 */
class Enemy : public Actor
{
    public:
        Enemy(Shaolin * shaolin, Group * enemies, Group * objects);
        ~Enemy();

        Shaolin * shaolin;
        Group * enemies;
        Group * objects;
};

#endif

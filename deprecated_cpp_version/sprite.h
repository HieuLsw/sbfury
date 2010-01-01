/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _SPRITE_H
#define _SPRITE_H

#include "SDL/SDL.h"
#include "animation.h"

/**
 * Representa un objeto visible en la pantalla del juego.
 *
 * Sprite debería ser la clase superior de cualquier objeto
 * visible del juego. Su función es representar las operaciones
 * básicas, como actualizar e imprimir.
 *
 * Los atributos principales de la clase son su posición (x, y),
 * el punto de control (anchor_x, anchor_y) y la animación
 * que contiene su gráfico a mostrar.
 *
 * Sprite coopera y utiliza a la clase Animation para contener
 * el gráfico a mostrar. Visite la documentación de esa clase
 * para mas detalles.
 *
 * TODO: mejorar la relación con Sprite, no queda claro quien debe
 *       liberar memoria cuando se vincula un Sprite y una Animación.
 */
class Sprite
{
    public:
        Sprite(float x, float y);
        virtual ~Sprite();

        virtual void update(float dt);
        virtual void draw(SDL_Surface * screen, int dx);

        void move(float dx, float dy);
        void change_animation(Animation * animation);
        void set_motion_bounds(int left, int right);

        Animation * animation;

        float x;
        float y;
        int anchor_x;
        int anchor_y;
        bool flip;

        /* Un valor positivo indica separación del suelo, evite
         * asignarle valores negativos. */
        float distance_to_floor;

        /** Rectangulo que se utiliza para colisiones */
        SDL_Rect collision_send;

        void set_collision_send(int y=70, int w=90, int h=30);
        void unset_collision_send();
        bool are_hit_me(Sprite * other);

    protected:
        int stage_left_bound;
        int stage_right_bound;
        bool are_close_to_other_sprite_in_z_plane(Sprite * other);
};

#endif

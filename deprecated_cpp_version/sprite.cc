/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include <iostream>
#include "sprite.h"
#include "common.h"
#include "stdio.h"
#include <assert.h>

using namespace std;

Sprite :: Sprite(float x, float y)
{
    this->x = x;
    this->y = y;
    this->anchor_x = 0;
    this->anchor_y = 0;
    this->flip = 0;
    this->animation = NULL;
    this->distance_to_floor = 0.0;

    // deshabilita las restricciones de movimiento.
    set_motion_bounds(-1, -1);
    unset_collision_send();
}

Sprite :: ~Sprite()
{
    if (animation)
        delete animation;
}

void Sprite :: update(float dt)
{
}

/**
 * Dibuja el Sprite sobre la pantalla principal.
 *
 *      @param screen: una referencia a la pantalla principal (generalmente).
 *      @param dx: el desplazamiento que se le debe aplicar al personaje para
 *                 representar el scroll del escenario.
 */
void Sprite :: draw(SDL_Surface * screen, int dx)
{
    int dst_x = x - anchor_x;
    int dst_y = y - anchor_y - distance_to_floor;

    if (animation)
        animation->draw(screen, dst_x, dst_y, this->flip, dx);
    else
        cout << "Warning: None to print, " <<  this << endl;
}


/**
 * Desplaza el personaje evitando que salga de la zona permita del escenario.
 *
 *      @param dx: desplazamiento horizontal, relativo a la posición actual.
 *      @param dy: desplazamiento vertical, relativo a la posición actual.
 */
void Sprite :: move(float dx, float dy)
{
    x += dx;
    y += dy;

    // Bottom edge.
    if (y > 480)
        y = 480;

    // Top edge.
    if (y < 230)
        y = 230.0;

    // Left edge.
    if (x < 0)
        x = 0;

    // Right edge.
    if (x > 5280.0)
        x = 5280;

    // Aplica los limites del escenario.
    if (stage_right_bound != -1 && stage_left_bound != -1)
    {
        if (x < stage_left_bound)
            x = stage_left_bound;
        else
            if (x > stage_right_bound)
                x = stage_right_bound;
    }
}

/**
 * Cambia la animación actual
 */
void Sprite :: change_animation(Animation * animation)
{
    // TODO: puede que a futuro no se liberen algunas animaciones.
    //
    //if (this->animation)
    //    delete this->animation;

    this->animation = animation;
    this->anchor_x = animation->w / 2;
    this->anchor_y = animation->h - 8;
}

/**
 * Define los límites del escenario impuestos por el objeto State.
 *
 * Si coloca -1 como valor a cada argumento, entonces el objeto no tendrá
 * ninguna restricción horizontal de movimiento.
 */
void Sprite :: set_motion_bounds(int left, int right)
{
    this->stage_left_bound = left;
    this->stage_right_bound = right;

    assert(left < right || (left == -1 && right == -1));
}



/**
 * Emite una colisión para golpear a otros sprites.
 */
void Sprite :: set_collision_send(int y, int w, int h)
{
    if (! flip)
        collision_send.x = x;
    else
        collision_send.x = x - w;

    collision_send.y = this->y - distance_to_floor - y - h;
    collision_send.w = w;
    collision_send.h = h;

    //printf("x=%d, y=%d, w=%d, h=%d\n", collision_send.x, collision_send.y, \
    //        collision_send.w, collision_send.h);
}

/**
 * Elimina la emisión de colisión para otros personajes.
 */
void Sprite :: unset_collision_send()
{
    collision_send.x = 0;
    collision_send.y = 0;
    collision_send.w = 0;
    collision_send.h = 0;
    // printf("Unset my collision send\n");
}


/**
 * Devuelve true si el otro sprite está golpeándolo.
 */
bool Sprite :: are_hit_me(Sprite * other)
{
    SDL_Rect my_area = {x - anchor_x, y - anchor_y - distance_to_floor, \
        animation->frame_width, animation->frame_height};

    if (other->collision_send.w != 0)
        if (are_close_to_other_sprite_in_z_plane(other))
            return are_in_collision(&my_area, &(other->collision_send));

    return false;
}


/**
 * Determina si los está cercano a otro sprite dentro del plano z.
 */
bool Sprite :: are_close_to_other_sprite_in_z_plane(Sprite * other)
{
    return (abs(int(y - other->y)) < 30);
}

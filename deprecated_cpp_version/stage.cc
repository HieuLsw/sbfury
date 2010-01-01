/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "stage.h"
#include "common.h"

#ifdef HAVE_OPENGL
    #include "SDL/SDL_opengl.h"
#endif

Stage :: Stage(Director * director, Sprite * object_to_follow)
{
    this->director = director;
    this->object_to_follow = object_to_follow;
    this->screen_width = director->screen->w;

    layer_0 = load_image("layer_0.png", true);
    layer_1 = load_image("layer_1.png", false);
    layer_2 = load_image("layer_2.png", false);
    layer_3 = load_image("layer_3.png", true);

    x = 0.0;
    to_x = 0.0;
    set_right_bound(640 * 4000);
}

Stage :: ~Stage()
{
    SDL_FreeSurface(layer_0);
    SDL_FreeSurface(layer_1);
    SDL_FreeSurface(layer_2);
    SDL_FreeSurface(layer_3);
}


void Stage :: set_camera_position(float to_x)
{
    // detiene el movimiento si el usuario llega al
    // final de la zona permita. Esto hace que el
    // scroll ya no se desplace hasta que se llame
    // nuevamente al método "set_right_bound(x)".
    if (to_x > right_bound - screen_width)
        to_x = right_bound - screen_width;

    this->to_x = to_x;
}

void Stage :: center_camera_to_show_object(void)
{
    // Define el nuevo punto a mostrar por la cámara, este
    // punto será el necesario para situar al objeto apuntado
    // en el centro de pantalla.
    set_camera_position(object_to_follow->x - screen_width / 2);

    // define el nuevo limite de movimiento para el objeto apuntado.
    set_object_bounds();
}

void Stage :: update(float dt)
{
    float camera_speed = 1.5;
    float delta;
    float distance_to_object = object_to_follow->x  -x - screen_width/2;

    // Cambia la posición de la cámara solo cuando
    // el personaje llega al extermo derecho de la pantalla.
    if (distance_to_object > screen_width / 4)
        center_camera_to_show_object();

    // realiza el movimiento de desplazamiento de la cámara
    // de manera suave.
    delta = (to_x - x);
    x += delta * camera_speed *  dt;

    // Limites generales del escenario.
    if (x < 0)
        x = 0;
    else
    {
        if (x > 4650.0)
            x = 4650.0;
    }

}

void Stage :: set_object_bounds(void)
{
    object_to_follow->set_motion_bounds(to_x, to_x + director->screen->w);
}

void Stage :: draw(SDL_Surface * screen)
{
    int x = (int) this->x;
    SDL_Rect rect = {0, 0, 0, 0};
    SDL_Rect src = {0, 0, screen->w, 480};

    src.x = x / 4.1;
    SDL_BlitSurface(layer_3, &src, screen, &rect);

    src.x = x / 2;
    SDL_BlitSurface(layer_2, &src, screen, &rect);

    src.x = x;
    SDL_BlitSurface(layer_1, &src, screen, &rect);
    rect.y = 221;

    if (director->flat_floor)
    {
        SDL_BlitSurface(layer_0, &src, screen, &rect);
    }
    else
    {
#ifdef HAVE_OPENGL
        float dy = 252;
        director->set_3d_camera();

        // Rotación
        glTranslatef(0, dy, 0);
        glRotated(-10, 1, 0, 0);
        glTranslatef(0, -dy, 0);

        // Aplicado
        glScalef(1, -1, 0);
        glTranslatef(0, -480, 0);

        SDL_BlitSurface(layer_0, &src, screen, &rect);
        director->set_2d_camera();
#endif
    }
}



void Stage :: set_right_bound(float x)
{
    this->right_bound = x;
}

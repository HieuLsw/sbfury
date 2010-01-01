/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _ANIMATION_H
#define _ANIMATION_H


#include "SDL/SDL.h"

/**
 * Representa una animación almacenada en una grilla de cuadros.
 *
 * Gestiona una animación a partir de un archivo que contiene todos
 * los cuadros de animación en disposición horizontal. En el archivo
 * gráfico se deben colocar todos los cuadros de animación en el
 * órden que se quieren mostrar, a menos que use el método ''set_frame''
 * manualmente.
 *
 * En el constructor se debe especificar la cantidad de cuadros que
 * tiene la imagen original junto a la velocidad de animación.
 */
class Animation
{
    public:
        Animation(SDL_Surface * image, int frames, float speed);
        Animation(const char * path, int frames, float speed);
        ~Animation();

        void init(SDL_Surface * image, int frames, float speed);
        int update(float dt);
        void draw(SDL_Surface * screen, int x, int y, bool flip, int dx);
        void reset(void);
        void set_frame(int index);

        // TODO: Eliminar estas variables, ya que cumplen la misma
        //       función que las variables frame_width y frame_height.
        int w;
        int h;

        int frame_width;
        int frame_height;

    private:
        SDL_Surface * image;
        SDL_Surface * image_flip;

        int image_width;
        float step;
        float speed;
        int frames;
        bool must_free_surface;
};

#endif

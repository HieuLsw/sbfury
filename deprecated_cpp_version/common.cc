/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include <iostream>
#include "SDL/SDL_image.h"
#include "common.h"

// Es importante eliminar la barra final '/' de la siguiente constante.
#define PREFIX "../data"

using namespace std;

/**
 * Carga una imagen desde un archivo para generar una superficie.
 *
 *      @param path: la ruta al archivo, sin incluir el prefijo.
 *      @param convert: si debe eliminar el canal alpha.
 */
SDL_Surface * load_image(const char * path, bool convert)
{
    SDL_Surface * original;
    SDL_Surface * tmp;
    char full_path[2048];

    sprintf(full_path, "%s/%s", PREFIX, path);

    cout << "Loading: " << full_path << endl;

    original = IMG_Load(full_path);

    if (! original)
    {
        printf("Can't open file: '%s' \n", path);
        printf("SDL_Error: %s\n", SDL_GetError());
    }

    // convierte la imagen al modo de video de la pantalla. Esta
    // operación agiliza la impresión de gráficos cuando se utiliza
    // SDL como visualizador por Software.
    if (convert)
        tmp = SDL_DisplayFormat(original);
    else
        tmp = SDL_DisplayFormatAlpha(original);

    if (! tmp)
    {
        printf("Can't convert file to display: '%s' \n", path);
        printf("SDL_Error: %s\n", SDL_GetError());
    }

    SDL_FreeSurface(original);

    return tmp;
}


/**
 * Compara cuan alejados están dos personajes entre sí.
 *
 * Esta rutina se utiliza para ordenar varios sprites en
 * base a la distancia que tienen con la cámara del juego. Por
 * ejemplo en un grupo de sprites que se deben imprimir sobre
 * la pantalla.
 */
int compare_sprites(Sprite * a, Sprite * b)
{
    if (a->y < b->y)
        return 1;
    else
        return 0;
}


/**
 * Retorna true si dos rectángulos están en colisión entre sí.
 */
bool are_in_collision(SDL_Rect * a, SDL_Rect * b)
{
    if ((a->x > b->x + b->w) || (a->y > b->y + b->h) ||
        (b->x > a->x + a->w) || (b->y > a->y + a->h)) 
        return false;
    else
        return true;
}

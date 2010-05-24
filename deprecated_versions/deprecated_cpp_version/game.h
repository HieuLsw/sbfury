/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "glSDL.h"

#include "scene.h"
#include "common.h"
#include "sprite.h"
#include "group.h"
#include "stage.h"
#include "shaolin.h"

class Game : public Scene
{
    public:
        Game(Director * director);
        ~Game();
        void update(float dt);
        void draw(SDL_Surface * screen);

        /** contiene todos los objetos visibles del juego */
        Group group;
        Group enemies;
        Sprite * sprite;
        Shaolin * shaolin;

    private:
        Stage * stage;
};

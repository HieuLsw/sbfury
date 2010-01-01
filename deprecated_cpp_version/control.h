/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _CONTROL_H
#define _CONTROL_H

class Control
{
    public:
        Control();

        void update(float dt);

        bool up;
        bool down;
        bool left;
        bool right;
        bool attack;
        bool jump;

        // Specials
        bool move;

    private:
        Uint8 * key;
};

#endif

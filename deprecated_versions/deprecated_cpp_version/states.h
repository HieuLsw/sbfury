/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _SHAOLIN_STATES_H
#define _SHAOLIN_STATES_H

#include "shaolin.h"

class Shaolin;

class State
{
    public:
        State(Shaolin * shaolin);
        ~State();

        Shaolin * shaolin;

        virtual void update(float dt) = 0;
        virtual void on_animation_done(void);
};

class Walk : public State
{
    public:
        Walk(Shaolin * shaolin);
        ~Walk();

        void update(float dt);
};

class Stand : public State
{
    public:
        Stand(Shaolin * shaolin);
        ~Stand();

        void update(float dt);
};


class Attack : public State
{
    public:
        Attack(Shaolin * shaolin);
        ~Attack();

        void update(float dt);
        void on_animation_done(void);
};

class Jump : public State
{
    public:
        Jump(Shaolin * shaolin, int dx, float vy=15);
        ~Jump();

        void update(float dt);
        void on_animation_done(void);
        void update_motion(float dt);

    private:
        int dx;
        float vy;
};

class AttackJump : public Jump
{
    public:
        AttackJump(Shaolin * shaolin, int dx, float vy=17);
        ~AttackJump();

        void update(float dt);
        void on_animation_done(void);

    private:
        int dx;
        float vy;
};

#endif

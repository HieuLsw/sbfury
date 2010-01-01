/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "states.h"

#define SPEED 400



State :: State(Shaolin * shaolin)
{
    this->shaolin = shaolin;
    shaolin->unset_collision_send();
}

State :: ~State()
{
}

void State :: on_animation_done(void)
{
}


Walk :: Walk(Shaolin * shaolin) : State(shaolin)
{
    shaolin->change_animation(shaolin->get_animation("walk"));
}

Walk :: ~Walk()
{
}

void Walk :: update(float dt)
{
    int speed = SPEED;

    if (shaolin->control->left)
    {
        shaolin->move(dt * -speed, 0);
        shaolin->flip = true;

        if (shaolin->control->jump)
            shaolin->change_state(new Jump(shaolin, -speed));
    }

    if (shaolin->control->right)
    {
        shaolin->move(dt * speed, 0);
        shaolin->flip = false;

        if (shaolin->control->jump)
            shaolin->change_state(new Jump(shaolin, speed));
    }

    if (shaolin->control->down)
        shaolin->move(0, dt * speed);

    if (shaolin->control->up)
        shaolin->move(0, -dt * speed);

    if (shaolin->control->attack)
        shaolin->change_state(new Attack(shaolin));


    if (not shaolin->control->move)
        shaolin->change_state(new Stand(shaolin));
}



Stand :: Stand(Shaolin * shaolin) : State(shaolin)
{
    shaolin->change_animation(shaolin->get_animation("stand"));
}


Stand :: ~Stand()
{
}

void Stand :: update(float dt)
{
    if (shaolin->control->move)
        shaolin->change_state(new Walk(shaolin));

    if (shaolin->control->attack)
        shaolin->change_state(new Attack(shaolin));

    if (shaolin->control->jump)
        shaolin->change_state(new Jump(shaolin, 0));
}






Attack :: Attack(Shaolin * shaolin) : State(shaolin)
{
    shaolin->change_animation(shaolin->get_animation("attack1"));
    shaolin->set_collision_send(70, 100, 30);
}


Attack :: ~Attack()
{
}

void Attack :: update(float dt)
{
}

void Attack :: on_animation_done(void)
{
    shaolin->change_state(new Stand(shaolin));
}



Jump :: Jump(Shaolin * shaolin, int dx, float vy) : State(shaolin)
{
    shaolin->change_animation(shaolin->get_animation("jump"));
    this->vy = vy;
    this->dx = dx;
}


Jump :: ~Jump()
{
}

void Jump :: update(float dt)
{
    update_motion(dt);

    shaolin->animation->set_frame(0);
    shaolin->move(dx * dt, 0);

    if (shaolin->control->left)
    {
        shaolin->move(- dt * 80, 0);
        shaolin->flip = true;
    }

    if (shaolin->control->right)
    {
        shaolin->move(dt * 80, 0);
        shaolin->flip = false;
    }

    if (shaolin->control->attack)
        shaolin->change_state(new AttackJump(shaolin, dx, vy));
    
}

void Jump :: on_animation_done(void)
{
}



void Jump :: update_motion(float dt)
{
    shaolin->distance_to_floor += vy * dt * 60;
    vy -= 0.75 * dt * 50;

    // TODO: cambiar el valor 0 por la distancia real al suelo.
    if (shaolin->distance_to_floor < 0.0)
    {
        shaolin->change_state(new Stand(shaolin));
        shaolin->distance_to_floor = 0;
    }
}





AttackJump :: AttackJump(Shaolin * shaolin, int dx, float vy) : Jump(shaolin, dx, vy)
{
    shaolin->change_animation(shaolin->get_animation("attackjump"));
    this->vy = vy;
    this->dx = dx;
}


AttackJump :: ~AttackJump()
{
}

void AttackJump :: update(float dt)
{
    update_motion(dt);
    shaolin->move(dx * dt, 0);
}

void AttackJump :: on_animation_done(void)
{
    shaolin->animation->set_frame(1);
}

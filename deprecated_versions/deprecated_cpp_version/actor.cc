/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include "actor.h"
#include "states.h"


Actor :: Actor(float x, float y) : Sprite(x, y)
{
    this->state = NULL;
}

Actor :: ~Actor()
{
    map<string,Animation*>::iterator iter;

    for (iter = animations.begin(); iter != animations.end(); ++iter)
        delete iter->second;

    // TODO: problema de invocación.
    //delete state;
}

void Actor :: load_animations(void)
{
}

void Actor :: change_state(State * new_state)
{
    if (state)
        delete state;

    state = new_state;
}

Animation * Actor :: get_animation(string name)
{
    animations[name]->reset();
    return animations[name];
}

void Actor :: update(float dt)
{
    int animation_done;

    animation_done = animation->update(dt);
    state->update(dt);

    if (animation_done)
        state->on_animation_done();
}

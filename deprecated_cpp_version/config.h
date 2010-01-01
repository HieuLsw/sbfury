/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#ifndef _CONFIG_H
#define _CONFIG_H

struct Config
{
    bool fullscreen;
    bool widescreen;
    bool small;
    bool flat_floor;
};

int config_parse_arguments(struct Config * config, int argc, char * argv[]);
void config_show_help(char * name);

#endif

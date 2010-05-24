/*
 * Shaolin's Blind Fury
 *
 * Copyright 2008, 2009 - Hugo Ruscitti
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 */

#include <stdio.h>
#include "config.h"
#include <string.h>

/**
 * Analiza los argumentos del programa y define la configuración.
 *
 */
int config_parse_arguments(struct Config * config, int argc, char * argv[])
{
    int i = 1;
    char * string;
    char * program_name = argv[0];

    // valores iniciales por defecto.
    config->widescreen = false;
    config->fullscreen = false;
    config->small = false;
    config->flat_floor = false;

    for (i; i < argc; i ++)
    {
        string = argv[i];

        if (strcmp(string, "--help") == 0)
        {
            config_show_help(program_name);
            return 1;
        }
        else
        {
            if (strcmp(string, "-fs") == 0)
                config->fullscreen = true;
            else
            {
                if (strcmp(string, "-wide") == 0)
                    config->widescreen = true;
                else
                {
                    if (strcmp(string, "-small") == 0)
                        config->small = true;
                    else
                    {

                        if (strcmp(string, "-flat") == 0)
                            config->flat_floor = true;
                        else
                        {
                            printf("Error, %s isn't a valid option.\n", string);
                            printf("run: '%s --help' for help\n", program_name);
                            return 1;
                        }
                    }
                }
            }
        }
    }

    return 0;
}


void config_show_help(char * name)
{
    printf("usage: %s [OPTIONS]\n", name);
    printf("\n");
    printf("\t-fs\tenable fullscreen mode.\n");
    printf("\t-wide\tenable wide screen mode.\n");
    printf("\t-small\treduce window size.\n");
    printf("\t-flat\tset a flat floor.\n");
    printf("\n");
}

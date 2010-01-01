# -*- coding: utf-8 -*-
#
# Shaolin's Blind Fury
# Copyright 2007 2008 Hugo Ruscitti <hugoruscitti@gmail.com>
# http://www.losersjuegos.com.ar
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see http://www.gnu.org/licenses

import sys

HELP_MESSAGE = """
Usage: shaolin [OPTIONS]

where OPTIONS can be:

  -h        show this help message.
  -fs       run in fullscreen video mode.
  -ns       disable sounds effects.
"""

class Options:
    "Administra los parámetros de configuración."

    def __init__(self, version):
        self.fullscreen = False
        self.show_mouse = True
        self.disabled_sound = True
        self.version = version
        self.sound_volume = 3
        self.music_volume = 3

    def parse_args(self, argv):
        "Parse command arguments to apply options"
        vars = {
                '-fs': 'fullscreen',
                '-ns': 'disabled_sound',
                }

        if '--help' in argv or '-h' in argv:
            print HELP_MESSAGE
            sys.exit(0)

        # remove program name in arguments
        argv = argv[1:]

        for k in vars.keys():
            if k in argv:
                setattr(self, vars[k], True)
                argv.remove(k)
                print k, vars[k], self.fullscreen

        for k in argv:
            print "Sorry, '%s' param is not allowed. Try with -h for help" %k
            sys.exit(1)

        print """
Shaolin's Blind Fury - %s
Copyright 2007 Hugo Ruscitti
http://www.losersjuegos.com.ar

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This game comes with NO WARRANTY, to the extent permitted by law.
You may redistribute copies of this program under the terms of the
GNU General Public License. For more information, see the file named
COPYING.
""" %(self.version)

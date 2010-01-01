# RunMeToCreatePackage.py
# Version 0.2
# 2007/04/11
#
# This program was created by Clint (HanClinto) Herron for the April 2007 PyWeek competition.
#
# This program was addapted to create a exe file for sbfury game too.
#
# It packages up basic games created with the Skellington app as EXE files.
# It requires that py2exe be installed on your system.
# Simply run this script, and it will take care of the rest.
#
# This source program is released into the public domain

from distutils.core import setup
import py2exe
import sys
import glob

print "INTRODUCTION:"
print "This program packages up basic games created with the Skellington framework."
print "It works on my machine for my game,"
print "but I can't guarantee that it will work on yours for yours."
print "Py2exe generally does a great job of automatically packaging dependencies,"
print "but I can't guarantee you won't need to tweak with all of this."
print "Still, I hope this give you a good push in the right direction.\n"

# First step is to create a temporary launcher file, similar to the
# run_game.py file, that has the name of the EXE that they wish to create.
# This is a workaround to a problem where EXEs created with py2exe cannot be
# renamed to anything other than that which they were originally created with
# (or else they won't run properly). I don't know of the proper py2exe option
# to fix this.


filename = 'sbfury.exe'
package_name = filename.replace(".exe", "") 

sys.argv.append("py2exe")
sys.argv.append("--bundle")
sys.argv.append("2")
    
setup(
    windows=[
        {
            "script": 'sbfury.py',
            "icon_resources": [(1, "program.ico")]
        }
    ],
    zipfile=None,
    dist_dir=package_name,
    data_files=[ ("data",   glob.glob("../data/*.*")),
                 (".", glob.glob("../README")),
                 (".", glob.glob("../AUTHORS")),
                 (".", glob.glob("../COPYING")),
                 (".", glob.glob("../CHANGELOG")),
                ]
    )

print "\n\nThe game has now been built (see lib/dist directory)."

#!/usr/bin/python
import sys
import os

import Image


INDIVIDUAL_WIDTH = 128

if len(sys.argv) < 2:
    print "usage: %s file_to_split.png" %(sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

try:
    img = Image.open(filename)
except IOError:
    print "Imposible abrir el archivo: %s" %filename
    sys.exit(1)

name = filename[:-4]
width, height = img.size
initial_width = width

x = 0
index = 0
os.mkdir(name)

print "Set up horizontal clip of '%d' pixels" %(INDIVIDUAL_WIDTH)

print "Creating '%s' directory" %(name)

while width > 0:

    right_border = x + INDIVIDUAL_WIDTH

    if right_border > initial_width:
        right_border = initial_width

    part = img.crop((x, 0, right_border, height))

    if index < 10:
        extra = "00"
    elif index < 100:
        extra = "0"
    else:
        extra = ""

    save_name = "%s/%s%d.png" %(name, extra, index)
    part.save(save_name)
    print "Creating:", save_name

    index += 1
    x += INDIVIDUAL_WIDTH
    width -= INDIVIDUAL_WIDTH

#!/bin/bash
for dir in `ls -d */`
do
    echo ""
    echo ""
    echo "Create layer for stage $dir"
    echo "==========================="

    cd $dir
    rm -R -f layer_0 layer_1 layer_2 layer_3 layer_4 layer_5
    ../splitimages.py layer_0.png
    ../splitimages.py layer_1.png
    ../splitimages.py layer_2.png
    ../splitimages.py layer_3.png
    ../splitimages.py layer_4.png

    if [ -f layer_5.png ]
    then
          ../splitimages.py layer_5.png
    fi

    cd ..
done

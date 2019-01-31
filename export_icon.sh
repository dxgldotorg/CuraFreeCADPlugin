#!/bin/bash
# Copyright (c) 2018 Thomas Karl Pietrowski

icon="icon"

for res in 32 64 128 256 512
do
	rm -f $icon.$res.png
	inkscape -z -e $icon.$res.png -w $res -h $res $icon.svg
done

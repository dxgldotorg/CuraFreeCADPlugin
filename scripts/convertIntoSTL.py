import os
import sys

import FreeCAD
import Part
import Mesh

in_fn, out_fn = sys.argv[-2:]

part_object = FreeCAD.open(in_fn)

all_objs_names = part_object.Objects
__objs__ = []

for obj_name in all_objs_names:
    if obj_name.ViewObject:
        if obj_name.ViewObject.isVisible():
            __objs__.append(obj_name)
    else: # <Part::PartFeature>
        __objs__.append(obj_name)

Mesh.export(__objs__, out_fn)
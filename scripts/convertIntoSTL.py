import os
import sys

import FreeCAD
import FreeCADGui
import Part
import Mesh

in_fn, out_fn = sys.argv[-2:]

print("OPENING: {}".format(in_fn))
FreeCADGui.setupWithoutGUI()
part_object = FreeCAD.open(in_fn)

__objs__ = []

for obj_name in part_object.Objects:
    if obj_name.ViewObject:
        if obj_name.ViewObject.isVisible():
            __objs__.append(obj_name)
    else: # <Part::PartFeature>
        __objs__.append(obj_name)

print("EXPORTING: {}".format(out_fn))
Mesh.export(__objs__, out_fn)

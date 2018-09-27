import os
import sys
import argparse

import FreeCAD
import FreeCADGui
import Part
import Mesh

our_args = sys.argv[-4:]
print("ARGS: {}".format(our_args))

parser = argparse.ArgumentParser()
parser.add_argument('--file', nargs='+')
parser.add_argument('--stl', nargs='+')

parsed = parser.parse_args(our_args)

#in_fn, out_fn = sys.argv[-2:]

if len(parsed.file) > 1 or len(parsed.stl) > 1:
    print("Too many arguments for either --file or --stl")
in_fn = os.path.normpath(parsed.file[0])
out_fn = os.path.normpath(parsed.stl[0])

print("INPUT: {}".format(in_fn))
print("OUTPUT: {}".format(out_fn))

FreeCADGui.setupWithoutGUI()
part_object = FreeCAD.open(in_fn)

__objs__ = []

for obj_name in part_object.Objects:
    if obj_name.ViewObject:
        if obj_name.ViewObject.isVisible():
            __objs__.append(obj_name)
    else: # <Part::PartFeature>
        __objs__.append(obj_name)

Mesh.export(__objs__, out_fn)
print("EXPORTED!")

sys.exit(0)

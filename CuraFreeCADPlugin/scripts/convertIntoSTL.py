import os
import sys
import argparse

import math

import FreeCAD
import FreeCADGui
import Part
import Mesh
import MeshPart

our_args = sys.argv[-4:]

parser = argparse.ArgumentParser()
parser.add_argument('--file', nargs='+')
parser.add_argument('--stl', nargs='+')

parsed = parser.parse_args(our_args)

if len(parsed.file) > 1 or len(parsed.stl) > 1:
    print("Too many arguments for either --file or --stl")
in_fn = os.path.normpath(parsed.file[0])
out_fn = os.path.normpath(parsed.stl[0])

FreeCADGui.setupWithoutGUI()
native_file = FreeCAD.open(in_fn)
active_object = native_file.ActiveObject
active_shape = active_object.Shape.copy()

active_mesh = native_file.addObject("Mesh::Feature","Mesh")
active_mesh.Mesh = MeshPart.meshFromShape(Shape = active_shape,
                                          #MaxLength=1, # Mefisto
                                          LinearDeflection = int(1.0 * 10), # Standard
                                          AngularDeflection = math.radians(5), # Standard
                                          Relative = False
                                          )

Mesh.export([active_mesh,], out_fn)

App.getDocument(App.ActiveDocument.Label).removeObject(active_mesh.Label)

App.closeDocument(App.ActiveDocument.Label)

sys.exit(0)

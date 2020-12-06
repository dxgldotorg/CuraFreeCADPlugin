#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse

import math

# import FreeCAD
import FreeCADGui as Gui
import Part
import Mesh
import MeshPart

import uuid

## Types
TYPE_App_DocumentObjectGroup = 'App::DocumentObjectGroup'
TYPE_PartDesign_Body = 'PartDesign::Body'
TYPE_Part_Box = 'Part::Box'
TYPE_Part_Cylinder = 'Part::Cylinder'
TYPE_Part_Sphere = 'Part::Sphere'
TYPE_Part_Cone = 'Part::Cone'
TYPE_Part_Torus = 'Part::Torus'

TYPES_Volumes = [
    TYPE_PartDesign_Body,
    TYPE_Part_Box,
    TYPE_Part_Cylinder,
    TYPE_Part_Sphere,
    TYPE_Part_Cone,
    TYPE_Part_Torus,
]

our_args = sys.argv[-4:]

parser = argparse.ArgumentParser()
parser.add_argument('--file', nargs='+')
parser.add_argument('--stl', nargs='+')

parsed = parser.parse_args(our_args)

if len(parsed.file) > 1 or len(parsed.stl) > 1:
    print("Too many arguments for either --file or --stl")
in_fn = os.path.normpath(parsed.file[0])
out_fn = os.path.normpath(parsed.stl[0])

Gui.setupWithoutGUI()

native_file = FreeCAD.open(in_fn)

# Look for the document in case our document is not active document
documents = App.listDocuments()
document = None
for document_key in documents.keys():
    this_document = documents[document_key]
    if this_document.FileName == in_fn:
        document = this_document

# Ensure recompute
document.recompute()

# Initial list of objects
dObjects = document.Objects

print("Searching objects with shapes...")
dObjects_to_be_removed = []
for dObject in dObjects:
    print("Inspecting object: {}".format(dObject))
    if dObject.TypeId == TYPE_App_DocumentObjectGroup:
        dObjects_to_be_removed.append(dObject)
        for member in dObject.Group:
            dObjects.append(member)
        continue

    # Check for all objects, which have a shape
    if "Shape" not in dir(dObject):
        dObjects_to_be_removed.append(dObject)
        continue
    
    # Whitelist of types
    if not dObject.TypeId in TYPES_Volumes:
        dObjects_to_be_removed.append(dObject)
        continue

for dObject in dObjects_to_be_removed:
    dObjects.remove(dObject)
del dObjects_to_be_removed
print("Found objects: {}".format(dObjects))

meshes = []
print("Generating meshes...")
for dObject in dObjects:
    this_shape = dObject.Shape.copy()

    this_mesh = native_file.addObject("Mesh::Feature", str(uuid.uuid4()))
    this_mesh.Mesh = MeshPart.meshFromShape(
        Shape=this_shape,
        # MaxLength=1, # Mefisto
        LinearDeflection=int(1.0 * 10),  # Standard
        AngularDeflection=math.radians(5),  # Standard
        Relative=False
    )
    meshes.append(this_mesh)

print("Exporting meshes: {}".format(meshes))
Mesh.export(meshes, out_fn)

for mesh in meshes:
    App.getDocument(document.Label).removeObject(mesh.Label)

App.closeDocument(document.Label)

sys.exit(0)

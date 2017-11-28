# Copyright (c) 2016 Thomas Karl Pietrowski

# Uranium
from UM.Platform import Platform # @UnresolvedImport
from UM.Logger import Logger # @UnresolvedImport
from UM.i18n import i18nCatalog # @UnresolvedImport
i18n_catalog = i18nCatalog("FreeCADPlugin")

def getMetaData():
    return {
        "plugin": {
            "name": i18n_catalog.i18nc("@label", "FreeCADPlugin"),
            "author": "Thomas Karl Pietrowski",
            "version": "0.1.0",
            "description": i18n_catalog.i18nc("@info:whatsthis", "Gives you the possibility to open *.FCStd files."),
            "api": 3
        },
        "mesh_reader": [
            {
                "extension": "FCStd",
                "description": i18n_catalog.i18nc("@item:inlistbox", "FreeCAD file")
            },
        ]
    }

def register(app):
    if Platform.isWindows() or Platform.isLinux() or Platform.isOSX(): 
        from . import FreeCADReader # @UnresolvedImport
        return {"mesh_reader": FreeCADReader.FreeCADReader()}
    else:
        Logger.logException("i", "Unsupported OS!")
        return {}

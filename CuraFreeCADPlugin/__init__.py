# Copyright (c) 2019 Thomas Karl Pietrowski

__plugin_name__ = "FreeCAD plugin"
__plugin_id__ = "CuraFreeCADPlugin"

# Uranium
from UM.Platform import Platform  # @UnresolvedImport
from UM.Logger import Logger  # @UnresolvedImport
from UM.i18n import i18nCatalog  # @UnresolvedImport

# This plugins
from . import FreeCADReader

i18n_catalog = i18nCatalog(__plugin_id__)


def getMetaData():
    return {
        "plugin": {
            "name": __plugin_name__,
            "author": "Thomas Karl Pietrowski",
            "version": "0.1.0",
            "description": i18n_catalog.i18nc("@info:whatsthis",
                                              "Gives you the possibility to open *.FCStd files."),
            "api": 3
        },
        "mesh_reader": [
            {
                "extension": "FCStd",
                "description": i18n_catalog.i18nc("@item:inlistbox",
                                                  "FreeCAD files")
            },
        ]
    }


def register(app):
    metadata = {}
    try:
        reader = FreeCADReader.FreeCADReader()
        metadata["mesh_reader"] = reader
    except:
        Logger.logException("e", "An error occured, when loading the reader!")

    return metadata

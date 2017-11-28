# Copyright (c) 2016 Thomas Karl Pietrowski

# built-ins
import os
import platform

# Uranium
from UM.Logger import Logger # @UnresolvedImport
from UM.i18n import i18nCatalog # @UnresolvedImport

# CIU
from .CadIntegrationUtils.CommonCLIReader import CommonCLIReader # @UnresolvedImport

i18n_catalog = i18nCatalog("FreeCADPlugin")

class FreeCADReader(CommonCLIReader):
    def __init__(self):
        super().__init__("FreeCAD")
        self._supported_extensions = [".FCStd".lower(),
                                      ]
        self.scanForAllPaths()

    def areReadersAvailable(self):
        return bool(self._readerForFileformat)

    def exportFileAs(self, options, quality_enum = None):
        Logger.log("d", "Exporting file: %s", options["tempFile"])
        
        cmd = 'FreeCADCmd'

        cmd = [cmd, 
               os.path.join(os.path.split(__file__)[0],
                            "scripts",
                            "convertIntoSTL.py"
                            ),
               '--',
               options["foreignFile"],
               options["tempFile"],
               ]
        self.executeCommand(cmd, cwd = os.path.split(options["foreignFile"])[0])

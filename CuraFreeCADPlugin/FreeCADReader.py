# Copyright (c) 2018 Thomas Karl Pietrowski

# built-ins
import os
import platform

# Uranium
from UM.Application import Application  # @UnresolvedImport
from UM.Logger import Logger  # @UnresolvedImport
from UM.i18n import i18nCatalog  # @UnresolvedImport
from UM.Version import Version  # @UnresolvedImport

# Since 3.4: Register Mimetypes:
if Version("3.4") <= Version(Application.getInstance().getVersion()):
    from UM.MimeTypeDatabase import MimeTypeDatabase, MimeType

# CIU
from .CadIntegrationUtils.CommonCLIReader import CommonCLIReader  # @UnresolvedImport

i18n_catalog = i18nCatalog("FreeCADPlugin")


class FreeCADReader(CommonCLIReader):
    def __init__(self):
        super().__init__()

        if Version("3.4") <= Version(Application.getInstance().getVersion()):
            MimeTypeDatabase.addMimeType(MimeType(name="application/x-extension-fcstd",
                                                  comment="FreeCAD files",
                                                  suffixes=["fcstd"]
                                                  )
                                         )

        self._supported_extensions = [".FCStd".lower(),
                                      ]
        self.scanForAllPaths()

    def areReadersAvailable(self):
        return bool(self._readerForFileformat)

    def openForeignFile(self, options):
        options["fileFormats"].append("stl")

        return super().openForeignFile(options)

    def exportFileAs(self, options, quality_enum=None):
        Logger.log("d", "Exporting file: %s", options["tempFile"])

        cli = 'FreeCADCmd'

        __real_file__ = os.path.realpath(__file__)
        opt = [os.path.join(os.path.split(__real_file__)[0],
                            "macro",
                            "conversion.py"
                            ),
               "--",
               "--file",
               options["foreignFile"],
               "--stl",
               options["tempFile"],
               ]

        cwd = os.path.split(options["foreignFile"])[0]

        try:
            ret = self.executeCommand([cli, ] + opt,
                                      cwd=cwd,
                                      )
        except:
            # Ubuntu: Command name is since bioic in lowercase.
            cli = cli.lower()
            ret = self.executeCommand([cli, ] + opt,
                                      cwd=cwd,
                                      )
        if ret != 0:
            Logger.log("c", "Returncode is not 0!")

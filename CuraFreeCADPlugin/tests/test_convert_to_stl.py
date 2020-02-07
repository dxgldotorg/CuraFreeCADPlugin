# built-ins
import os
import sys
import subprocess

# OS dependent
if sys.platform == "win32":
    import winreg


class Test():
    def __init__(self):
        self._supported_extensions = [".FCStd".lower(),
                                      ]
        self._additional_paths = None
        self.scanForAllPaths()

    def executeCommand(self, command, cwd=os.path.curdir):
        environment_with_additional_path = os.environ.copy()
        if self._additional_paths:
            environment_with_additional_path["PATH"] = os.pathsep.join(
                self._additional_paths) + os.pathsep + environment_with_additional_path["PATH"]
        print("i", "Executing command: {}".format(command))
        p = subprocess.Popen(command,
                             cwd=cwd,
                             env=environment_with_additional_path,
                             shell=True,
                             )
        p.wait()

    def scanForAllPaths(self):
        self._additional_paths = []
        if sys.platform == "win32":
            for file_extension in self._supported_extensions:
                path = self._findPathFromExtension(file_extension)
                print("d", "Found path for {}: {}".format(file_extension, path))
                if path:
                    self._additional_paths.append(path)

    def _findPathFromExtension(self, extension):
        file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, extension)
        file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, os.path.join(file_class,
                                                                              "shell",
                                                                              "open",
                                                                              "command",
                                                                              )
                                       )
        file_class = file_class.split("\"")
        while "" in file_class:
            file_class.remove("")
        file_class = file_class[0]
        path = os.path.split(file_class)[0]
        if os.path.isdir(path):
            return path
        return

    def exportFileAs(self, foreign, stl):
        print("d", "Exporting file: {}".format(stl))

        cmd = r'FreeCADCmd'

        cmd = [cmd,
               # os.path.join(os.curdir,
               #             "scripts",
               #             "convertIntoSTL.py"
               #             ),
               # '--',
               # foreign,
               # stl,
               ]
        self.executeCommand(cmd, cwd=os.path.split(foreign)[0])


t = Test()
t.exportFileAs("test.FCStd", "test.stl")

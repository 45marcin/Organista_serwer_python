from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("amixerControl",  ["amixerControl.py"]),
    Extension("audioFile",  ["audioFile.py"]),
    Extension("audioFileList",  ["audioFileList.py"]),
    Extension("IOSingleton",  ["IOSingleton.py"]),
    Extension("localSettings",  ["localSettings.py"]),
    Extension("mymodule2",  ["main.py"]),
    Extension("singletonStatus",  ["singletonStatus.py"]),
    Extension("text_display",  ["text_display.py"]),
    Extension("vlcPlayer",  ["vlcPlayer.py"]),
    Extension("clock",  ["clock.py"]),
#   ... all your modules that need be compiled ...
]
setup(
    name = 'Organista',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
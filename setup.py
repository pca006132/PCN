from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'includes':['sip']
        }
    },
    windows = [{'script':'main.py',"icon_resources": [(1, "image/icon.ico")]}],
    data_files = [
      ('lib/imageformats', [
        r'C:\Python34\Lib\site-packages\PyQt5\plugins\imageformats\qico.dll'
        ])],
    zipfile = None
)

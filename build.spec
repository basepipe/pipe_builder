# -*- mode: python -*-

import sys
import os

def load_libs(dir):
    for f in os.listdir(pyside_dir):
        if f.startswith("lib"):
            print f
            pyside_libs.append((os.path.join(pyside_dir, f), f))

pyside_libs = []
hidden = []
try:
    import PySide
    print "*********************************PYSIDE*********************************"
    pyside_dir = os.path.dirname(PySide.__file__)
    print "Version %s" % PySide.__version__
    hidden = ['PySide.QtUiTools',
              'PySide.QtXml',
              'PySide.QtTest',

              ]
    load_libs(pyside_dir)
    print "************************************************************************"
except:
    try:
        import PySide2
        pyside_dir = os.path.dirname(PySide2.__file__)
        #load_libs(pyside_dir)
        hidden = ['PySide2.QtPrintSupport',
                  'PySide2.QtTest'
                 ]

        pyside_libs.append(("/usr/local/Cellar/qt/5.9.1/plugins/", ""))
        pyside_libs.append(("/usr/local/Cellar/qt/5.9.1/plugins/platforms/libqcocoa.dylib", ""))
    except:
        print "FAILED TO FIND PYSIDE :("
        sys.exit()

block_cipher = None

#a = Analysis(['src/bin/path_explorer.py'],
a = Analysis(['src/bin/lumber_mill.py'],
             pathex=['src'],
             binaries=[] + pyside_libs,
             datas=[
                 ('src/cfg/*', 'cfg'),
                 ('src/shotgun_api3/lib/httplib2/cacerts.txt', '.')
                    ],
             hiddenimports=hidden +
                            ['ssl',
                            'certifi'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='lumber_mill',
          debug=False,
          strip=False,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='LumberMill')

import sys
if sys.platform == "darwin":
    app = BUNDLE(coll,
             name='LumberMill.app',
             icon='resources/images/lumbermill_icon/ljicon128x128.png',
             info_plist={
                   'NSHighResolutionCapable': 'True'
             },
             bundle_identifier=None)

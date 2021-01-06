# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Main_Ultra_Speaker_No_UI_2020_10_14_ver.py'],
             pathex=['C:\\Window\\Programming\\python\\Project_by_Python\\Ultrasonic_Equalizer\\Final_Build\\Ultrasonic_sound_speaker_algorithm_except_Graph_UI_by_python_build'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Main_Ultra_Speaker_No_UI_2020_10_14_ver',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='Ultra.ico')

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['face_unlock.py'],
    pathex=[],
    binaries=[],
    datas=[('venv310\\Lib\\site-packages\\facenet_pytorch\\data', 'facenet_pytorch\\data'), ('venv310\\Lib\\site-packages\\facenet_pytorch\\models\\20180402-114759-vggface2.pt', 'facenet_pytorch\\models'), ('known_faces', 'known_faces')],
    hiddenimports=['facenet_pytorch', 'facenet_pytorch.models.mtcnn', 'facenet_pytorch.models.inception_resnet_v1', 'torch', 'cv2', 'numpy', 'pyautogui', 'PIL.Image'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='face_unlock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

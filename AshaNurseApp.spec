# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules


# =========================================================
# HIDDEN IMPORTS
# =========================================================

hiddenimports = []

hiddenimports += collect_submodules("core")
hiddenimports += collect_submodules("webview")
hiddenimports += collect_submodules("waitress")
hiddenimports += collect_submodules("whitenoise")

hiddenimports += [
    "config",
    "config.settings",
    "config.urls",
    "config.wsgi",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django.db.backends.sqlite3",
]


# =========================================================
# ANALYSIS
# =========================================================

a = Analysis(
    ['launcher.py'],

    pathex=[],

    binaries=[],

    datas=[
        # Django templates
        ('templates', 'templates'),

        # Original static files
        ('static', 'static'),

        # collectstatic output used by WhiteNoise
        ('staticfiles', 'staticfiles'),

        # Django project
        ('config', 'config'),

        # Main application
        ('core', 'core'),

        # Django management
        ('manage.py', '.'),

        # Application icon
        ('AshaNurseApp.ico', '.'),
    ],

    hiddenimports=hiddenimports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,

    optimize=0,
)


# =========================================================
# PYZ
# =========================================================

pyz = PYZ(a.pure)


# =========================================================
# EXE
# =========================================================

exe = EXE(
    pyz,

    a.scripts,

    [],

    exclude_binaries=True,

    name='AshaNurseApp',

    # Windows EXE icon
    icon='AshaNurseApp.ico',

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=True,

    # IMPORTANT:
    # Prevent CMD/console window from appearing
    console=False,

    disable_windowed_traceback=False,

    argv_emulation=False,

    target_arch=None,

    codesign_identity=None,

    entitlements_file=None,
)


# =========================================================
# COLLECT
# =========================================================

coll = COLLECT(
    exe,

    a.binaries,

    a.datas,

    strip=False,

    upx=True,

    upx_exclude=[],

    name='AshaNurseApp',
)
# -*- mode: python ; coding: utf-8 -*-

# Optimized PyInstaller spec file for FileRenamerTool
# Based on import validation results

import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Get customtkinter package location
try:
    import customtkinter
    import pkg_resources
    ctk_package = pkg_resources.get_distribution('customtkinter')
    ctk_path = Path(ctk_package.location) / 'customtkinter'
except Exception as e:
    print(f"Warning: Could not find customtkinter path: {e}")
    ctk_path = None

# Define data files to include
datas = []

# Add customtkinter assets if available
if ctk_path and ctk_path.exists():
    assets_path = ctk_path / 'assets'
    if assets_path.exists():
        datas.append((str(assets_path), 'customtkinter/assets'))
        print(f"[OK] Added customtkinter assets: {assets_path}")
    else:
        print(f"[WARN] CustomTkinter assets not found at: {assets_path}")

# Define hidden imports based on validation results
hiddenimports = [
    # CustomTkinter core modules
    'customtkinter',
    'customtkinter.windows',
    'customtkinter.windows.widgets',
    'customtkinter.windows.widgets.core_rendering',
    'customtkinter.windows.widgets.font',
    'customtkinter.windows.widgets.image',
    'customtkinter.windows.widgets.scaling',
    'customtkinter.windows.widgets.draw_engine',
    'customtkinter.windows.widgets.frame',
    'customtkinter.windows.widgets.button',
    'customtkinter.windows.widgets.label',
    'customtkinter.windows.widgets.entry',
    'customtkinter.windows.widgets.checkbox',
    'customtkinter.windows.widgets.optionmenu',
    'customtkinter.windows.widgets.scrollable_frame',
    'customtkinter.windows.ctk_input_dialog',
    'customtkinter.windows.ctk_tk',
    
    # Tkinter modules
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    'tkinter.font',
    'tkinter.colorchooser',
    
    # Standard library modules
    'os',
    'json',
    're',
    'sys',
    'traceback',
    'typing',
    
    # Runtime dependencies (optional)
    'darkdetect',
    'darkdetect.theme',
]

# Define excludes to reduce package size
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'IPython',
    'jupyter',
    'notebook',
    'pytest',
    'unittest',
    'doctest',
    'pdb',
    'tkinter.test',
]

a = Analysis(
    [str(current_dir / 'main.py')],
    pathex=[str(current_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
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
    name='FileRenamerTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging, or use --console flag
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
) 
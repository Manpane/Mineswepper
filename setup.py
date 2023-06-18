import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","pygame"],"excludes": ["tkinter"],"include_files":["bomb.png","bomb.ico"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Minesweeper",
        version = "1",
        author="Manoj Neupane",
        description = "Minesweeper",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Mine Sweeper.py", base=base,icon="bomb.ico",shortcutName="Minesweeper",shortcutDir="DesktopFolder")])
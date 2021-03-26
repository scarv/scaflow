#!/usr/bin/env python
"""
Convert .ui_models files to .py files for a give file/directory
"""
import os
import subprocess
import sys

usage = """Compile .ui and .qrc files to .py

  Usage: python build_ui.py [--force] [.ui files|search paths]

  May specify a list of .ui files and/or directories to search recursively for .ui files.
"""

args = sys.argv[1:]

if "--force" in args:
    force = True
    args.remove("--force")
else:
    force = False

if len(args) == 0:
    print(usage)
    sys.exit(-1)

ui_files = []
qrc_files = []
for arg in args:
    if os.path.isfile(arg) and arg.endswith(".ui"):
        ui_files.append(arg)
    elif os.path.isfile(arg) and arg.endswith(".qrc"):
        qrc_files.append(arg)
    elif os.path.isdir(arg):
        # recursively search for ui_models files in this directory
        for path, sd, files in os.walk(arg):
            for f in files:
                if f.endswith(".ui"):
                    ui_files.append(os.path.join(path, f))
                elif f.endswith(".qrc"):
                    qrc_files.append(os.path.join(path, f))

    else:
        print('Argument "%s" is not a directory or .ui file.' % arg)
        sys.exit(-1)

# # rebuild all requested ui_models files
# for ui in ui_files:
#     base, _ = os.path.splitext(ui)
#
#     py = base + ".py"
#     if (
#         not force
#         and os.path.exists(py)
#         and os.stat(ui).st_mtime <= os.stat(py).st_mtime
#     ):
#         print(f"Skipping {py}; already compiled.")
#     else:
#         cmd = f"pyside6-uic {ui} > {py}"
#         print(cmd)
#         try:
#             subprocess.check_call(cmd, shell=True)
#         except subprocess.CalledProcessError:
#             os.remove(py)

for qrc in qrc_files:
    base, _ = os.path.splitext(qrc)

    py = base + "_rc.py"
    if (
        not force
        and os.path.exists(py)
        and os.stat(qrc).st_mtime <= os.stat(py).st_mtime
    ):
        print(f"Skipping {py}; already compiled.")
    else:
        cmd = f"pyside6-rcc {qrc} > {py}"
        print(cmd)
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError:
            os.remove(py)

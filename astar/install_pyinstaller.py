import os
import platform
import shutil
import subprocess
import sys
import zipfile
import glob


def run_pyinstaller() -> None:
    args = ["pyinstaller", "-F"]

    # Bundle graphviz.
    binaries = glob.glob("c:/Program Files/Graphviz*/bin/dot.exe")
    binaries.extend(glob.glob("c:/Program Files/Graphviz*/bin/*.dll"))
    binaries.extend(glob.glob("c:/Program Files/Graphviz*/bin/*.exe"))
    
    for binary in binaries:
        args.append('--add-binary=' + binary + ';graphviz')
    configs = glob.glob("c:/Program Files/Graphviz*/bin/config*")
    for config in configs:
        args.append('--add-data=' + config + ';graphviz')
    
    args.append("main.py")
    #args.append("--debug=imports")
    
    print("Running '" + " ".join(args) + "'...")
    subprocess.run(args, check=True)

def main() -> None:
    run_pyinstaller()

if __name__ == "__main__":
    main()
from pragma import operating_system
from os import getcwd, sep
import os
import sys


def clean_bash_command(file: str, alias: str):
    with open(file, "r") as rfile:
        lines = rfile.readlines()
    backup = lines.copy()
    cleaned = []
    for line in lines:
        if line.startswith("alias "+ alias):
            continue
        if line.startswith("# Python to C command"):
            continue
        cleaned.append(line)
    try: 
        with open(file, "w") as wfile:
            wfile.writelines(cleaned)
    except:
        with open(file, "w") as wfile:
            wfile.writelines(backup)
    os.sync()
    
def install_py2pyc_command():

    if operating_system != "windows":
        print(f"[\033[32mUPDATE\033[0m]: installing py2pyc command now.")
        shell_profile_file = os.path.expanduser('~/.bash_profile')
        shell_aliases_file = os.path.expanduser('~/.bash_aliases')
        shell_config_file = os.path.expanduser('~/.bashrc')
        order = [shell_aliases_file, shell_profile_file, shell_config_file]
        for file in order:
            if os.path.exists(file):
                target = getcwd() + sep + "mkc.py"
                if os.path.exists(target):
                    print(f"[\033[32mUPDATE\033[0m]: writing alias for {target} to {file}")
                    string = '\n# Python to C command \nalias py2pyc="python3 ' + target
                    clean_bash_command(file, "py2pyc")
                    with open(file, "a") as wfile:
                        wfile.write(string + "\n\n")
                    os.sync()
                    print(f"[\033[32mUPDATE\033[0m]: please use the command 'source {file}' to finalize")
                    break
    
    elif operating_system == "windows":
        target = getcwd() + sep + "mkc.py"
        pypath = sys.path[0].rstrip("\\") + "\\py2pyc.cmd"
        with open(pypath, "w") as wfile:
            wfile.write("@echo off\n " + sys.executable + " " + target + " %* \n")


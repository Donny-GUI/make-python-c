from pragma import operating_system
from os import getcwd, sep
import os
import sys


def install_py2pyc_command():

    if operating_system != "windows":
        shell_profile_file = os.path.expanduser('~/.bash_profile')
        shell_aliases_file = os.path.expanduser('~/.bash_aliases')
        shell_config_file = os.path.expanduser('~/.bashrc')
        order = [shell_aliases_file, shell_profile_file, shell_config_file]
        for file in order:
            if os.path.exists(file):
                target = getcwd() + sep + "mkc.py"
                if os.path.exists(target):
                    string = '\n# Python to C command \nalias py2pyc="python3 ' + target
                    with open(file, "a") as wfile:
                        wfile.write(string)
                    os.sync()
                    break
    
    elif operating_system == "windows":
        target = getcwd() + sep + "mkc.py"
        pypath = sys.path[0].rstrip("\\") + "\\py2pyc.cmd"
        with open(pypath, "w") as wfile:
            wfile.write("@echo off\n " + sys.executable + " " + target + " %* \n")

  

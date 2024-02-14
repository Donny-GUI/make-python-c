import platform


operating_system = platform.system().lower()
devnull = "NUL" if operating_system == "windows" else "/dev/null"
python_argument = "python" if operating_system == "windows" else "python3"
pip_argument = "pip" if operating_system == "windows" else "pip3"

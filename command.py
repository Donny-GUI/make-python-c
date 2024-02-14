import subprocess
import platform

build_execution= "build_ext"
inplace = "--inplace"
operating_system = platform.system().lower()
python_argument = "python" if operating_system == "windows" else "python3"
pip_argument = "pip" if operating_system == "windows" else "pip3"
global_python_install = python_argument + " -m " + pip_argument + " install "
remove_dir = "del" if operating_system == "windows" else "rm -r -f"

class Command(object):

    def __init__(self, command: str|list) -> None:
        if isinstance(command, str):
            self._arguments = command.split(" ")
            self._command = command
        elif isinstance(command, list):
            self._command = " ".join(command)
            self._arguments = command
    
    def __call__(self) -> list:
        return self._arguments
    
    def __str__(self) -> str:
        return self._command

    def __len__(self) -> int:
        return len(self._arguments)
    
    def __iter__(self) -> list:
        return iter(self._arguments)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, list):
            return other == self._arguments
        elif isinstance(other, str):
            return other == self._command
        elif isinstance(other, Command):
            return other.command == self.command
        
    def __ne__(self, other) -> bool:
        if isinstance(other, list):
            return other != self._arguments
        elif isinstance(other, str):
            return other != self._command
        elif isinstance(other, Command):
            return other.command != self.command
        
    @property
    def command(self) -> str:
        return self._command
    
    @property 
    def arguments(self) -> list:
        return self._arguments

    @property
    def list(self) -> list:
        return self._arguments
    
    @property
    def string(self) -> str:
        return self._command
    
    def execute(self) -> int | None:
        process = subprocess.Popen(
            self._arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,  # line buffered
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        return process.poll()

    def get_output(self) -> str:
        try:
            result = subprocess.run(self._arguments, capture_output=True, text=True)
            output = result.stdout
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return ""
    
    def check_errors(self) -> bool:
        if self.get_output() == "":
            return True
        return False
    
    def silent_execution(self) -> bool:
        retv = self.get_output()
        if retv == "":
            return False
        return True


def is_package_installed(package_name: str):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def python_file_execution_str(filename: str) -> str:
    return python_argument + " " + filename

def python_execution(string: str, module: bool=False) -> None:
    mod= " -m " if module == True else " "
    s = python_argument + mod + string.lstrip()
    pycommand = Command(s)
    pycommand.execute()

def pip_install(packages: str|list):
    if isinstance(packages, list):
        package = " ".join(packages)
    elif isinstance(packages, str):
        package = packages
    pcommand = Command(pip_argument + " install " + package)
    pcommand.execute()
    
def run_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1,  # line buffered
    )
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()



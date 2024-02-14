import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", message="A NumPy version >=1.17.3 and <1.25.0 is required for this version of SciPy*")

from command import Command, is_package_installed, global_python_install, python_argument, operating_system
from os import listdir, remove, sep, getcwd, sync
from os.path import exists, basename, splitext
import argparse


devnull = "NUL" if operating_system == "windows" else "/dev/null"
gverbose = False


def set_red(string: str):
    return "\033[31m" + string + "\033[0m"

def set_green(string: str):
    return "\033[32m" + string + "\033[0m"

def get_setup_template(ext_modules: str) -> str:
    if isinstance(ext_modules, str):

        return f"""\
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("{ext_modules}")
)
        """
    elif isinstance(ext_modules, list):
        
        exts: list[str] = [f"'{x}'" for x in ext_modules]
        arg = "[" + ", ".join(exts) + "]"
        # ["file.py", "file2.py"]
        return f"""\
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize({arg})
)
        """


def make_setup_file(filename: str) -> str:
    template = get_setup_template(filename)
    with open("setup.py", "w") as wfile:
        wfile.write(template)

def execute_setup_file():
    pythoncommand = Command(python_argument + " setup.py > " + devnull)
    pythoncommand.silent_execution()

def check_cython():
    if is_package_installed("cython") == False:
        pyc = Command(global_python_install + "cython")
        pyc.execute()

def clean_up():
    for file in listdir():
        if file == "setup.py":
            path = getcwd() + sep + file
            remove(path)
            sync()

def mksetup(filenames: list, *args):
    fns = list(getcwd() + sep + x.strip("'") for x in filenames)
    make_setup_file(fns)
    execute_setup_file()
    print("\nFiles")
    for f in fns:
        file = "  [+] " + set_green(splitext(basename(f))[0] + ".c")
        print(file)
    
def python_to_c(filename: str|list):
    print_verbose("Checking cython...")
    check_cython()
    mksetup(filename)
    print("\n" + set_green("Done."))

def get_files_that_exist_and_are_pythonic(files: list) -> list:
    usable = []
    for file in files:
        print_verbose("Checking "+ set_green(file))
        try:
            ext_start = file.split(".")[1]
        except IndexError:
            print_verbose(f"No extension provided for {set_red(file)}")
            continue
        if ext_start.startswith("py"):
            fex = exists(file)
            if fex == True:
                usable.append(file)
            elif fex == False:
                print(f"{set_green(file)} could not be located... Skipping")
        else:
            print_verbose("Extension " + set_red(ext_start) + " not permitted.")
            print(f"Non pythonic file {set_red(file)} not usable. Skipping")

    return usable

def print_examples():
    s = """\n\
py2pyc myfile.py 
py2pyc myfile1.py myfile2.py
py2pyc -h  <or> py2pyc --help
py2pyc -e  <or> py2pyc --show-examples
py2pyc -v  <or> py2pyc --verbose 
    """
    print(s)


def print_verbose(string):
    global gverbose
    if gverbose:
        print(string)


def main():
    global gverbose

    parser = argparse.ArgumentParser(prog="py2pyc", 
                                     description="Convert python to cython",
                                     usage="py2pyc [FILE] [FILE] ...",
                                     argument_default=False, 
                                     exit_on_error=False)
    parser.add_argument("-v", "--verbose", dest="VERB", action="store_true", default=False, help="Show this help message")
    parser.add_argument("FILE", help="File(s) to convert to python c", nargs="+",)
    parser.add_argument("-e", "--show-examples", dest="EX", action="store_true", default=False, help="Show usage examples")

    try:
        args = parser.parse_args()
    except SystemExit:
        return
    
    gverbose = args.VERB

    if args.EX == True:
        print_examples()

    print_verbose("Checking files...")
    files = get_files_that_exist_and_are_pythonic(args.FILE)
    if files == []:
        print(f"\n[{set_red('Error')}]: No usable files provided...")
        return
    elif files != []:
        python_to_c(files)
        return


if __name__ == "__main__":
    main()

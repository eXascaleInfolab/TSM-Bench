from contextlib import contextmanager
import os
import pathlib


@contextmanager
def change_directory(dir_name_or_module):
    # print(dir_name_or_module)
    new_dir = dir_name_or_module

    if not isinstance(dir_name_or_module, str):  # Check if it's a module
        new_dir = os.path.dirname(dir_name_or_module.__file__)
    elif dir_name_or_module.endswith(".py"):  # Check if it's a Python script , e.g., when using __file__
        new_dir = pathlib.Path(dir_name_or_module).parent.resolve()

    original_dir = os.getcwd()
    #print(f"changing directory to {new_dir}")
    os.chdir(new_dir)

    try:
        yield
    finally:
        os.chdir(original_dir)

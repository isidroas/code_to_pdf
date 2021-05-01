import tempfile
import os


# TODO: make a class
temp_folder = "tmp"
with tempfile.TemporaryDirectory() as file:
    temp_folder = file
os.mkdir(temp_folder)

sub_temp_folder = os.path.join(temp_folder, "tmp")
os.mkdir(sub_temp_folder)


def get_temp_folder():
    return temp_folder


def is_excluded(exclude_list, path):
    for exclude in exclude_list:
        if exclude in path:
            return True
    return False


def get_temp_file(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=suffix, dir=sub_temp_folder) as file:
        return file.name

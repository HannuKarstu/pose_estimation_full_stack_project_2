import os
import json
import time
import uuid

from werkzeug.utils import secure_filename

from backend.config import config

dir_path = os.path.dirname(os.path.realpath(__file__))
files_path = config.dict()["filesPath"]


def save_file(file):
    filename = secure_filename(file.filename)

    # Find input file size
    pos = file.tell()
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(pos)

    filename, filepath = create_filepath(filename, file_size)

    print(f"Saving file to '{os.path.basename(os.path.normpath(filepath))}' ")
    file.save(filepath)
    print("- Done")

    return filename, filepath


def create_filepath(filename, file_size, file_index=0):
    # Check if the input file already exists
    filepath = os.path.abspath(os.path.join(files_path, filename))

    if os.path.exists(filepath):
        existing_file_size = os.path.getsize(filepath)

        if not existing_file_size == file_size:
            filename, ext = os.path.splitext(filename)
            filename = f"{filename}_{file_index+1}{ext}"

            filename, filepath = create_filepath(
                filename, file_size, file_index)

    return filename, filepath


def does_file_exist(filepath):
    return os.path.exists(filepath)


def get_file_size(filepath):
    os.path.getsize(filepath)


def create_folders():
    print("Creating folders")
    for key, value in config.dict().items():
        if "path" in key.lower():
            folder = os.path.abspath(value)
            if not os.path.exists(value):
                print(
                    f"- Creating folder: '{os.path.basename(os.path.normpath(folder))}'")
                os.makedirs(folder)
            else:
                print(
                    f"Folder '{os.path.basename(os.path.normpath(folder))}' already found.")


def delete_file(filename):
    if not filename:
        file_status = "no_filename"

    else:
        filepath = os.path.abspath(os.path.join(files_path, filename))

        if not os.path.isfile(filepath):
            file_status = "not_found"
        else:
            os.remove(filepath)
            if os.path.isfile(filepath):
                file_status = "unable_to_delete"
            else:
                file_status = "deleted"

    return file_status


def get_filepath(filename):
    filepath = os.path.abspath(os.path.join(files_path, filename))

    if not os.path.isfile(filepath):
        filepath = None

    return filepath


def open_file(filename):
    file = None

    if not filename:
        file_status = "no_filename"

    else:
        filepath = os.path.abspath(os.path.join(files_path, filename))

        if not os.path.isfile(filepath):
            file_status = "not_found"
        else:
            file = open(filepath, "r")
            if file:
                file_status = "opened"
            else:
                file_status = "unable_to_open"

    return file, file_status


def get_files():
    files = [f for f in os.listdir(files_path) if os.path.isfile(
        os.path.join(files_path, f))]

    return files

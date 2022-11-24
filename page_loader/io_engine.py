import os
from page_loader.name_assigner import get_base_name


def save_data(local_name, save_location, content):
    mode = 'w' if not isinstance(content, bytes) else 'wb'
    absolute_filename = os.path.join(save_location, local_name)
    with open(absolute_filename, mode) as current_file:
        current_file.write(content)
    return absolute_filename


def create_directory(url, save_location):
    directory = os.path.join(save_location, f'{get_base_name(url)}_files')
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def check_directory(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError
    if not os.path.isdir(directory):
        raise NotADirectoryError

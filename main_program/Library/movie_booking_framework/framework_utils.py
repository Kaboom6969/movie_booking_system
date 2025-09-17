import os
import warnings
import csv

TARGET_DIRECTORY = "Data"
def parse_csv_line(line: str) -> list:
    return line.strip().split(',')

def format_csv_line(data_list: list) -> str:
    return ','.join(map(str, data_list)) + '\n'

def overwrite_file(overwrited_file_csv: str, original_file_csv: str, delete_after_overwrite: bool = True) -> None:
    try:
        overwrited_file_csv_path = get_path(overwrited_file_csv)
        original_file_csv_path = get_path(original_file_csv)
        with open(original_file_csv_path, 'r', newline='') as ori_file_r, open(overwrited_file_csv_path, 'w',
                                                                               newline='') as overwrited_file_w:
            ori_file_reader = csv.reader(ori_file_r)  # Create reader for source file
            overwrited_file_writer = csv.writer(overwrited_file_w)  # Create writer for target file
            for row in ori_file_reader:  # Copy each row
                overwrited_file_writer.writerow(row)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"OVERWRITE FILE FAILED! NO FILE FOUND! OVERWRITED FILE:{overwrited_file_csv}\nORIGINAL FILE:{original_file_csv}")
    finally:
        if delete_after_overwrite:
            try:
                if original_file_csv.endswith(".temp"):
                    os.remove(original_file_csv_path)
                else:
                    warnings.warn("The original File is not .temp File!\nYou should not delete it!")
            except FileNotFoundError:
                pass

def _find_project_root(target_directory : str) -> str:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    while True:
        if target_directory in os.listdir(current_directory):
            return os.path.join(current_directory, target_directory)
        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:
            raise FileNotFoundError(f"Cannot Find File!")
        current_directory = parent_directory

def get_path(file) -> str:
    if os.path.isabs(file):
        warnings.warn("Path Is Using in get_path Function! (Should be file)")
        return file
    base_directory = _find_project_root(target_directory= TARGET_DIRECTORY)
    movie_code_csv_path = os.path.join(base_directory, file)
    return movie_code_csv_path
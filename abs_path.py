from pathlib import Path

def return_abs_path(file_name):
    data_folder = "visualizations/" + file_name
    relative_file_path = Path(data_folder)
    absolute_file_path = relative_file_path.absolute()
    return absolute_file_path

def return_abs_path2(file_name):
    data_folder = "apartment/" + file_name
    relative_file_path = Path(data_folder)
    absolute_file_path = relative_file_path.absolute()
    return absolute_file_path
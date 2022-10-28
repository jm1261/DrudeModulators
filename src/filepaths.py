import os


def check_directory_exists(dir_path):
    '''
    Check to see if a directory path exists, if not create one.
    Args:
        dir_path: <string> path to directory
    Return:
        dir_path: <string> path to directory
    '''
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)
    else:
        pass
    return dir_path


def get_filename(file_path):
    '''
    Splits file path to remove directory path and file extensions.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name without path or extensions
    '''
    return os.path.splitext(os.path.basename(file_path))[0]

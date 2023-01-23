import os

from pathlib import Path
from sys import platform
from src.fileIO import load_json
from src.GUI import prompt_for_path


def check_platform():
    '''
    Check operating system.
    Args:
        None
    Returns:
        operating_system: <string> "Windows", "Linux", or "Mac"
    '''
    if platform == 'linux' or platform == 'linux2':
        operating_system = 'Linux'
    elif platform == 'darwin':
        operating_system = 'Mac'
    elif platform == 'win32':
        operating_system = 'Windows'
    return operating_system


def get_directory_paths(root_path):
    '''
    Get target data path and results path from info dictionary file.
    Args:
        root_path: <string> path to root directory
    Returns:
        data_path: <string> path to data directory
        bg_path: <string> path to background directory
        results_path: <string> path to results directory
        info: <dict> information dictionary (info.json)
    '''
    info = load_json(file_path=Path(f'{root_path}/info.json'))
    directory_paths = {}
    for key, value in info.items():
        if 'Path' in key:
            directory_paths.update({key: Path(f'{root_path}/{value}')})
    return info, directory_paths


def extractfile(directory_path,
                file_string):
    '''
    Pull file from directory path.
    Args:
        directory_path: <string> path to file
        file_string: <string> string contained within file name
    Returns:
        array: <array> array of selected files
    '''
    directory_list = sorted(os.listdir(directory_path))
    return [file for file in directory_list if file_string in file]


def get_files_paths(directory_path,
                    file_string):
    '''
    Get target files and directory paths depending on the operating system.
    Args:
        directory_path: <string> path to data directory
        file_string: <string> file extension (e.g. .csv)
    Returns:
        file_paths: <string> path to files
    '''
    operating_system = check_platform()
    if operating_system == 'Linux' or operating_system == 'Mac':
        file_list = extractfile(
            directory_path=directory_path,
            file_string=file_string)
        file_paths = [Path(f'{directory_path}/{file}') for file in file_list]
    elif operating_system == 'Windows':
        file_paths = prompt_for_path(
            default=directory_path,
            title='Select Target File(s)',
            file_path=True,
            file_type=[(f'{file_string}', f'*{file_string}')])
    return file_paths


def get_parent_directory(file_path):
    '''
    Find parent directory name of target file.
    Args:
        file_path: <string> path to file
    Returns:
        parent_directory: <string> parent directory name (not path)
    '''
    dirpath = os.path.dirname(file_path)
    dirpathsplit = dirpath.split('\\')
    parent_directory = dirpathsplit[-1]
    return parent_directory


def get_filename(file_path):
    '''
    Splits file path to remove directory path and file extensions.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name without path or extensions
    '''
    return os.path.splitext(os.path.basename(file_path))[0]


def probe_sample_information(file_path):
    '''
    Pull sample parameters from file name string for various processes.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
    parent_directory = get_parent_directory(file_path=file_path)
    file_name = get_filename(file_path=file_path)
    file_split = file_name.split('_')
    return {
        'Parent Directory': parent_directory,
        f'{parent_directory} File Name': file_name,
        f'{parent_directory} File Path': f'{file_path}',
        f'{parent_directory} Primary String': file_split[0],
        f'{parent_directory} Secondary String': file_split[1]}


def S4_sample_information(file_path):
    '''
    Pull sample parameters for file name string for various processes.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
    parent_directory = get_parent_directory(file_path=file_path)
    file_name = get_filename(file_path=file_path)
    file_split = file_name.split('_')
    return {
        "Parent Directory": parent_directory,
        f'{parent_directory} File Name': file_name,
        f'{parent_directory} File Path': f'{file_path}',
        f'{parent_directory} Primary String': file_split[0],
        f'{parent_directory} Secondary String': '_'.join(file_split[1:])}


def sample_information(file_path):
    '''
    Pull sample parameters based on which type of file is being analysed.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
    parent_directory = get_parent_directory(file_path=file_path)
    if parent_directory == '4PP':
        sample_parameters = probe_sample_information(file_path=file_path)
    elif parent_directory == 'S4':
        sample_parameters = S4_sample_information(file_path=file_path)
    else:
        sample_parameters = {}
    return sample_parameters


def get_all_batches(file_paths):
    '''
    Find all sample batches in series of file paths and append file paths to
    batch names for loop processing.
    Args:
        file_paths: <array> array of target file paths
    Returns:
        parent: <string> parent directory string
        batches: <dict>
            Batch inidicators: respective file paths for all samples in batch
    '''
    batches = {}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        parent = sample_parameters['Parent Directory']
        key = f'{parent} Primary String'
        if sample_parameters[key] in batches.keys():
            batches[f'{sample_parameters[key]}'].append(file)
        else:
            batches.update({f'{sample_parameters[key]}': [file]})
    return parent, batches


def update_batch_dictionary(parent,
                            batch_name,
                            file_paths):
    '''
    Update batch results dictionary.
    Args:
        parent: <string> parent directory identifier
        batch_name: <string> batch name identifier
        file_paths: <array> list of target file paths
    Returns:
        batch_dictionary: <dict>
            Batch Name
            File Names
            File Paths
            Secondary Strings
    '''
    batch_dictionary = {
        f'{parent} Batch Name': batch_name,
        f'{parent} File Name': [],
        f'{parent} File Path': [],
        f'{parent} Secondary String': []}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        for key, value in sample_parameters.items():
            if key in batch_dictionary.keys():
                batch_dictionary[key].append(value)
    return batch_dictionary


def find_S4_measurement(S4_path,
                        sample_details,
                        file_string):
    '''
    Find S4 measurement file for current sample.
    Args:
        S4_path: <string> path to S4 directory
        sample_details: <dict> dictionary containing all sample information
        file_string: <string> file path extension for S4 file
    Returns:
        S4_file: <array> path to S4 file or empty if no file
        S4_details: <dict> S4 parameters (same as sample_information)
    '''
    parent = sample_details['Parent Directory']
    primary = f'{parent} Primary String'
    try:
        S4_files = extractfile(
            directory_path=S4_path,
            file_string=file_string)
        S4_file = []
        S4_details = {}
        for file in S4_files:
            file_path = Path(f'{S4_path}/{file}')
            S4_info = sample_information(file_path=file_path)
            S4_parent = S4_info['Parent Directory']
            S4_primary = f'{S4_parent} Primary String'
            if S4_info[S4_primary] == sample_details[primary]:
                S4_file.append(file_path)
                S4_details.update(S4_info)
    except:
        S4_file = []
        S4_details = {"S4 String": "No S4 File"}
    return S4_file, S4_details

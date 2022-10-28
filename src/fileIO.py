import os
import json
import numpy as np
from src.filepaths import get_filename


def read_sample_data(file_path):
    '''
    Read sample data from csv or json
    Args:
        file_path: <string> path to file
    Returns:
        sample_data: <dict> dictionary containing all required sample data
    '''
    filename = {"File Name": get_filename(file_path=file_path)}
    if os.path.splitext(file_path)[1] == '.json':
        sample_dict = load_json(file_path=file_path)
        sample_data = dict(filename, **sample_dict)
    elif os.path.splitext(file_path)[1] == '.csv':
        res, thick, eps_inf, mu, wav, n, n_upper, n_lower = np.genfromtxt(
            fname=file_path,
            delimiter=',',
            skip_header=2,
            unpack=True)
        sample_dict = {
            "Sheet Resistance": [
                sr for sr in res if isinstance(sr, (float, int))],
            "Film Thickness": [
                t for t in thick if isinstance(t, (float, int))],
            "Epsilon Infinity": [
                e for e in eps_inf if isinstance(e, (float, int))],
            "Electron Mobility": [
                u for u in mu if isinstance(u, (float, int))],
            "Resonant Wavelength": [
                w for w in wav if isinstance(w, (float, int))],
            "Material Index": [
                N for N in n if isinstance(N, (float, int))],
            "Index Upper Bound": [
                n for n in n_upper if isinstance(n, (float, int))],
            "Index Lower Bound": [
                n for n in n_lower if isinstance(n, (float, int))]}
        sample_data = dict(filename, **sample_dict)
    else:
        sample_dict = {}
        sample_data = dict(filename, **sample_dict)
    return sample_data


def load_json(file_path):
    '''
    Extract user variables from json dictionary.
    Args:
        file_path: <string> path to file
    Returns:
        dictionary: <dict> use variables dictionary
    '''
    with open(file_path, 'r') as file:
        return json.load(file)


def convert(o):
    '''
    Check type of data string
    '''
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path,
                    dictionary):
    '''
    Save dictionary to json file.
    Args:
        out_path: <string> path to file, including file name and extension
        dictionary: <dict> python dictionary to save out
    Returns:
        None
    '''
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')

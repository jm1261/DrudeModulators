import json
import numpy as np


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


def load_sheet_resistance(file_path):
    '''
    Load sheet resistances from single column csv file. Works with txt file.
    Args:
        file_path: <string> path to file
    Returns:
        sheet_resistances: <array> sheet resistances array
    '''
    sheet_resistances, _ = np.genfromtxt(
        fname=file_path,
        delimiter=',',
        skip_header=1,
        unpack=True)
    return sheet_resistances


def get_S4_measurements(file_path):
    '''
    Pull required measured parameters from S4 output file and store in batch/
    sample dictionary.
    Args:
        file_path: <string> path to S4 measurements
    Returns:
        batch_dictionary: <dict> sample/batch dictionary containing required
                            parameters to fit the Drude model
    '''
    S4_measurements = load_json(file_path=file_path)
    gratings = S4_measurements['Gratings']
    batch_dictionary = {
        'Refractive Index': [],
        'Refractive Index Error': [],
        'Extinction Coefficient': [],
        'Extinction Coefficient Error': [],
        'Peak Wavelength': [],
        'Peak Wavelength Error': [],
        'Film Thickness': [],
        'Film Thickness Error': [],
        'Figure Of Merit': [],
        'Bad Gratings': []}
    for grating in gratings:
        grating_dict = S4_measurements[f'{grating}']
        if f'{grating} Missing Parameters' in grating_dict.keys():
            pass
        else:
            fano_names = grating_dict[f'{grating} S4 Fano Fit Parameters']
            fano_values = grating_dict[f'{grating} S4 Fano Fit']
            fano_errors = grating_dict[f'{grating} S4 Fano Errors']
            variables = (grating_dict[f'{grating} Variables'])['S4 Strings']
            variable_values = grating_dict[f'{grating} Optimizer Results']
            variable_errors = grating_dict[f'{grating} Optimizer Errors']
            constants = (grating_dict[f'{grating} Constants'])['S4 Strings']
            constant_values = (
                grating_dict[f'{grating} Constants'])['S4 Values']
            if grating_dict[f'{grating} Figure Of Merit'] > 50:
                batch_dictionary['Bad Gratings'].append(f'{grating}')
            else:
                batch_dictionary['Figure Of Merit'].append(
                    grating_dict[f'{grating} Figure Of Merit'])
                for index, name in enumerate(fano_names):
                    if name == 'Peak':
                        batch_dictionary['Peak Wavelength'].append(
                            fano_values[index])
                        batch_dictionary['Peak Wavelength Error'].append(
                            fano_errors[index])
                for index, name in enumerate(variables):
                    if name == 'material_n':
                        batch_dictionary['Refractive Index'].append(
                            variable_values[index])
                        batch_dictionary['Refractive Index Error'].append(
                            variable_errors[index])
                    if name == 'material_k':
                        batch_dictionary['Extinction Coefficient'].append(
                            variable_values[index])
                        batch_dictionary['Extinction Coefficient Error'].append(
                            variable_errors[index])
                    ''' This will need changing soon '''
                    if name == 'grating_thickness':
                        batch_dictionary['Film Thickness Error'].append(
                            variable_errors[index])
                for index, name in enumerate(constants):
                    if name == 'film_thickness':
                        batch_dictionary['Film Thickness'].append(
                            constant_values[index])
    if len(batch_dictionary['Peak Wavelength']) == 0:
        batch_dictionary = {'Skip': True}
    return batch_dictionary


def get_mobilities():
    '''
    '''
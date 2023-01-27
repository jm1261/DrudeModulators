import json
import math
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


def get_refractiveindex(grating_name,
                        grating_dictionary):
    '''
    Pull refractive index and refractive index error from grating dictionary in
    S4 output file.
    Args:
        grating_name: <string> grating identifier key
        grating_dictionary: <dict> grating dictionary from S4 output
    Returns:
        TE_RIU: <float> refractive index for TE mode
        RIU_error: <float> refractive index error
    '''
    TE_variables = grating_dictionary[f'{grating_name}_TE Variables']
    TE_strings = TE_variables['S4 Strings']
    TE_results = TE_variables['S4 Guesses']
    TE_index = [
        index
        for index, name
        in enumerate(TE_strings) if name == 'material_n'][0]
    TE_RIU = TE_results[TE_index]
    #TE_opt_errors = grating_dictionary[f'{grating_name}_TE Optimizer Errors']
    #TM_opt_errors = grating_dictionary[f'{grating_name}_TM Optimizer Errors']
    #RIU_error = math.sqrt(
    #    (TE_opt_errors[TE_index]) ** 2
    #    + (TM_opt_errors[TE_index]) ** 2)
    TM_variables = grating_dictionary[f'{grating_name}_TM Variables']
    TM_strings = TM_variables['S4 Strings']
    TM_results = TM_variables['S4 Guesses']
    TM_index = [
        index
        for index, name
        in enumerate(TM_strings) if name == 'material_n'][0]
    TM_RIU = TM_results[TM_index]
    RIU_error = math.sqrt(np.abs(TE_RIU - TM_RIU)) / 2
    return TE_RIU, RIU_error


def get_extinction_coef(grating_name,
                        grating_dictionary):
    '''
    Pull extinction coefficient and refractive index error from grating
    dictionary in S4 output file.
    Args:
        grating_name: <string> grating identifier key
        grating_dictionary: <dict> grating dictionary from S4 output
    Returns:
        TE_k: <float> extinction coefficient for TE mode
        k_error: <float> extinction coefficient error
    '''
    TE_variables = grating_dictionary[f'{grating_name}_TE Variables']
    TE_strings = TE_variables['S4 Strings']
    TE_results = TE_variables['S4 Guesses']
    TE_index = [
        index
        for index, name
        in enumerate(TE_strings) if name == 'material_k'][0]
    TE_k = TE_results[TE_index]
    optimizer_errors = grating_dictionary[f'{grating_name}_TE Optimizer Errors']
    k_error = optimizer_errors[TE_index]
    return TE_k * 10, k_error


def get_peak_wavelength(grating_name,
                        grating_dictionary):
    '''
    Pull extinction coefficient and refractive index error from grating
    dictionary in S4 output file.
    Args:
        grating_name: <string> grating identifier key
        grating_dictionary: <dict> grating dictionary from S4 output
    Returns:
        peak_wavelength: <float> resonant wavelength in nm
        peak_error: <float> resonant wavelength error in nm
    '''
    TE_names = grating_dictionary[f'{grating_name}_TE Fano Fit Parameters']
    TE_values = grating_dictionary[f'{grating_name}_TE Fano Fit']
    TE_errors = grating_dictionary[f'{grating_name}_TE Fano Errors']
    TE_index = [
        index
        for index, name
        in enumerate(TE_names) if name == 'Peak'][0]
    peak_wavelength = TE_values[TE_index]
    peak_error = TE_errors[TE_index]
    return peak_wavelength, peak_error


def get_films_thickness(grating_name,
                        grating_dictionary):
    '''
    Pull film thickness and film thickness error from grating dictionary in
    S4 output file.
    Args:
        grating_name: <string> grating identifier key
        grating_dictionary: <dict> grating dictionary from S4 output
    Returns:
        film_thickness: <float> film thickness for TE mode
        film_error: <float> film thickness error
    '''
    TE_variables = grating_dictionary[f'{grating_name}_TE Variables']
    TE_strings = TE_variables['S4 Strings']
    TE_results = TE_variables['S4 Guesses']
    TE_index = [
        index
        for index, name
        in enumerate(TE_strings) if name == 'film_thickness'][0]
    TE_film_thickness = TE_results[TE_index]
    TM_variables = grating_dictionary[f'{grating_name}_TM Variables']
    TM_strings = TM_variables['S4 Strings']
    TM_results = TM_variables['S4 Guesses']
    TM_index = [
        index
        for index, name
        in enumerate(TM_strings) if name == 'film_thickness'][0]
    TM_film_thickness = TM_results[TM_index]
    film_thickness = (TE_film_thickness + TM_film_thickness) / 2
    film_error = np.abs(film_thickness - TM_film_thickness)
    return film_thickness, film_error


def get_fom(grating_name,
            grating_dictionary):
    '''
    Pull figure of merit from grating dictionary in S4 output file.
    Args:
        grating_name: <string> grating identifier key
        grating_dictionary: <dict> grating dictionary from S4 output
    Returns:
        fom: <float> figure of merit for grating
    '''
    TE_fom = grating_dictionary[f'{grating_name}_TE Figure Of Merit']
    TM_fom = grating_dictionary[f'{grating_name}_TM Figure Of Merit']
    fom = TE_fom + TM_fom
    return fom


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
        'Figure Of Merit': []}
    for grating in gratings:
        grating_dict = S4_measurements[f'{grating}']
        if f'{grating} Missing Parameters' in grating_dict.keys():
            pass
        else:
            index, index_error = get_refractiveindex(
                grating_name=f'{grating}',
                grating_dictionary=grating_dict)
            extinction, extinction_error = get_extinction_coef(
                grating_name=f'{grating}',
                grating_dictionary=grating_dict)
            peak, peak_error = get_peak_wavelength(
                grating_name=f'{grating}',
                grating_dictionary=grating_dict)
            film_thickness, film_error = get_films_thickness(
                grating_name=f'{grating}',
                grating_dictionary=grating_dict)
            fom = get_fom(
                grating_name=f'{grating}',
                grating_dictionary=grating_dict)
            batch_dictionary['Refractive Index'].append(index)
            batch_dictionary['Refractive Index Error'].append(index_error)
            batch_dictionary['Extinction Coefficient'].append(extinction)
            batch_dictionary['Extinction Coefficient Error'].append(
                extinction_error)
            batch_dictionary['Peak Wavelength'].append(peak)
            batch_dictionary['Peak Wavelength Error'].append(peak_error)
            batch_dictionary['Film Thickness'].append(film_thickness)
            batch_dictionary['Film Thickness Error'].append(film_error)
            batch_dictionary['Figure Of Merit'].append(fom)
    if len(batch_dictionary['Peak Wavelength']) == 0:
        batch_dictionary = {'Skip': True}
    return batch_dictionary

import json
import numpy as np


def get_real_guesses_bounds(conductivity,
                            mobility,
                            drude_parameters):
    '''
    Get real Drude variable guesses and error bounds from measured parameters
    and user set guesses.
    Args:
        conductivity: <dict> measured conductivity dictionary
        mobility: <float> mobility in cm2/Vs
        drude_parameters: <dict> user input guess dictionary
                            (Drude_parameters.json)
    Returns:
        guesses_bounds: <dict> dictionary containing variable names, guesses,
                        and bounds (bounds set for optimize curve_fit)
    '''
    required_names = ['Effective Mass', 'Epsilon Infinity']
    initial_names = ['Conductivity', 'Mobility']
    initial_guesses = [conductivity['Conductivity'], mobility]
    initial_lowers = [
        conductivity['Conductivity'] - conductivity['Conductivity Error'],
        0]
    initial_uppers = [
        conductivity['Conductivity'] + conductivity['Conductivity Error'],
        50]
    variable_names = drude_parameters['Names']
    variable_guesses = drude_parameters['Guesses']
    variable_bounds = drude_parameters['Bounds']
    for index, name in enumerate(variable_names):
        if name in required_names:
            initial_names.append(name)
            initial_guesses.append(variable_guesses[index])
            initial_lowers.append((variable_bounds[index])[0])
            initial_uppers.append((variable_bounds[index])[1])
    bounds = (tuple(initial_lowers), tuple(initial_uppers))
    return {
        'Real Variable Names': [name for name in initial_names],
        'Real Initial Guesses': [guess for guess in initial_guesses],
        'Real Bounds': bounds}


def get_imag_guesses_bounds(variables,
                            errors,
                            drude_parameters):
    '''
    Generate error bounds from optimizer results and errors.
    Args:
        variables: <array> popt array from optimizer
        errors: <array> sqrt(diag(pcov)) array from optimizer
        drude_parameters: <dict> user input guesses dictionary
                            (Drude_parameters.json)
    Returns:
        guesses_bounds: <dict> dictionary containing variable names
    '''
    initial_names = ['Conductivity']
    drude_names = drude_parameters['Names']
    [initial_names.append(name) for name in drude_names]
    drude_guesses = drude_parameters['Guesses']
    drude_errors = drude_parameters['Bounds']
    initial_guesses = [variable for variable in variables]
    initial_lowers = [v - e for v, e in zip(variables, errors)]
    initial_uppers = [v + e for v, e in zip(variables, errors)]
    for index, name in enumerate(drude_names):
        if name == 'Relaxation Time':
            initial_guesses.append(drude_guesses[index])
            initial_lowers.append((drude_errors[index])[0])
            initial_uppers.append((drude_errors[index])[1])
    bounds = (tuple(initial_lowers), tuple(initial_uppers))
    return {
        'Imaginary Variable Names': [name for name in initial_names],
        'Imaginary Initial Guesses': [guess for guess in initial_guesses],
        'Imaginary Bounds': bounds}

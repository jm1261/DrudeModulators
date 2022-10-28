import math
import numpy as np


def mean_array(x):
    '''
    Calculate mean of array.
    Args:
        x: <array> data array
    Returns:
        mean: <float> mean value of x
    '''
    return np.sum(x) / len(x)


def standard_deviation(x):
    '''
    Calculate standard deviation of array.
    Args:
        x: <array> data array
    Returns:
        stdev: <float> standard deviation of x
    '''
    return np.std(x)


def standard_error_mean(x):
    '''
    Standard error of the mean of an array.
    Args:
        x: <array> data array
    Returns:
        SEOM: <float> standard error of the mean of x
    '''
    return np.std(x) / math.sqrt(len(x) - 1)


def standard_quadrature(calculated_parameter,
                        variables,
                        errors):
    '''
    Quadrature error for calculated parameter.
    Args:
        calculated_parameter: <float> value calculated from variables
        variables: <array> variables used to calculate parameter
        errors: <array> errors associated with variables (must be same order)
    Returns:
        delta_parameter: <float> calculated error for calculated_parameter
    '''
    fractional_errors = [
        (error / variable) ** 2
        for variable, error in zip(variables, errors)]
    square_root_fractional_errors = math.sqrt(np.sum(fractional_errors))
    delta_parameter = calculated_parameter * square_root_fractional_errors
    return delta_parameter

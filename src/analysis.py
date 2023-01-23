import math
import numpy as np
import scipy.optimize as opt


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


def resistance_conductivity(film_thickness,
                            sheet_resistance):
    '''
    Calculate conductivity using standard equation
    Args:
        film_thickness: <float> film thickness in m
        sheet_resistances: <float> sheet resistances in Ohm/Sq
    Returns:
        conductivity: <float> conductivity in S/m
    '''
    resistivity = sheet_resistance * film_thickness
    conductivity = 1 / resistivity
    return conductivity


def average_sample_conductivity(film_thicknesses,
                                sheet_resistances):
    '''
    Calculate conductivity from measured sheet resistances and optimized S4
    parameters.
    Args:
        film_thicknesses: <array> film thickness array (can be length 1)
        sheet_resistances: <array> measured sheet resistances
    Returns:
    '''
    conductivity = resistance_conductivity(
        film_thickness=np.mean(film_thicknesses),
        sheet_resistance=np.mean(sheet_resistances))
    conductivity_error = standard_quadrature(
        calculated_parameter=conductivity,
        variables=[np.mean(film_thicknesses), np.mean(sheet_resistances)],
        errors=[np.std(film_thicknesses), np.std(sheet_resistances)])
    return {
        'Conductivity': conductivity,
        'Conductivity Error': conductivity_error}


def calc_permittivities(refractive_indices,
                        refractive_indices_errors,
                        extinction_coefficients,
                        extinction_coefficients_errors):
    '''
    Calculate real and imaginary permittivies and errors from measured
    refractive indices and extinction coefficients.
    Args:
        refractive_indices: <array> measured n values
        refractive_indices_errors: <array> measured n errors
        extinction_coefficients: <array> measured k values
        extinction_coefficients_errors: <array> measured k errors
    Returns:
        Permittivities: <dict>
    '''
    real_permittivities = [
        (n ** 2) - (k ** 2) for n, k
        in zip(refractive_indices, extinction_coefficients)]
    real_permittivities_errors = [
        standard_quadrature(
            calculated_parameter=eps_r,
            variables=[n, k],
            errors=[dn, dk])
        for eps_r, n, k, dn, dk in zip(
            real_permittivities,
            refractive_indices,
            refractive_indices_errors,
            extinction_coefficients,
            extinction_coefficients_errors)]
    imaginary_permittivities = [
        2 * n * k for n, k
        in zip(refractive_indices, extinction_coefficients)]
    imaginary_permittivities_errors = [
        standard_quadrature(
            calculated_parameter=eps_i,
            variables=[n, k],
            errors=[dn, dk])
        for eps_i, n, k, dn, dk in zip(
            real_permittivities,
            refractive_indices,
            refractive_indices_errors,
            extinction_coefficients,
            extinction_coefficients_errors)]
    return {
        'Real Permittivity': [eps_r for eps_r in real_permittivities],
        'Real Permittivity Error': [e for e in real_permittivities_errors],
        'Imaginary Permittivity': [eps_i for eps_i in imaginary_permittivities],
        'Imaginary Permittivity Error': [
            e for e in imaginary_permittivities_errors]}

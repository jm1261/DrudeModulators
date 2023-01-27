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
    print(f'fraction = {fractional_errors}')
    square_root_fractional_errors = math.sqrt(np.sum(fractional_errors))
    print(f'root = {square_root_fractional_errors}')
    delta_parameter = calculated_parameter * square_root_fractional_errors
    print(f'delta = {delta_parameter}')
    return delta_parameter


def resistance_conductivity(film_thickness,
                            sheet_resistance):
    '''
    Calculate conductivity using standard equation
    Args:
        film_thickness: <float> film thickness in nm
        sheet_resistances: <float> sheet resistances in Ohm/Sq
    Returns:
        conductivity: <float> conductivity in S/m
    '''
    resistivity = sheet_resistance * (film_thickness * 1E-9)
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
        conductivity: <dict> conductivity, conductivity error
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
    Calculate real and imaginary permittivities and errors from measured
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
    print(f'eps_r = {real_permittivities}')
    print(f'n = {refractive_indices}, dn = {refractive_indices_errors}')
    print(f'k = {extinction_coefficients}, dk = {extinction_coefficients_errors}')
    real_permittivities_errors = [
        standard_quadrature(
            calculated_parameter=eps_r,
            variables=[n, k],
            errors=[dn, dk])
        for eps_r, n, dn, k, dk in zip(
            real_permittivities,
            refractive_indices,
            refractive_indices_errors,
            extinction_coefficients,
            extinction_coefficients_errors)]
    imaginary_permittivities = [
        2 * n * k for n, k
        in zip(refractive_indices, extinction_coefficients)]
    #imaginary_permittivities_errors = [
    #    standard_quadrature(
    #        calculated_parameter=eps_i,
    #        variables=[n, k],
    #        errors=[dn, dk])
    #    for eps_i, n, dn, k, dk in zip(
    #        real_permittivities,
    #        refractive_indices,
    #        refractive_indices_errors,
    #        extinction_coefficients,
    #        extinction_coefficients_errors)]
    imaginary_permittivities_errors = [
        math.sqrt(((2 * n * dk) ** 2) + ((2 * k * dn) ** 2))
        for n, k, dn, dk in zip(
            refractive_indices,
            extinction_coefficients,
            refractive_indices_errors,
            extinction_coefficients_errors)]
    return {
        'Real Permittivity': [eps_r for eps_r in real_permittivities],
        'Real Permittivity Error': [e for e in real_permittivities_errors],
        'Imaginary Permittivity': [eps_i for eps_i in imaginary_permittivities],
        'Imaginary Permittivity Error': [
            e for e in imaginary_permittivities_errors]}


def calculate_carrier_concs(conductivity,
                            mobility):
    '''
    Calculate carrier concentration from electron mobility and conductivity.
    Args:
        conductivity: <dict> conductivity dictionary
        mobility: <float> mobility in cm2/Vs
    Returns:
        carrier_density: <dict> carrier density, carrier error
    '''
    carrier_density = (
        conductivity['Conductivity']
        / (mobility * 1E-4 * 1.60217663E-19))
    carrier_error = standard_quadrature(
        calculated_parameter=carrier_density,
        variables=[conductivity['Conductivity']],
        errors=[conductivity['Conductivity Error']])
    return {
        'Carrier Density': carrier_density,
        'Carrier Error': carrier_error}


def wavelength_or_frequency(wavelength_or_frequency):
    '''
    Convert wavelength to frequency, or frequency to wavelength.
    Args:
        wavelength_or_frequency: <float/int> wavelength in meters or frequency
                                in hertz
    Returns:
        wavelength/frequency: <float> returns calculated wavelength or frequency
    '''
    frequency_or_wavelength = 299792458 / wavelength_or_frequency
    return frequency_or_wavelength


def peaks_to_angularfrequencies(resonant_peaks,
                                resonant_peaks_errors):
    '''
    Convert measured resonant wavelengths to angular frequencies.
    Args:
        resonant_peaks: <array> resonant peak wavelengths in nm
        resonant_peaks_errors: <array> resonant peak wavelengths errors in nm
    Returns:
        angular_frequencies: <dict> angular frequency, angular frequency error
    '''
    resonant_frequencies = [
        wavelength_or_frequency(wavelength_or_frequency=peak * 1E-9)
        for peak in resonant_peaks]
    resonant_omegas = [2 * np.pi * f for f in resonant_frequencies]
    omegas_errors = [
        standard_quadrature(
            calculated_parameter=omega,
            variables=[p],
            errors=[dp])
        for omega, p, dp in zip(
            resonant_omegas,
            resonant_peaks,
            resonant_peaks_errors)]
    return {
        'Angular Frequency': [omega for omega in resonant_omegas],
        'Angular Frequency Error': [omega for omega in omegas_errors]}


def get_real_guesses_bounds(carrier_density,
                            drude_parameters):
    '''
    Get real Drude variable guesses and error bounds from measured parameters
    and user set guesses.
    Args:
        carrier_density: <dict> carrier density in m^-3, with errors
        drude_parameters: <dict> user input guess dictionary
                            (Drude_parameters.json)
    Returns:
        guesses_bounds: <dict> dictionary containing variable names, guesses,
                        and bounds (bounds set for optimize curve_fit)
    '''
    required_names = ['Effective Mass', 'Epsilon Infinity']
    initial_names = ['Carrier Density']
    initial_guesses = [carrier_density['Carrier Density']]
    initial_lowers = [
        carrier_density['Carrier Density'] - carrier_density['Carrier Error']]
    initial_uppers = [
        carrier_density['Carrier Density'] + carrier_density['Carrier Error']]
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


def plasmafrequency(carrier_density,
                    effective_mass):
    '''
    Calculate the plasma frequency from the Drude model.
    Args:
        carrier_density: <float> free carrier density in m-3
        effective_mass: <float> elemental effective mass
    Returns:
        plasma_frequency: <float> plasma frequency
    '''
    plasma_frequency = math.sqrt(
        (carrier_density * (1.60217663E-19 ** 2))
        / (8.854E-12 * effective_mass * 9.11E-31))
    return plasma_frequency


def real_drude_equation(x,
                        plasma_frequency,
                        epsilon_infinity):
    '''
    Drude model equation for real part of the permittivity. Equation taken from
    literature. Calculate Drude permittivity at one value of omega.
    Args:
        x: <float> wavelength/frequency as an angular frequency
        epsilon_infinity: <float> permittivity at infinite frequency, material
                            dependent
        plasma_frequency: <float> plasma frequency of material
    Returns:
        drude_permittivity: <float> Drude permittivity at angular frequency
    '''
    drude_permittivity = (
        epsilon_infinity * (
            1 - ((plasma_frequency ** 2) / (x ** 2))))
    return drude_permittivity


def real_drude_permittivity(x,
                            carrier_density,
                            effective_mass,
                            epsilon_infinity):
    '''
    Calculate real Drude permittivity from conductivity, mobility, electron
    effective mass, and high frequency permittivity.
    Args:
        x: <float> angular frequency
        carrier_density: <float> carrier density in m^-3
        effective_mass: <float> effective mass material multiplier
        epsilon_infinity: <float> high frequency permittivity
    Returns:
        drude: <float> drude permittivity
    '''
    plasma_frequency = plasmafrequency(
        carrier_density=carrier_density,
        effective_mass=effective_mass)
    drude = real_drude_equation(
        x=x,
        plasma_frequency=plasma_frequency,
        epsilon_infinity=epsilon_infinity)
    return drude


def optimize_real_drude(angular_frequency,
                        real_permittivity,
                        real_permittivity_error,
                        initial_guesses,
                        bounds):
    '''
    Optimize real drude parameters conductivity, mobility, effective mass, and
    epsilon infinity.
    Args:
        angular_frequency: <array> angular frequency values of x data points
        real_permittivity: <array> real permittivity values of x data points
        real_permittivity_error: <array> real permittivity error values of x
                                    data points
        initial_guesses: <array> guesses for carrier density, effective mass,
                            and epsilon infinity
        bounds: <tuple> (lower, upper) error bounds
    Returns:
        results: <dict> popt, sqrt(diag(pcov)) from optimizer
    '''
    popt, pcov = opt.curve_fit(
        f=real_drude_permittivity,
        xdata=angular_frequency,
        ydata=real_permittivity,
        p0=initial_guesses,
        sigma=real_permittivity_error,
        bounds=bounds)
    errors = np.sqrt(np.diag(pcov))
    return {
        'Real Results': [result for result in popt],
        'Real Errors': [error for error in errors]}


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
    initial_names = ['Carrier Density']
    drude_names = drude_parameters['Names']
    [initial_names.append(name) for name in drude_names]
    drude_guesses = drude_parameters['Guesses']
    drude_errors = drude_parameters['Bounds']
    ''' Fix this better, throws error when carrier density error very small '''
    c_errors = [variables[0] * 0.1, errors[1], errors[2]]
    initial_guesses = [variable for variable in variables]
    initial_lowers = [max(v - e, 0) for v, e in zip(variables, c_errors)]
    initial_uppers = [v + e for v, e in zip(variables, c_errors)]
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


def imag_drude_equation(x,
                        plasma_frequency,
                        epsilon_infinity,
                        relaxation_time):
    '''
    Drude model equation for imaginary part of the permittivity. Equation taken
    from literature. Calculate Drude permittivity at one value of omega.
    Args:
        x: <float> wavelength/frequency as an angular frequency
        plasma_frequency: <float> plasma frequency of material
        epsilon_infinity: <float> permittivity at infinite frequency, material
                            dependent
        relaxation_time: <float> relaxation time of electrons (1/T where T is
                        time between collisions)
    Returns:
        drude_permittivity: <float> Drude permittivity at angular frequency
    '''
    drude_permittivity = (
        (epsilon_infinity * (plasma_frequency ** 2))
        / ((x ** 1)  * relaxation_time))
    return drude_permittivity


def imag_drude_permittivity(x,
                            carrier_density,
                            effective_mass,
                            epsilon_infinity,
                            relaxation_time):
    '''
    Calculate imaginary Drude permittivity from conductivity, mobility, electron
    effective mass, high frequency permittivity, and relaxation time.
    Args:
        x: <float> angular frequency
        carrier_density: <float> carrier density in m^-3
        effective_mass: <float> effective mass material multiplier
        epsilon_infinity: <float> high frequency permittivity
        relaxation_time: <float> relaxation time of electrons (1/T where T is
                        time between collisions)
    Returns:
        drude: <float> drude permittivity
    '''
    plasma_frequency = plasmafrequency(
        carrier_density=carrier_density,
        effective_mass=effective_mass)
    drude = imag_drude_equation(
        x=x,
        plasma_frequency=plasma_frequency,
        epsilon_infinity=epsilon_infinity,
        relaxation_time=relaxation_time)
    return drude


def optimize_imag_drude(angular_frequency,
                        imag_permittivity,
                        imag_permittivity_error,
                        initial_guesses,
                        bounds):
    '''
    Optimize imaginary drude parameters conductivity, mobility, effective mass,
    epsilon infinity, and relaxation time.
    Args:
        angular_frequency: <array> angular frequency values of xdata points
        imag_permittivity: <array> imaginary permittivity values of xdata points
        imag_permittivity_error: <array> imaginary permittivity error values of
                                xdata
        initial_guesses: <array> guesses for conductivity, mobility, effective
                        mass and epsilon infinity
        bounds: <tuple> (lower, upper) error bounds
    Returns:
        results: <dict> popt, sqrt(diag(pcov)) from optimizer
    '''
    popt, pcov = opt.curve_fit(
        f=imag_drude_permittivity,
        xdata=angular_frequency,
        ydata=imag_permittivity,
        p0=initial_guesses,
        sigma=imag_permittivity_error,
        bounds=bounds)
    errors = np.sqrt(np.diag(pcov))
    return {
        'Imaginary Results': [result for result in popt],
        'Imaginary Errors': [error for error in errors]}

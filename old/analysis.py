

from src.fileIO import get_real_guesses_bounds, get_imag_guesses_bounds














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
    '''
    resonant_frequencies = [
        wavelength_or_frequency(
            wavelength_or_frequency=peak * 1E-9)
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


def conductivity_to_carrier(conductivity,
                            mobility):
    '''
    Calculate carrier concentration from electron mobility and conductivity.
    Args:
        conductivity: <float> electrical conductivity in S/m
        mobility: <float> carrier mobility in cm2/Vs
    Returns:
        carrier_density: <float> carrier concentration in m-3
    '''
    carrier_density = conductivity / (mobility * 1E-4 * 1.60217663E-19)
    return carrier_density


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
        epsilon_infinity: <float> permittivity at infinite frequnecy, material
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
                            conductivity,
                            mobility,
                            effective_mass,
                            epsilon_infinity):
    '''
    Calculate real Drude permittivity from conductivity, mobility, electron
    effective mass, and high frequency permittivity.
    Args:
        x: <float> angular frequency
        conductivity: <float> conductivity in S/m
        mobility: <float> electron mobility in cm2/(Vs)
        effective_mass: <float> effective mass material multiplier
        epsilon_infinity: <float> high frequency permittivity
    Returns:
        drude: <float> drude permittivity
    '''
    carrier_density = conductivity_to_carrier(
        conductivity=conductivity,
        mobility=mobility)
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
        angular_frequency: <array> angular frequency values of xdata points
        real_permittivity: <array> real permittivity values of xdata points
        real_permittivity_error: <array> real permittivity error values of xdata
        initial_guesses: <array> guesses for conductivity, mobility, effective
                        mass and epslion infinity
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
        epsilon_infinity: <float> permittivity at infinite frequnecy, material
                            dependent
        relaxation_time: <float> relaxation time of electrons (1/T where T is
                        time between collisions)
    Returns:
        drude_permittivity: <float> Drude permittivity at angular frequency
    '''
    drude_permittivity = (
        (epsilon_infinity * (plasma_frequency ** 2))
        / ((x ** 3) * relaxation_time))
    return drude_permittivity


def imag_drude_permittivity(x,
                            conductivity,
                            mobility,
                            effective_mass,
                            epsilon_infinity,
                            relaxation_time):
    '''
    Calculate imaginary Drude permittivity from conductivity, mobility, electron
    effective mass, high frequency permittivity, and relaxation time.
    Args:
        x: <float> angular frequency
        conductivity: <float> conductivity in S/m
        mobility: <float> electron mobility in cm2/(Vs)
        effective_mass: <float> effective mass material multiplier
        epsilon_infinity: <float> high frequency permittivity
        relaxation_time: <float> relaxation time of electrons (1/T where T is
                        time between collisions)
    Returns:
        drude: <float> drude permittivity
    '''
    carrier_density = conductivity_to_carrier(
        conductivity=conductivity,
        mobility=mobility)
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
                        mass and epslion infinity
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


def optimize_drude_permittivity(S4_measurements,
                                conductivity,
                                mobility,
                                drude_parameters,
                                permittivity):
    '''
    Optimize real and imaginary components of the Drude permittivity from
    S4 measurements, conductivity measurements, set Drude guesses, and the real
    and imaginary components of the measured permittivity.
    Args:
        S4_measurements: <dict> S4 measurement components
        conductivity: <dict> calculated conductivity from measured sheet
                        resistance
        mobility: <float> mobility in cm2/Vs
        drude_parameters: <dict> user input guesses dictionary
                            (Drude_parameters.json)
        permittivity: <dict> calculated real and imaginary permittivity
    Returns:
        drude_results: <dict> arguments, calculated angular frequency values,
                        real parameter guesses, real drude results (optimized),
                        imaginary parameter guesses, imaginary drude results
                        (optimized)
    '''
    angular_frequency = peaks_to_angularfrequencies(
        resonant_peaks=S4_measurements['Peak Wavelength'],
        resonant_peaks_errors=S4_measurements[
            'Peak Wavelength Error'])
    real_guesses_bounds = get_real_guesses_bounds(
        conductivity=conductivity,
        mobility=mobility,
        drude_parameters=drude_parameters)
    real_drude_results = optimize_real_drude(
        angular_frequency=angular_frequency[
            'Angular Frequency'],
        real_permittivity=permittivity['Real Permittivity'],
        real_permittivity_error=permittivity[
            'Real Permittivity Error'],
        initial_guesses=real_guesses_bounds[
            'Real Initial Guesses'],
        bounds=real_guesses_bounds['Real Bounds'])
    imag_guesses_bounds = get_imag_guesses_bounds(
        variables=real_drude_results['Real Results'],
        errors=real_drude_results['Real Errors'],
        drude_parameters=drude_parameters)
    imag_drude_results = optimize_imag_drude(
        angular_frequency=angular_frequency[
            'Angular Frequency'],
        imag_permittivity=permittivity[
            'Imaginary Permittivity'],
        imag_permittivity_error=permittivity[
            'Imaginary Permittivity Error'],
        initial_guesses=imag_guesses_bounds[
            'Imaginary Initial Guesses'],
        bounds=imag_guesses_bounds['Imaginary Bounds'])
    results_dictionary = dict(
        S4_measurements,
        **conductivity,
        **drude_parameters,
        **permittivity,
        **angular_frequency,
        **real_guesses_bounds,
        **real_drude_results,
        **imag_guesses_bounds,
        **imag_drude_results)
    return results_dictionary

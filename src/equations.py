import math


def wavelength_or_frequency(speed_of_light,
                            wavelength_or_frequency):
    '''
    Convert wavelength to frequency, or frequency to wavelength.
    Args:
        speed_of_light: <float/int> speed of light constant
        wavelength_or_frequency: <float/int> wavelength in meters or frequency
                                in hertz
    Returns:
        wavelength/frequency: <float> returns calculated wavelength or frequency
    '''
    frequency_or_wavelength = speed_of_light / wavelength_or_frequency
    return frequency_or_wavelength


def sheetresistance_to_conductivity(sheet_resistance,
                                    film_thickness):
    '''
    Calculate conductivity from a sheet resistance measurement.
    Args:
        sheet_resistance: <float> sheet resistance in Ohms/sq
        film_thickness: <float> film thickness in m
    Returns:
        conductivity: <float> electrical conductivity S/m
    '''
    resistivity = sheet_resistance * film_thickness
    conductivity = 1 / resistivity
    return conductivity


def conductivity_to_carrier(conductivity,
                            mobility,
                            electron_charge):
    '''
    Calculate carrier concentration from electron mobility and conductivity.
    Args:
        conductivity: <float> electrical conductivity in S/m
        mobility: <float> carrier mobility in m2/Vs
        electron_charge: <float> electron charge
    Returns:
        carrier_density: <float> carrier concentration in m-3
    '''
    carrier_density = conductivity / (mobility * electron_charge)
    return carrier_density


def plasmafrequency(carrier_density,
                    electron_charge,
                    epsilon_naught,
                    effective_mass):
    '''
    Calculate the plasma frequency from the Drude model.
    Args:
        carrier_density: <float> free carrier density in m-3
        electron_charge: <float> electron charge
        epsilon_naught: <float> permittivity free space
        effective_mass: <float> elemental effective mass
    Returns:
        plasma_frequency: <float> plasma frequency
    '''
    plasma_frequency = math.sqrt(
        (carrier_density * (electron_charge ** 2))
        / (epsilon_naught * effective_mass))
    return plasma_frequency


def drude_permittivity_real(epsilon_infinity,
                            plasma_frequency,
                            angular_frequency):
    '''
    Drude model equation for real part of the permittivity. Equation taken from
    literature. Calculate Drude permittivity at one value of omega.
    Args:
        epsilon_infinity: <float> permittivity at infinite frequnecy, material
                            dependent
        plasma_frequency: <float> plasma frequency of material
        angular_frequency: <float> wavelength/frequency as an angular frequency
    Returns:
        drude_permittivity: <float> Drude permittivity at angular frequency
    '''
    drude_permittivity = (
        epsilon_infinity
        - ((plasma_frequency ** 2) / (angular_frequency ** 2)))
    return drude_permittivity

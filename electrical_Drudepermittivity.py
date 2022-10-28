import os
import numpy as np
import src.GUI as gui
import src.fileIO as io
import src.equations as eq
import src.analysis as anal
import src.plotting as plot


def resistance_to_Drude(sample_data,
                        constants,
                        angular_frequency):
    '''
    Calculates Drude permittivity from sheet resistance measurements. Uses the
    standard equations, and some assumptions, to calculate a Drude permittivity
    from sheet reistance measurements.
    Args:
        sample_data: <dict> dictionary containing all required sample data
        constants: <dict> dictionary of relevant constants
        angular_frequency: <array> angular frequency range over which Drude
                            permittivity is analysed
    Returns:
        results: <dict> dictionary containing:
            sheet resistance, sheet resistance error
            conductivity, conductivity error
            carrier density, carrier density error
            plasma frequency, plasma frequency error
            drude permittivity (array)
            drude permittivity error (array)
    '''
    sheet_resistance, sheet_resistance_error = (
        anal.mean_array(x=sample_data['Sheet Resistance']),
        anal.standard_error_mean(x=sample_data['Sheet Resistance']))

    conductivity = eq.sheetresistance_to_conductivity(
        sheet_resistance=sheet_resistance,
        film_thickness=sample_data['Film Thickness'][0])
    conductivity_error = anal.standard_quadrature(
        calculated_parameter=conductivity,
        variables=[
            sheet_resistance,
            sample_data['Film Thickness'][0]],
        errors=[
            sheet_resistance_error,
            sample_data['Film Thickness'][1]])

    carrier_density = eq.conductivity_to_carrier(
        conductivity=conductivity,
        mobility=sample_data['Electron Mobility'][0],
        electron_charge=constants['Electron Charge'])
    carrier_density_error = anal.standard_quadrature(
        calculated_parameter=carrier_density,
        variables=[sample_data['Electron Mobility'][0], conductivity],
        errors=[sample_data['Electron Mobility'][1], conductivity_error])

    plasma_frequency = eq.plasmafrequency(
        carrier_density=carrier_density,
        electron_charge=constants['Electron Charge'],
        epsilon_naught=constants['Epsilon Naught'],
        effective_mass=(
            constants['Electron Mass'] * constants['Effective Mass ITO']))
    plasma_frequency_error = anal.standard_quadrature(
        calculated_parameter=plasma_frequency,
        variables=[carrier_density],
        errors=[carrier_density_error])

    drude_permittivity = [
        eq.drude_permittivity_real(
            epsilon_infinity=sample_data['Epsilon Infinity'][0],
            plasma_frequency=plasma_frequency,
            angular_frequency=omega)
        for omega in angular_frequency]
    drude_permittivity_error = [
        anal.standard_quadrature(
            calculated_parameter=drude,
            variables=[
                plasma_frequency,
                sample_data['Epsilon Infinity'][0]],
            errors=[
                plasma_frequency_error,
                sample_data['Epsilon Infinity'][1]])
        for drude in drude_permittivity]
    return {
        "Sheet Resistance": [sheet_resistance, sheet_resistance_error],
        "Conductivity": [conductivity, conductivity_error],
        "Carrier Density": [carrier_density, carrier_density_error],
        "Plasma Frequency": [plasma_frequency, plasma_frequency_error],
        "Drude Permittivity": drude_permittivity,
        "Drude Permittivity Error": drude_permittivity_error}


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    file_paths = gui.prompt_for_path(
        default=root,
        title='Select Target File(s)',
        file_path=True,
        file_type=[
            ('json', '*.json'),
            ('CSV', '*.csv'),
            ('All Files', '*')])

    ''' Info '''
    info = io.load_json(
        file_path=os.path.join(
            root,
            'info.json'))

    ''' Constants '''
    constants = io.load_json(
        file_path=os.path.join(
            root,
            'References',
            'Constants.json'))

    ''' Out Path '''
    out_path = gui.prompt_for_path(
        default=root,
        title='Select Out Path',
        dir_path=True)

    ''' Wavelength/Frequency/Angular Frequency '''
    frequency_THz = np.arange(
        info['Frequency THz Range'][0],
        info['Frequency THz Range'][1],
        info['Frequency THz Range'][2])
    omega = [2 * np.pi * f * 1E12 for f in frequency_THz]

    for file in file_paths:
        sample_data = io.read_sample_data(file_path=file)
        calculation_results = resistance_to_Drude(
            sample_data=sample_data,
            constants=constants,
            angular_frequency=omega)
        sample_results = dict(sample_data, **calculation_results)
        io.save_json_dicts(
            out_path=os.path.join(
                out_path,
                f'{sample_data["File Name"]}_Electrical.json'),
            dictionary=sample_results)
        plot.literature_plot(
            drude_permittivity=calculation_results['Drude Permittivity'],
            label=calculation_results['Carrier Density'],
            frequency_range=frequency_THz,
            frequency_ticks=info['Frequency THz Ticks'],
            out_path=os.path.join(
                out_path,
                f'{sample_data["File Name"]}_Electrical.png'))

import os
import numpy as np
import src.GUI as gui
import src.fileIO as io
import src.equations as eq
import src.analysis as anal
import src.plotting as plot


def opticalmeasure_to_Drude(sample_data,
                            constants):
    '''
    Calculate Drude permittivity from refractive index and resonant wavelength
    measurements for a periodic structure in the Drude material.
    Args:
        sample_data: <dict> dictionary containing all required sample data
        constants: <dict> dictionary to relevant constants
    Returns:
        results: <dict> dictionary containing:
            resonant frequency in THz
            resonant frequency error in THz
            real component of drude permittivity
            real component of drude permittivity errors
    '''
    resonant_frequency = [
        eq.wavelength_or_frequency(
            speed_of_light=constants['Speed Light'],
            wavelength_or_frequency=wavelength * 1E-9)
        for wavelength in sample_data['Resonant Wavelength']]
    resonant_frequency_THz = [f / 1E12 for f in resonant_frequency]
    resonant_frequency_error = [
        anal.standard_quadrature(
            calculated_parameter=rf,
            variables=[wavelength * 1E-9],
            errors=[10E-9])
        for rf, wavelength in zip(
            resonant_frequency_THz,
            sample_data['Resonant Wavelength'])]
    real_permittivity = [n ** 2 for n in sample_data['Material Index']]
    real_permittivity_range = [
        (n1 ** 2, n2 ** 2)
        for n1, n2 in zip(
            sample_data['Index Lower Bound'],
            sample_data['Index Upper Bound'])]
    return {
        "Resonant Frequency THz": resonant_frequency_THz,
        "Resonant Frequency Error": resonant_frequency_error,
        "Real Permittivity": real_permittivity,
        "Permittivity Range": real_permittivity_range}


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
        calculation_results = opticalmeasure_to_Drude(
            sample_data=sample_data,
            constants=constants)
        sample_results = dict(sample_data, **calculation_results)
        io.save_json_dicts(
            out_path=os.path.join(
                out_path,
                f'{sample_data["File Name"]}_Optical.json'),
            dictionary=sample_results)
        plot.uncertainty_region_plot(
            frequencies=calculation_results['Resonant Frequency THz'],
            frequency_errors=calculation_results['Resonant Frequency Error'],
            permittivities=calculation_results['Real Permittivity'],
            permittivity_range=calculation_results['Permittivity Range'],
            label=sample_data['File Name'],
            frequency_ticks=info['Frequency THz Ticks'],
            out_path=os.path.join(
                out_path,
                f'{sample_data["File Name"]}_Optical.png'))

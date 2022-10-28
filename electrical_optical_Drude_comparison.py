import os
import numpy as np
import src.GUI as gui
import src.fileIO as io
import src.equations as eq
import src.analysis as anal
import src.plotting as plot
from electrical_Drudepermittivity import resistance_to_Drude
from optical_Drudepermittivity import opticalmeasure_to_Drude


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
        electrical_results = resistance_to_Drude(
            sample_data=sample_data,
            constants=constants,
            angular_frequency=omega)
        optical_results = opticalmeasure_to_Drude(
            sample_data=sample_data,
            constants=constants)
        sample_results = dict(
            sample_data,
            **optical_results,
            **electrical_results)
        io.save_json_dicts(
            out_path=os.path.join(
                out_path,
                f'{sample_data["File Name"]}_Results.json'),
            dictionary=sample_results)
        plot.literature_plot_with_errors(
            drude_permittivities=electrical_results['Drude Permittivity'],
            drude_permittivities_errors=electrical_results[
                'Drude Permittivity Error'],
            frequency_range=frequency_THz,
            curve_labels=electrical_results['Carrier Density'],
            frequencies=optical_results['Resonant Frequency THz'],
            frequency_errors=optical_results['Resonant Frequency Error'],
            permittivities=optical_results['Real Permittivity'],
            permittivity_range=optical_results['Permittivity Range'],
            point_label='Optical Measurements',
            frequency_ticks=info['Frequency THz Ticks'],
            out_path=os.path.join(
                out_path,
                f'{sample_data["File Name"]}_Results.png'))

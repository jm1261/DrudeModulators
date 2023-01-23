import numpy as np
import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot

from pathlib import Path
''' Some thing about x0 infeasable '''

if __name__ == '__main__':
    ''' Organisation '''
    root = Path().absolute()
    info, directory_paths = fp.get_directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        directory_path=directory_paths['4PP Path'],
        file_string='.csv')
    parent, batches = fp.get_all_batches(file_paths=file_paths)
    drude_parameters = io.load_json(
        file_path=Path(f'{root}/Drude_parameters.json'))
    mobilities = drude_parameters['Mobilities']
    redo = {}

    ''' Loo[ Files '''
    for batch in batches:
        file_paths = batches[f'{batch}']
        out_file = Path(f'{directory_paths["Results Path"]}/{batch}_Drude.json')
        if out_file.is_file():
            pass
        else:
            batch_dictionary = fp.update_batch_dictionary(
                parent=parent,
                batch_name=batch,
                file_paths=file_paths)
            sheet_resistances = io.load_sheet_resistance(
                file_path=file_paths[0])
            sample_parameters = fp.sample_information(
                file_path=file_paths[0])
            S4_file, S4_parameters = fp.find_S4_measurement(
                    S4_path=directory_paths['S4 Path'],
                    sample_details=sample_parameters,
                    file_string='S4.json')
            batch_dictionary.update(S4_parameters)
            ''' All Works Up To Here '''
            if len(S4_file) == 0:
                pass
            else:
                ''' Possible the problem is here... '''
                S4_measurements = io.get_S4_measurements(
                    file_path=S4_file[0])
                if 'Skip' in S4_measurements.keys():
                    pass
                else:
                    redo.update({f'{batch}': S4_measurements['Gratings']})
                    conductivity = anal.average_sample_conductivity(
                        film_thicknesses=S4_measurements['Film Thickness'],
                        sheet_resistances=sheet_resistances)
                    permittivity = anal.calc_permittivities(
                        refractive_indices=S4_measurements[
                            'Refractive Index'],
                        refractive_indices_errors=S4_measurements[
                            'Refractive Index Error'],
                        extinction_coefficients=S4_measurements[
                            'Extinction Coefficient'],
                        extinction_coefficients_errors=S4_measurements[
                            'Extinction Coefficient Error'])
                    mobility = mobilities[f'{batch}']
                    drude_results = anal.optimize_drude_permittivity(
                        S4_measurements=S4_measurements,
                        conductivity=conductivity,
                        mobility=mobility,
                        drude_parameters=drude_parameters,
                        permittivity=permittivity)
                    batch_dictionary.update(drude_results)
                    frequency_range = drude_results['Frequency THz Range']
                    frequency_THz = np.arange(
                        frequency_range[0],
                        frequency_range[1],
                        frequency_range[2])
                    omega = [2 * np.pi * f * 1E12 for f in frequency_THz]
                    real_results = drude_results['Real Results']
                    real_drude_permittivity = [
                        anal.real_drude_permittivity(
                            x=w,
                            conductivity=real_results[0],
                            mobility=real_results[1],
                            effective_mass=real_results[2],
                            epsilon_infinity=real_results[3])
                        for w in omega]
                    frequency_points = [
                        w / (2 * np.pi * 1E12)
                        for w in drude_results['Angular Frequency']]
                    frequency_errors = [
                        anal.standard_quadrature(
                            calculated_parameter=f,
                            variables=[w],
                            errors=[dw])
                        for f, w, dw in zip(
                            frequency_points,
                            drude_results['Angular Frequency'],
                            drude_results['Angular Frequency Error'])]
                    plot.drude_permittivity_plot(
                        frequency_THz=frequency_THz,
                        drude_permittivity=real_drude_permittivity,
                        drude_label=f'{file_paths[0]}',
                        frequency_ticks=drude_results['Frequency THz Ticks'],
                        frequency_points=frequency_points,
                        frequency_errors=frequency_errors,
                        permittivity_points=drude_results['Real Permittivity'],
                        permittivity_errors=drude_results[
                            'Real Permittivity Error'],
                        out_path=Path(
                            f'{directory_paths["Results Path"]}'
                            f'\{batch}_RealDrude.png'))
                io.save_json_dicts(
                    out_path=out_file,
                    dictionary=batch_dictionary)
    io.save_json_dicts(
        out_path=Path(f'{root}/Redo.json'),
        dictionary=redo)

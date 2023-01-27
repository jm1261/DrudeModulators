import numpy as np
import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import src.plotting as plot

from pathlib import Path


if __name__ == '__main__':
    root = Path().absolute()
    info, directory_paths = fp.get_directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        directory_path=directory_paths['4PP Path'],
        file_string='.csv')
    parent, batches = fp.get_all_batches(file_paths=file_paths)
    drude_parameters = io.load_json(
        file_path=Path(f'{root}/Drude_parameters.json'))

    real_color = [
        'darkviolet',
        'black',
        'blue',
        'crimson']
    imag_color = [
        'peru',
        'forestgreen',
        'fuchsia',
        'olive']
    real_label = [
        '$\epsilon_r$ 0% $O_2$',
        '$\epsilon_r$ 20% $O_2$',
        '$\epsilon_r$ 27% $O_2$',
        '$\epsilon_r$ 5% $O_2$']
    imag_label = [
        '$\epsilon_i$ 0% $O_2$',
        '$\epsilon_i$ 20% $O_2$',
        '$\epsilon_i$ 27% $O_2$',
        '$\epsilon_i$ 5% $O_2$']
    for index, batch in enumerate(batches):
        file_paths = batches[f'{batch}']
        out_file = Path(f'{directory_paths["Results Path"]}/{batch}_Drude.json')
        oot_file = Path(f'{directory_paths["Results Path"]}/{batch}_Drude.json')
        if oot_file.is_file():
            pass
        else:
            batch_dictionary = fp.update_batch_dictionary(
                parent=parent,
                batch_name=batch,
                file_paths=file_paths)
            sheet_resistances = io.load_sheet_resistance(
                file_path=file_paths[0])
            S4_file, S4_parameters = fp.find_S4_measurement(
                S4_path=directory_paths['S4 Path'],
                sample_details=fp.sample_information(
                    file_path=file_paths[0]),
                file_string='S4.json')
            batch_dictionary.update(S4_parameters)

            if len(S4_file) == 0:
                pass
            else:
                S4_measurements = io.get_S4_measurements(file_path=S4_file[0])
                if 'Skip' in S4_measurements.keys():
                    pass
                else:
                    conductivity = anal.average_sample_conductivity(
                        film_thicknesses=S4_measurements['Film Thickness'],
                        sheet_resistances=sheet_resistances)
                    print(f'{batch}')
                    permittivity = anal.calc_permittivities(
                        refractive_indices=S4_measurements['Refractive Index'],
                        refractive_indices_errors=S4_measurements[
                            'Refractive Index Error'],
                        extinction_coefficients=S4_measurements[
                            'Extinction Coefficient'],
                        extinction_coefficients_errors=S4_measurements[
                            'Extinction Coefficient Error'])
                    mobility = (drude_parameters['Mobilities'])[f'{batch}']
                    carrier_density = anal.calculate_carrier_concs(
                        conductivity=conductivity,
                        mobility=mobility)

                    angular_frequencies = anal.peaks_to_angularfrequencies(
                        resonant_peaks=S4_measurements['Peak Wavelength'],
                        resonant_peaks_errors=S4_measurements[
                            'Peak Wavelength Error'])
                    real_guesses_bounds = anal.get_real_guesses_bounds(
                        carrier_density=carrier_density,
                        drude_parameters=drude_parameters)
                    drude_real = anal.optimize_real_drude(
                        angular_frequency=angular_frequencies[
                            'Angular Frequency'],
                        real_permittivity=permittivity['Real Permittivity'],
                        real_permittivity_error=permittivity[
                            'Real Permittivity Error'],
                        initial_guesses=real_guesses_bounds[
                            'Real Initial Guesses'],
                        bounds=real_guesses_bounds['Real Bounds'])

                    imag_guesses_bounds = anal.get_imag_guesses_bounds(
                        variables=drude_real['Real Results'],
                        errors=drude_real['Real Errors'],
                        drude_parameters=drude_parameters)
                    drude_imag = anal.optimize_imag_drude(
                        angular_frequency=angular_frequencies[
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
                        **angular_frequencies,
                        **real_guesses_bounds,
                        **drude_real,
                        **imag_guesses_bounds,
                        **drude_imag)
                    batch_dictionary.update(results_dictionary)

                    frequency_range = results_dictionary['Frequency THz Range']
                    frequency_THz = np.arange(
                        frequency_range[0],
                        frequency_range[1],
                        frequency_range[2])
                    omega = [2 * np.pi * f * 1E12 for f in frequency_THz]
                    real_results = results_dictionary['Real Results']
                    imag_results = results_dictionary['Imaginary Results']
                    real_drude_permittivity = [
                        anal.real_drude_permittivity(
                            x=w,
                            carrier_density=real_results[0],
                            effective_mass=real_results[1],
                            epsilon_infinity=real_results[2])
                        for w in omega]
                    imag_drude_permittivity = [
                        anal.imag_drude_permittivity(
                            x=w,
                            carrier_density=imag_results[0],
                            effective_mass=imag_results[1],
                            epsilon_infinity=imag_results[2],
                            relaxation_time=imag_results[3])
                        for w in omega]
                    frequency_points = [
                        (anal.wavelength_or_frequency(
                            wavelength_or_frequency=peak * 1E-9)) / 1E12
                        for peak in S4_measurements['Peak Wavelength']]
                    frequency_errors = [
                        anal.standard_quadrature(
                            calculated_parameter=f,
                            variables=[w],
                            errors=[dw])
                        for f, w, dw in zip(
                            frequency_points,
                            results_dictionary['Angular Frequency'],
                            results_dictionary['Angular Frequency Error'])]
                    plot.drude_permittivity_plot(
                        frequency_THz=frequency_THz,
                        drude_permittivity_real=real_drude_permittivity,
                        drude_permittivity_imag=imag_drude_permittivity,
                        real_color=real_color[index],
                        imag_color=imag_color[index],
                        real_label=real_label[index],
                        imaginary_label=imag_label[index],
                        frequency_points=frequency_points,
                        frequency_errors=frequency_errors,
                        real_permittivity_points=results_dictionary[
                            'Real Permittivity'],
                        real_permittivity_errors=results_dictionary[
                            'Real Permittivity Error'],
                        imag_permittivity_points=results_dictionary[
                            'Imaginary Permittivity'],
                        imag_permittivity_errors=results_dictionary[
                            'Imaginary Permittivity Error'],
                        frequency_ticks=drude_parameters[
                            'Frequency THz Ticks'],
                        out_path=Path(
                            f'{directory_paths["Results Path"]}'
                            f'\{batch}_Drude.png'))

            io.save_json_dicts(
                out_path=out_file,
                dictionary=batch_dictionary)

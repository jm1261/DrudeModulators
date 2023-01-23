import numpy as np
import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal

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
                    ''' What parameters do we need?
                    Conductivity - check
                    Mobility
                    Eps_real - check
                    Eps_imag - check
                    carrier concentration
                    effective mass
                    relaxation time
                    '''
                    conductivity = anal.average_sample_conductivity(
                        film_thicknesses=S4_measurements['Film Thickness'],
                        sheet_resistances=sheet_resistances)
                    permittivity = anal.calc_permittivities(
                        refractive_indices=S4_measurements['Refractive Index'],
                        refractive_indices_errors=S4_measurements[
                            'Refractive Index Error'],
                        extinction_coefficients=S4_measurements[
                            'Extinction Coefficient'],
                        extinction_coefficients_errors=S4_measurements[
                            'Extinction Coefficient Error'])
                    mobility = 
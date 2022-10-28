import os
import src.GUI as gui
import src.fileIO as io


def create_sample_dictionary():
    '''
    Create a results dictionary for Drude material electrical vs optical
    measurements. Dictionary creates an array for sheet resistance measurements
    in Ohms/Sq, resonant wavelength of grating for optical measurements in nm,
    grating effective index in RIU, and the upper and lower bounds of the
    grating effective index in RIU.
    Args:
        None
    Returns:
        sample_dictionary: <dict> sample dictionary containing required
                            parameters
    '''
    sample_dictionary = {
        'Sheet Resistance': [],
        'Film Thickness': [],
        'Epsilon Infinity': [],
        'Electron Mobility': [],
        'Resonant Wavelength': [],
        'Material Index': [],
        'Index Upper Bound': [],
        'Index Lower Bound': []}
    return sample_dictionary


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    directory_path = gui.prompt_for_path(
        default=root,
        title='Create/Select Data Directory',
        dir_path=True)

    ''' Samples '''
    info_json = io.load_json(
        file_path=os.path.join(
            root,
            'info.json'))
    samples = info_json['Sample Names']

    ''' Sample dictionary '''
    for sample in samples:
        sample_dictionary = create_sample_dictionary()
        io.save_json_dicts(
            out_path=os.path.join(
                directory_path,
                f'{sample}.json'),
            dictionary=sample_dictionary)

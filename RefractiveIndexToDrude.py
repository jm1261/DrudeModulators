import os
import numpy as np
import Functions.Organisation as org
import Functions.StandardPlots as plot
import matplotlib.pyplot as plt


def txt_in(file_path):
    '''
    Loads text file output from Filmetrics spectral reflectometer.
    Args:
        file_path: <string> path to file
    Returns:
        col0: <array> column 0, data array
        col1: <array> column 1, data array
        col2: <array> column 2, data array
    '''
    col0, col1, col2 = np.genfromtxt(
        fname=file_path,
        delimiter=',',
        skip_header=5,
        skip_footer=6,
        unpack=True)
    return col0, col1, col2


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    dirpathsconfig = org.GetConfig(
        config_path=os.path.join(
            root,
            '..',
            'Dirpaths.config'))
    rootpath = os.path.join(
        dirpathsconfig['root'],
        dirpathsconfig['filmetrics'])
    filepaths = org.OpenThePath(
        default=rootpath,
        title='Select nk Files',
        file_path=True,
        file_type=[('nk Files', '*.fitnk')])
    constants = org.GetConfig(
        config_path=os.path.join(
            root,
            'References',
            'Constants.config'))
    outpath = os.path.join(
        root,
        'References')

    ''' Params '''
    frequencyTHz = np.arange(900, 1, -1)  # THz, range from paper
    frequency = [f * 1E12 for f in frequencyTHz]
    wavelength = [constants['c'] / f for f in frequency]
    omegasq = [(2 * np.pi * f) ** 2 for f in frequency]
    ticks = [1, 100, 200, 300, 400, 500, 600, 700, 800, 900]

    for file in filepaths:
        ''' Calculate Permittivity '''
        wavs, ns, ks = txt_in(file_path=file)
        wav = [(w * 1E-9) for w in wavs]
        freq = [constants['c'] / (w * 1E-9) for w in wav]
        freqTHz = [f / 1E12 for f in freq]
        freqrange = np.arange(
            max(freqTHz),
            min(freqTHz),
            -((max(freqTHz) - min(freqTHz)) / len(frequency)))
        narray = [n for n in ns]
        karray = [k for k in ks]
        ninterp = np.interp(
            x=wavelength,
            xp=wav,
            fp=narray)
        kinterp = np.interp(
            x=wavelength,
            xp=wav,
            fp=karray)
        epsreal = [(n ** 2) - (k ** 2) for n, k in zip(ninterp, kinterp)]
        fig, ax = plt.subplots(1, figsize=[10, 7])
        ax.plot(frequencyTHz, epsreal, 'b', lw=2)
        plt.show()

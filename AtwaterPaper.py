import os
import numpy as np
import Functions.Organisation as org
import Functions.StandardPlots as plot


def PlasmaFrequency(e_density,
                    e_charge,
                    eps_0,
                    m_star):
    '''
    Calculate the square of the plasma frequency from the Drude model.
    Args:
        e_density: <float> N in the Drude equation, carrier density in m^-3
        e_charge: <float> e in the Drude equation, carrier charge in SI
        eps_0: <float> permittivity free space
        m_star: <float> molecular electron mass
    Return:
        omega_p_square: <float> plasma frequency squared
    '''
    omega_p_squared = (e_density * (e_charge ** 2)) / (eps_0 * m_star)
    return omega_p_squared


def DrudeEq(eps_inf,
            omega_p_sq,
            omega_sq):
    '''
    Drude model equation as taken from Atwater Paper.
    Args:
        eps_inf: <float> epsilon at infinite frequency
        omega_p_sq: <float> plasma frequency (squared)
        omega_sq: <float> omega squared
    Returns:
        eps_drude: <float> Drude permittivity at specified omega
    '''
    eps_drude = eps_inf - (omega_p_sq / omega_sq)
    return eps_drude


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    constants = org.GetConfig(
        config_path=os.path.join(
            root,
            'Constants.config'))

    ''' Params '''
    Ns = [1E18, 1E19, 1E20, 1E21, 5E21, 1E22]  # cm^-3, from paper
    Nm = [n * 1E6 for n in Ns]  # m^-3, from paper
    plasmafreqs = [
        PlasmaFrequency(
            e_density=N,
            e_charge=constants['e_charge'],
            eps_0=constants['eps_0'],
            m_star=(constants['e_mass'] * constants['m_star_ITO']))
        for N in Nm]
    frequencyTHz = np.arange(900, 1, -1)  # THz, range from paper
    frequency = [f * 1E12 for f in frequencyTHz]
    wavelength = [constants['c'] / f for f in frequency]
    omegasq = [(2 * np.pi * f) ** 2 for f in frequency]
    ticks = [1, 100, 200, 300, 400, 500, 600, 700, 800, 900]

    ''' Drude '''
    epsdrude = []
    for omp in plasmafreqs:
        epsdrude.append(
            [
                DrudeEq(
                    eps_inf=constants['eps_inf_ITO'],
                    omega_p_sq=omp,
                    omega_sq=w)
                for w in omegasq])

    ''' Specific Plot '''
    plot.AtwaterPlot(
        eps_drude=epsdrude,
        N_m3=Nm,
        frequency_THz=frequencyTHz,
        frequency_ticks=ticks,
        out_path=os.path.join(
            root,
            'AtwaterPaper.png'))

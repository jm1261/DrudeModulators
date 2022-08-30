import os
import numpy as np
import Functions.Organisation as org
import Functions.StandardPlots as plot


def SheetResistanceConductivity(sheet_resistance,
                                film_thickness):
    '''
    Calculate conductivity from a sheet resistance measurement.
    '''
    resistivity = sheet_resistance * film_thickness
    conductivity = 1 / resistivity
    return conductivity


def ConductivityToConcentration(sigma,
                                mu,
                                e_charge):
    '''
    Calculate carrier concentration from electron mobility and conductivity.
    Args:
        sigma: <float> electrical conductivity
        mu: <float> electron mobility
        e_charge: <float> electron charge
    Returns:
        N: <float> carrier concentration
    '''
    N = sigma / (mu * e_charge)
    return N


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
            'References',
            'Constants.config'))
    outpath = os.path.join(
        root,
        'References')

    ''' Sheet Resistances '''
    samplenames = ['AF1', 'AF2', 'AF3']
    probeoffset = 1.17  # Ohms/sq
    #measuredresistances = [481.89, 251.00, 102.47, 143.52, 168.69]  # Ohms/sq AG
    #thicknesses = [162.18, 147.13, 181.70, 168.04, 171.05]  # nm AG
    measuredresistances = [677.65, 357.38, 168.63]
    sheetresistances = [r - probeoffset for r in measuredresistances]
    thicknesses = [162.18, 147.13, 181.70]

    ''' Params '''
    mus = range(5, 51, 5)
    for mu in mus:
        sigmas = [
            SheetResistanceConductivity(
                sheet_resistance=rs,
                film_thickness=(t * 1E-9))
            for rs, t in zip(sheetresistances, thicknesses)]
        Ns = [
            ConductivityToConcentration(
                sigma=sig,
                mu=mu,
                e_charge=constants['e_charge'])
            for sig in sigmas]
        Nm = [n * 1E6 for n in Ns]  # m^-3
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
            N_m3=samplenames,
            frequency_THz=frequencyTHz,
            frequency_ticks=ticks,
            out_path=os.path.join(
                outpath,
                f'SampleAF_{mu}mu.png'))

import matplotlib.pyplot as plt

def TickFunction(X):
    '''
    Converts frequency ticks to wavelength ticks, THz to um.
    Args:
        X: <array> x ticks to convert
    Returns:
        <array> converted x ticks
    '''
    V = (3E8 / (X * 1E12)) * 1E6
    return ["%.3f" % z for z in V]


def AtwaterPlot(eps_drude,
                N_m3,
                frequency_THz,
                frequency_ticks,
                out_path):
    '''
    Recreate plot from Atwater Paper, including x ticks in frequency (THz) and
    wavelength (μm).
    Args:
        eps_drude: <array> nested array of Drude permittivities for different
                    carrier concentrations across a range of omega_sq values
        N_m3: <array> all used carrier concentrations in m^-3
        frequency_THz: <array> frequency array in THz
        frequency_ticks: <array> desired frequency tick values
        out_path: <string> path to save
    Returns:
        None
    '''
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[10, 7])
    ax2 = ax1.twiny()
    for index, eps in enumerate(eps_drude):
        ax1.plot(
            frequency_THz[::-1],
            eps,
            f'C{index}',
            lw=2,
            label=f'{N_m3[index]}')
    ax1.axhline(
        y=0,
        color='g',
        lw=2,
        linestyle='--')
    ax1.legend(
        loc=0,
        prop={'size': 14})
    ax1.set_ylim(-10, 6)
    ax2.set_xticks(frequency_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(frequency_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(TickFunction(X=ax1Ticks[::-1]))
    ax2.set_xlabel(
        'Frequency [THz]',
        fontsize=14,
        fontweight='bold')
    ax1.set_xlabel(
        'Wavelength[μm]',
        fontsize=14,
        fontweight='bold')
    ax1.set_ylabel(
        'Epsilon [au]',
        fontsize=14,
        fontweight='bold')
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator


def tick_function(X):
    '''
    Converts frequency ticks to wavelength ticks, THz to um.
    Args:
        X: <array> x ticks to convert
    Returns:
        <array> converted x ticks
    '''
    V = (3E8 / (X * 1E12)) * 1E6
    return ['%.2f' % z for z in V]


def cm_to_inches(cm):
    '''
    Convert cm to inches.
    Args:
        cm: <float> distance in cm
    Returns:
        inches: <float> distance in inches to 2dp
    '''
    return round(cm * 0.393701, 2)


def literature_plot(drude_permittivity,
                    label,
                    frequency_range,
                    frequency_ticks,
                    out_path):
    '''
    Recreate plot from Atwater Paper, including x ticks in frequency (THz) and
    wavelength (μm).
    Args:
        drude_permittivity: <array> array of Drude permittivities for different
                            across a range of omega_sq values
        label: <string> labels for plot legend
        frequency_range: <array> frequency array in THz
        frequency_ticks: <array> desired frequency tick values
        out_path: <string> path to save
    Returns:
        None
    '''
    page_width = 7.5
    figure_height = 9
    figure_width = page_width / 2
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    ax1.plot(
        frequency_range[::-1],
        drude_permittivity,
        lw=2,
        label=label)
    ax1.axhline(
        y=0,
        color='g',
        lw=2,
        linestyle='--')
    ax1.legend(
        loc=0,
        prop={'size': 10})
    ax1.set_ylim(-10, 6)
    ax2.set_xticks(frequency_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(frequency_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax2.set_xlabel(
        'Frequency [THz]',
        fontsize=15,
        fontweight='bold')
    ax1.set_xlabel(
        'Wavelength[μm]',
        fontsize=15,
        fontweight='bold')
    ax1.set_ylabel(
        'Epsilon [au]',
        fontsize=15,
        fontweight='bold')
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)


def drude_permittivity_plot(frequency_THz,
                            drude_permittivity_real,
                            drude_permittivity_imag,
                            real_color,
                            imag_color,
                            real_label,
                            imaginary_label,
                            frequency_points,
                            frequency_errors,
                            real_permittivity_points,
                            real_permittivity_errors,
                            imag_permittivity_points,
                            imag_permittivity_errors,
                            frequency_ticks,
                            legend_loc,
                            out_path):
    page_width = 15
    page_height = 9
    figure_height = page_height
    figure_width = page_width / 2
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            10,
            7],
        dpi=300)
    ax3 = ax1.twiny()
    
    ''' Plot Real Permittivity and Frequency '''
    line1 = ax1.plot(
        frequency_THz,
        drude_permittivity_real,
        color=real_color,
        lw=4,
        label=real_label)
    ax1.axhline(
        y=0,
        color='black',
        lw=4,
        linestyle='--',
        alpha=0.5)
    ax1.set_ylim(-1.9, 5.9)

    ''' Plot Imaginary Permittivity and Frequency '''
    ax2 = ax1.twinx()
    line2 = ax2.plot(
        frequency_THz,
        drude_permittivity_imag,
        color=imag_color,
        lw=4,
        label=imaginary_label)
    ax2.set_ylim(-0.19, 0.59)

    ''' Get Lines and Labels '''
    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax1.legend(
        lines,
        labels,
        frameon=True,
        loc=legend_loc,
        ncol=2,
        prop={'size': 22})

    ''' Plot Real Resonant Points with Errors '''
    ax1.errorbar(
        x=frequency_points,
        y=real_permittivity_points,
        yerr=real_permittivity_errors,
        mfc=real_color,
        ecolor=real_color,
        markeredgecolor=real_color,
        marker='o',
        linestyle='',
        ms=12)

    ''' Plot Imaginary Resonant Points with Errors '''
    ax2.errorbar(
        x=frequency_points,
        y=imag_permittivity_points,
        yerr=imag_permittivity_errors,
        mfc=imag_color,
        ecolor=imag_color,
        markeredgecolor=imag_color,
        marker='^',
        linestyle='',
        ms=12)

    ''' Set Up Wavelength Range '''
    ax3.set_xticks(frequency_ticks)
    ax3.set_xlim(90, 600)
    ax3Ticks = ax3.get_xticks()
    ax3.set_xticklabels(frequency_ticks)
    ax1Ticks = ax3Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax3.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks))

    ''' Set Axes Labels '''
    ax3.set_xlabel(
        'Frequency (THz)',
        fontsize=32,
        fontweight='bold',
        labelpad=20)
    ax1.set_xlabel(
        r'Wavelength ($\bf{\mu}$m)',
        fontsize=32,
        fontweight='bold')
    ax1.set_ylabel(
        r'$\bf{\epsilon_{r}}$ (a.u.)',
        fontsize=32,
        fontweight='bold',
        color=real_color)
    ax2.set_ylabel(
        r'$\bf{\epsilon_{i}}$ (a.u.)',
        fontsize=32,
        fontweight='bold',
        rotation=270,
        labelpad=20,
        color=imag_color)
    
    ax1.tick_params(axis='x', which='major', labelsize=28)
    ax1.tick_params(axis='y', which='major', labelsize=28)
    ax2.tick_params(axis='y', which='major', labelsize=28)
    ax3.tick_params(axis='x', which='major', labelsize=28)
    ax1.yaxis.set_major_locator(MultipleLocator(1.5))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_major_locator(MultipleLocator(0.15))
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax3.xaxis.set_minor_locator(AutoMinorLocator())

    ax2.invert_xaxis()
    ax3.invert_xaxis()

    ''' Save '''
    fig.tight_layout()
    plt.savefig(out_path)
    fig.clf()
    plt.cla()
    plt.close(fig)

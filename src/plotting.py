import matplotlib.pyplot as plt
import matplotlib.patches as patches


def tick_function(X):
    '''
    Converts frequency ticks to wavelength ticks, THz to um.
    Args:
        X: <array> x ticks to convert
    Returns:
        <array> converted x ticks
    '''
    V = (3E8 / (X * 1E12)) * 1E6
    return ["%.3f" % z for z in V]


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
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[10, 7])
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
        prop={'size': 14})
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


def uncertainty_region_plot(frequencies,
                            frequency_errors,
                            permittivities,
                            permittivity_range,
                            label,
                            frequency_ticks,
                            out_path):
    '''
    Plot optically measured permittivities as a function of resonant frequency,
    on to the same style of plot as is common in Drude/ENZ literature. Errors
    calculated using a region of uncertainty method where minimum permittivity
    and maximum permittivity given by the min/max values of refractive index of
    the resonant structure.
    Args:
        frequencies: <array> resonant frequency array for resonant structure
        frequency_errors: <array> resonant frequency errors
        permittivities: <array> calculated permittivities of the resonant
                        structures
        permittivity_range: <array/tuple> array of min/max permittivities for
                            each resonant frequency in a tuple
        label: <string> legend label for data
        frequency_ticks: <array> array of frequency space axis ticks
        out_path: <string> path to save
    Returns:
        None
    '''
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[10, 7])
    ax2 = ax1.twiny()
    ax1.plot(
        frequencies[::-1],
        permittivities,
        'g.',
        markersize=8,
        label=label)
    for index, frequency in enumerate(frequencies[::-1]):
        rectangle = patches.Rectangle(
            xy=(
                (frequency - frequency_errors[index]),
                min(permittivity_range[index])),
            width=(
                (frequency + frequency_errors[index])
                - (frequency - frequency_errors[index])),
            height=(
                max(permittivity_range[index])
                - min(permittivity_range[index])),
            linewidth=1,
            edgecolor='g',
            facecolor='g',
            alpha=0.3)
        ax1.add_patch(rectangle)
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
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
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


def literature_plot_with_errors(drude_permittivities,
                                drude_permittivities_errors,
                                frequency_range,
                                curve_labels,
                                frequencies,
                                frequency_errors,
                                permittivities,
                                permittivity_range,
                                point_label,
                                frequency_ticks,
                                out_path):
    '''
    '''
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[10, 7])
    ax2 = ax1.twiny()
    ax1.plot(
        frequency_range[::-1],
        drude_permittivities,
        'b',
        lw=2,
        label=curve_labels)
    ax1.plot(
        frequency_range[::-1],
        [
            (permittivity + error)
            for permittivity, error
            in zip(drude_permittivities, drude_permittivities_errors)],
        lw=2,
        linestyle='--',
        color='b',
        alpha=0.2,
        label='Permittivity Error')
    ax1.plot(
        frequency_range[::-1],
        [
            (permittivity - error)
            for permittivity, error
            in zip(drude_permittivities, drude_permittivities_errors)],
        lw=2,
        linestyle='--',
        color='b',
        alpha=0.2)
    ax1.plot(
        frequencies[::-1],
        permittivities,
        'g.',
        markersize=8,
        label=point_label)
    for index, frequency in enumerate(frequencies[::-1]):
        rectangle = patches.Rectangle(
            xy=(
                (frequency - frequency_errors[index]),
                min(permittivity_range[index])),
            width=(
                (frequency + frequency_errors[index])
                - (frequency - frequency_errors[index])),
            height=(
                max(permittivity_range[index])
                - min(permittivity_range[index])),
            linewidth=1,
            edgecolor='g',
            facecolor='g',
            alpha=0.3)
        ax1.add_patch(rectangle)
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
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
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

import cmath
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.ticker import MultipleLocator, AutoMinorLocator


def cm_to_inches(cm):
    '''
    Convert cm to inches.
    Args:
        cm: <float> distance in cm
    Returns:
        inches: <float> distance in inches to 2dp
    '''
    return round(cm * 0.393701, 2)


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


if __name__ == '__main__':
    root = Path().absolute()
    carrier_concs = [1E24, 1E25, 1E26, 1E27, 5E27, 1E28]
    carriers_cm3 = [n / 1E6 for n in carrier_concs]
    plasma_freq_sq = [
        (n * (1.60217662E-19 ** 2))
        / (8.854187812813E-12 * 0.35 * 9.10938356E-31)
        for n in carrier_concs]
    THz_range = np.arange(1000, 1, -1)
    frequency_range = [t * 1E12 for t in THz_range]
    wavelength_range = [3E8 / f for f in frequency_range]
    angular_frequency = [f * np.pi * 2 for f in frequency_range]
    freq_ticks = [1, 200, 400, 600, 800, 1000]
    gamma = 1.8E14
    colors = [
        'darkorange',
        'forestgreen',
        'blue',
        'darkmagenta',
        'darkgoldenrod',
        'red']

    page_width = 15
    page_height = 9
    figure_height = page_height
    figure_width = page_width / 2
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{n}$'
    label2 = r'$\bf[{cm^{-3}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freq_sq):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_real,
            lw=2,
            label=carriers_cm3[index],
            color=colors[index])
    ax1.axhline(
        y=0,
        color='k',
        lw=2,
        linestyle='--')
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-3.9, 5.9)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{r}}$ (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Carrier_Drude_Real.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{n}$'
    label2 = r'$\bf[{cm^{-3}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freq_sq):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_imag,
            lw=2,
            label=carriers_cm3[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-0.39, 0.59)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{i}}$ (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Carrier_Drude_Imag.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{n}$'
    label2 = r'$\bf[{cm^{-3}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freq_sq):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        n = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) + A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            n,
            lw=2,
            label=carriers_cm3[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 4)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('n (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Carrier_n.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{n}$'
    label2 = r'$\bf[{cm^{-3}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freq_sq):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        k = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) - A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            k,
            lw=2,
            label=carriers_cm3[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 0.5)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('k (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Carrier_k.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    carrier_conc = 1E26
    plasma_freq_sq = (
        (carrier_conc * (1.60217662E-19 ** 2))
        / (8.854187812813E-12 * 0.35 * 9.10938356E-31))
    THz_range = np.arange(1000, 1, -1)
    frequency_range = [t * 1E12 for t in THz_range]
    wavelength_range = [3E8 / f for f in frequency_range]
    angular_frequency = [f * np.pi * 2 for f in frequency_range]
    freq_ticks = [1, 200, 400, 600, 800, 1000]
    eps_infs = [0, 0.5, 1.5, 3.5, 4.5, 5.5]
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\epsilon_{\infty}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, eps in enumerate(eps_infs):
        drude_complex = [
            eps - (plasma_freq_sq / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_real,
            lw=2,
            label=eps_infs[index],
            color=colors[index])
    ax1.axhline(
        y=0,
        color='k',
        lw=2,
        linestyle='--')
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-3.9, 5.9)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{r}}$ (a.u.)',fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Eps_Drude_Real.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\epsilon_{\infty}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, eps in enumerate(eps_infs):
        drude_complex = [
            eps - (plasma_freq_sq / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_imag,
            lw=2,
            label=eps_infs[index],
            color=colors[index])
    ax1.axhline(
        y=0,
        color='k',
        lw=2,
        linestyle='--')
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-0.39, 0.59)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{i}}$ (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Eps_Drude_Imag.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\epsilon_{\infty}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, eps in enumerate(eps_infs):
        drude_complex = [
            eps - (plasma_freq_sq / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        n = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) + A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            n,
            lw=2,
            label=eps_infs[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 4)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('n (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Eps_n.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\epsilon_{\infty}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, eps in enumerate(eps_infs):
        drude_complex = [
            eps - (plasma_freq_sq / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        k = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) - A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            k,
            lw=2,
            label=eps_infs[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 0.5)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('k (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Eps_k.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)


    carrier_conc = 1E26
    plasma_freq_sq = (
        (carrier_conc * (1.60217662E-19 ** 2))
        / (8.854187812813E-12 * 0.35 * 9.10938356E-31))
    THz_range = np.arange(1000, 1, -1)
    frequency_range = [t * 1E12 for t in THz_range]
    wavelength_range = [3E8 / f for f in frequency_range]
    angular_frequency = [f * np.pi * 2 for f in frequency_range]
    freq_ticks = [1, 200, 400, 600, 800, 1000]
    gammas = [0.5, 1, 1.5, 2, 2.5, 3]
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\Gamma}$'
    label2 = r'$\bf[{x10^{14}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, g in enumerate(gammas):
        drude_complex = [
            3.9 - (plasma_freq_sq / complex(x**2, (x * g * 1E14)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_real,
            lw=2,
            label=gammas[index],
            color=colors[index])
    ax1.axhline(
        y=0,
        color='k',
        lw=2,
        linestyle='--')
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-3.9, 5.9)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{r}}$ (a.u.)',
                fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Gamma_Drude_Real.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\Gamma}$'
    label2 = r'$\bf[{x10^{14}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, g in enumerate(gammas):
        drude_complex = [
            3.9 - (plasma_freq_sq / complex(x**2, (x * g * 1E14)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_imag,
            lw=2,
            label=gammas[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-0.39, 0.59)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{i}}$ (a.u.)',
                   fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Gamma_Drude_Imag.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\Gamma}$'
    label2 = r'$\bf[{x10^{14}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, g in enumerate(gammas):
        drude_complex = [
            3.9 - (plasma_freq_sq / complex(x**2, (x * g * 1E14)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        n = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) + A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            n,
            lw=2,
            label=gammas[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 4)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('n (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Gamma_n.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{\Gamma}$'
    label2 = r'$\bf[{x10^{14}}]$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=label2)
    ax1.plot([], [], ' ', label=' ')
    for index, g in enumerate(gammas):
        drude_complex = [
            3.9 - (plasma_freq_sq / complex(x**2, (x * g * 1E14)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        k = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) - A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            k,
            lw=2,
            label=gammas[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 0.5)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('k (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('Gamma_k.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    ems = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    carrier_conc = 1E26
    plasma_freqs = [
        (carrier_conc * (1.60217662E-19 ** 2))
        / (8.854187812813E-12 * e * 9.10938356E-31)
        for e in ems]
    THz_range = np.arange(1000, 1, -1)
    frequency_range = [t * 1E12 for t in THz_range]
    wavelength_range = [3E8 / f for f in frequency_range]
    angular_frequency = [f * np.pi * 2 for f in frequency_range]
    freq_ticks = [1, 200, 400, 600, 800, 1000]
    gamma = 1.8E14
    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{m^{*}_{e}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freqs):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_real,
            lw=2,
            label=ems[index],
            color=colors[index])
    ax1.axhline(
        y=0,
        color='k',
        lw=2,
        linestyle='--')
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-3.9, 5.9)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{r}}$ (a.u.)',
                   fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('em_Drude_Real.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{m^{*}_{e}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freqs):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        ax1.plot(
            THz_range[::-1],
            drude_imag,
            lw=2,
            label=ems[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(-0.39, 0.59)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel(r'$\bf{\epsilon_{i}}$ (a.u.)',
                   fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('em_Drude_Imag.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{m^{*}_{e}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freqs):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        n = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) + A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            n,
            lw=2,
            label=ems[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 4)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('n (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('em_n.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

    fig, ax1 = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[
            cm_to_inches(cm=figure_width),
            cm_to_inches(cm=figure_height)],
        dpi=600)
    ax2 = ax1.twiny()
    label = r'$\bf{m^{*}_{e}}$'
    ax1.plot([], [], ' ', label=label)
    ax1.plot([], [], ' ', label=' ')
    ax1.plot([], [], ' ', label=' ')
    for index, omp in enumerate(plasma_freqs):
        drude_complex = [
            3.9 - (omp / complex(x**2, (x * gamma)))
            for x in angular_frequency]
        drude_imag = [x.imag for x in drude_complex]
        drude_real = [x.real for x in drude_complex]
        k = [
            np.sqrt((np.sqrt((A ** 2) + (B ** 2))) - A) / 2
            for A, B in zip(drude_real, drude_imag)]
        ax1.plot(
            THz_range[::-1],
            k,
            lw=2,
            label=ems[index],
            color=colors[index])
    ax1.legend(
        frameon=True,
        loc=0,
        ncol=3,
        prop={'size': 8})
    ax2.set_xticks(freq_ticks)
    ax2Ticks = ax2.get_xticks()
    ax2.set_xticklabels(freq_ticks[::-1])
    ax1Ticks = ax2Ticks
    ax1.set_xticks(ax1Ticks)
    ax1.set_xbound(ax2.get_xbound())
    ax1.set_xticklabels(tick_function(X=ax1Ticks[::-1]))
    ax1.set_ylim(0, 0.5)
    ax1.set_xlabel('Wavelength [μm]', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Frequency [THz]', fontsize=15, fontweight='bold')
    ax1.set_ylabel('k (a.u.)', fontsize=15, fontweight='bold')
    ax1.tick_params(axis='x', which='major', labelsize=10)
    ax1.tick_params(axis='y', which='major', labelsize=10)
    ax2.tick_params(axis='x', which='major', labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(0.1))
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    plt.savefig('em_k.png', bbox_inches='tight')
    fig.clf()
    plt.cla()
    plt.close(fig)

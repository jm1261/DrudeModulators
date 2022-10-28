import numpy as np
import scipy.optimize as opt
import math
import matplotlib.pyplot as plt

frequency_THz = np.arange(900, 1, -1)
frequency = [f * 1E12 for f in frequency_THz]
omega = [2 * np.pi * f for f in frequency]
e = 1.6E-19
eps_0 = 8.854E-12
e_ITO = 0.35 * 9.11E-31

def carrier(mu, conductivity, echarge):
    return conductivity / (mu * echarge)

def plasma(carrier, echarge, eps, emass):
    return math.sqrt((carrier * (echarge ** 2)) / (eps * emass))

def drude(epsinf, plasma, angular):
    return epsinf - ((plasma ** 2) / (angular ** 2))

def function(x, conductivity, epsinf, mu):
    carrier = conductivity / (mu * 1E-4 * 1.6E-19)
    plasmasq = (carrier * (1.6E-19 ** 2)) / (8.85E-12 * 0.35 * 9.11E-31)
    drude = epsinf - (plasmasq / (x ** 2))
    return drude

xs = np.array([
    549.8357750715281,
    515.7009925515628,
    489.05784339314846,
    468.425715625,
    437.94731936775065])
xdata = [x * 1E12 * 2 * np.pi for x in xs]
ydata = np.array([
    4.0804,
    3.9601,
    3.798601,
    3.7636,
    3.6481])
yerrors = np.array([
    (4.41, 3.8024999999999998),
    (4.41, 3.8415999999999997),
    (4.040099999999999, 3.61),
    (4.1616, 3.6864),
    (3.8809, 3.4225000000000003)])
sigma = []
for y, yerror in zip(ydata, yerrors):
    delta_y = [np.abs(y - ye) for ye in yerror]
    sigma.append(max(delta_y))

mus = []
conductivities = []
epses = []
carriers = []
for conductivity in range(58500, 60500, 1):
    initial_guess = np.array([conductivity, 4.5, 4.5])
    popt, pcov = opt.curve_fit(function, xdata, ydata, initial_guess, sigma, bounds=((conductivity-500, 2.5, 1), (conductivity+500, 10, 50)))
    errors = np.sqrt(np.diag(pcov))
    mobility = popt[2]
    conductivity = popt[0]
    carrier = conductivity / (mobility * 1E-4 * 1.6E-19)
    mus.append(mobility)
    conductivities.append(conductivity)
    epses.append(popt[1])
    carriers.append(carrier)
print(np.sum(mus) / len(mus))
print(np.std(mus) / np.sqrt(len(mus) - 1))
print('')
print(np.sum(conductivities) / len(conductivities))
print(np.std(conductivities) / np.sqrt(len(conductivities) - 1))
print('')
print(np.sum(epses) / len(epses))
print(np.std(epses) / np.sqrt(len(epses) - 1))
print('')
print(np.sum(carriers) / len(carriers))
print(np.std(carriers) / np.sqrt(len(carriers) - 1))
print('')
print(len(carriers))

drude = [
    function(
        x=w,
        conductivity=np.sum(conductivities) / len(conductivities),
        epsinf=np.sum(epses) / len(epses),
        mu=np.sum(mus) / len(mus))
    for w in omega]
plt.plot(frequency_THz[::-1], drude)
plt.ylim(-10, 6)
plt.show()

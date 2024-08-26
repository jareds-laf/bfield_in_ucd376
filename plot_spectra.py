import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import glob

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
    return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def plot_spectra(csv_paths):

    """Calibration!
    """
    raw_data_sets = []
    for csv in csv_paths:
        raw_data_sets.append(pd.read_csv(csv, names=['Frequency', 'Voltage']))


    calibration_path = normalize_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc90r_calibration_teslas.csv'))
    calibration_data = pd.read_csv(calibration_path)

    # Interpolation
    x_new = np.linspace(calibration_data['freq'].min(), calibration_data['freq'].max(), 2**10)
    y_new = np.interp(x_new, calibration_data['freq'], calibration_data['B/Vo'])


    def get_interpolated_values(frequencies):
        # Interpolation
        interpolated_values = []
        for freq_set in frequencies:
            nearest_x_new = find_nearest(x_new, freq_set)
            nearest_y_new = y_new[np.where(x_new == nearest_x_new)[0][0]]
            interpolated_values.append(nearest_y_new)
        return interpolated_values
    
    frequencies_khz = []
    for data_set in raw_data_sets:
        # Make sure frequencies is in kHz!
        frequencies_khz.append(data_set['Frequency'] / 1000)

    for data_set in frequencies_khz:
        interpolated_values = get_interpolated_values(data_set)

    print(f'len interpolated values: {len(interpolated_values)}\nlen raw data: {len(raw_data_sets)}')


    b_fields = []
    for i, data_set in enumerate(interpolated_values):
        b_fields.append(raw_data_sets[i]['Voltage']*np.sqrt(2)*data_set / np.sqrt(1560/400))


    custom_params = {
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.spines.right": True,
    "axes.spines.top": True,
    "grid.linestyle": '--',
    "grid.alpha": 0.5,
    "grid.linewidth": 0.7,
    "grid.color": 'black',
    "axes.edgecolor": 'black',
    "axes.linewidth": 0.75,
    # "font.family": 'Times New Roman',
    "font.size": 16.0
    }

    plt.rcParams.update(custom_params)

    # Plot data
    fig, ax = plt.subplots()

    for i, data_set in enumerate(raw_data_sets):
        ax.plot(data_set['Frequency'], b_fields[i], linestyle='-', label=r'B{i}' + r'$_{AC}$')

    ax.set_title('Room 376B AC Magnetic Field Spectra')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel(r'$B (T/\sqrt{Hz})$')    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='major')
    ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    csv_paths = glob.glob(normalize_path(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\spectrum_*'))

    plot_spectra(csv_paths)
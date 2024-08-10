import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
    return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def plot_sr770(csv_path_in):
    # Read in the spectrum analyzer data
    if csv_path_in:
        print(f'Reading data from {csv_path_in}')       
    else:
        csv_path_in = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        print(f'Reading data from {csv_path_in}')

    # Work around to allow the DataFrame to be accessed globally
    global csv_path

    csv_path = csv_path_in
    sr770_data_1 = pd.read_csv(csv_path, index_col=False, names=['Frequency', 'Voltage'])
    print(sr770_data_1.head())

    sr770_data_2 = pd.read_csv(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\SR770\sr770_ting', index_col=False, names=['Frequency', 'Voltage'])

    fig, ax = plt.subplots()

    ax.plot(sr770_data_1['Frequency'], sr770_data_1['Voltage'], linestyle='-', label='No T\'ing')
    ax.plot(sr770_data_2['Frequency'], sr770_data_2['Voltage'], linestyle='-', label='With T\'ing')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Voltage (V)')
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.legend()
    plt.show()

if __name__ == '__main__':
    plot_sr770(csv_path_in=r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\SR770\sr770_direct')
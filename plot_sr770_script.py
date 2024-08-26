import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
    return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


# Read in the spectrum analyzer data
# csv_path_in1 = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\SR770\240812-1'
# csv_path_in2 = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\SR770\sr770_direct'
# csv_path_in3 = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\SR770\sr770_direct'
csv_path_in_ac = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\AA2'
csv_path_in_ac2 = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\AB2'


# if csv_path_in1:
#     print(f'Reading data from {csv_path_in1}')       
# else:
#     csv_path_in = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
#     print(f'Reading data from {csv_path_in1}')

# Work around to allow the DataFrame to be accessed globally
# csv_path1 = csv_path_in1
# csv_path2 = csv_path_in2
# csv_path3 = csv_path_in3
csv_path_ac = csv_path_in_ac
# sr770_data_1 = pd.read_csv(csv_path1, index_col=False, names=['Frequency', 'Voltage'])
# sr770_data_2 = pd.read_csv(csv_path2, index_col=False, names=['Frequency', 'Voltage'])
# sr770_data_3 = pd.read_csv(csv_path3, index_col=False, names=['Frequency', 'Voltage'])
sr770_data_ac = pd.read_csv(csv_path_ac, index_col=False, names=['Frequency', 'Voltage'])
sr770_data_ac2 = pd.read_csv(csv_path_in_ac2, index_col=False, names=['Frequency', 'Voltage'])
print(sr770_data_ac.head())


# Read in MC90R calibration data
calibration_path = normalize_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc90r_calibration_teslas.csv'))
calibration_data = pd.read_csv(calibration_path)

# Interpolation
x = calibration_data['freq']
y = calibration_data['B/Vo']
x_new = np.linspace(x.min(), x.max(), 2**10)
y_new = np.interp(x_new, x, y)

def get_interpolated_values(frequencies):
    # Interpolation
    interpolated_values = []
    for freq in frequencies:
        nearest_x_new = find_nearest(x_new, freq)
        nearest_y_new = y_new[np.where(x_new == nearest_x_new)[0][0]]
        interpolated_values.append(nearest_y_new)
    return interpolated_values

# Make sure frequencies is in kHz!
frequencies_khz = sr770_data_ac['Frequency'] / 1000
frequencies_khz2 = sr770_data_ac2['Frequency'] / 1000

interpolated_values = get_interpolated_values(frequencies_khz)
interpolated_values2 = get_interpolated_values(frequencies_khz2)


# Calculate the magnetic field
# Multiply by sqrt(2) to convert from RMS to peak
# Multiply by interpolated_values to convert from V to T
# 1560 is the span, 1560/400 is the resolution (400 frequency bins)
# Divide by sqrt(1560/400) to convert from T to T/sqrt(Hz)
b_field = sr770_data_ac['Voltage']*np.sqrt(2)*interpolated_values / np.sqrt(1560/400)
b_field2 = sr770_data_ac2['Voltage']*np.sqrt(2)*interpolated_values2 / np.sqrt(1560/400)


# Apply custom parameters
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

ax.plot(sr770_data_ac['Frequency'], b_field, color='purple', linestyle='-', label='$B_{AC,motor}$')
ax.plot(sr770_data_ac2['Frequency'], b_field2, linestyle='-', label='$B_{AC,background}$')
ax.set_title('Room 376B AC Magnetic Field Spectra')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel(r'$B (T/\sqrt{Hz})$')    
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True, which='major')
ax.legend()

# ax.plot(sr770_data_1['Frequency'], sr770_data_1['Voltage'], linestyle='-', label=r'$B_{DC,x}$')
# ax.plot(sr770_data_2['Frequency'], sr770_data_2['Voltage'], linestyle='-', label='$B_{DC,y}$')
# ax.plot(sr770_data_3['Frequency'], sr770_data_3['Voltage'], linestyle='-', label='B_{DC,z}')

# color1 = 'tab:blue'
# ax1.tick_params(axis='y', labelcolor=color1)

# ax1.plot(sr770_data_ac['Frequency'], sr770_data_ac['Voltage'], linestyle='-', label='$V_{AC}$')
# ax1.set_title('Background AC Magnetic Field Spectrum in 376')
# ax1.set_xlabel('Frequency (Hz)')
# ax1.set_ylabel('Voltage (V)')    
# ax1.set_xscale('log')
# ax1.set_yscale('log')
# ax1.grid(True, which='minor', axis='x')

# ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis
# color2 = 'tab:red'
# ax2.tick_params(axis='y', labelcolor=color2)

# ax2.plot(frequencies_khz*1000, sr770_data_ac['Voltage']*interpolated_values*np.sqrt(2), color=color2, linestyle='-', label='$B_{AC}$')
# ax2.set_ylabel('B (T)')    
# ax2.set_yscale('log')
# ax2.grid(True, which='major')

plt.tight_layout()
plt.show()
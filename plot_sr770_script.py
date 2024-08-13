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
csv_path_in_ac = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\SR770\240812-1'


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
        print(nearest_x_new, nearest_y_new)
        interpolated_values.append(nearest_y_new)
    return interpolated_values

# Make sure frequencies is in kHz!
frequencies_khz = [0.060, 0.120, 0.180, 0.240, 0.300, 0.360, 0.420, 0.480, 0.540, 0.600]
interpolated_values = get_interpolated_values(frequencies_khz)
frequencies_hz = [freq * 10**3 for freq in frequencies_khz]

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
    "axes.linewidth": 0.75
}

plt.rcParams.update(custom_params)

# Plot data
fig, ax = plt.subplots()

# ax.plot(sr770_data_1['Frequency'], sr770_data_1['Voltage'], linestyle='-', label=r'$B_{DC,x}$')
# ax.plot(sr770_data_2['Frequency'], sr770_data_2['Voltage'], linestyle='-', label='$B_{DC,y}$')
# ax.plot(sr770_data_3['Frequency'], sr770_data_3['Voltage'], linestyle='-', label='B_{DC,z}')
ax.plot(sr770_data_ac['Frequency'], sr770_data_ac['Voltage'], linestyle='-', label='$V_{AC}$')
ax.plot(frequencies_hz, interpolated_values, marker='^', linestyle='-', label='$B_{AC}$')

ax.grid(True, which='both')


ax.set_title('Background AC Magnetic Field Spectrum in 376 (Non-Shielded)')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Voltage (V)')    
ax.set_xscale('log')
ax.set_yscale('log')

ax.legend()
plt.show()
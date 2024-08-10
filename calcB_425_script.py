import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog

'''This script reads the oscilloscope data originally measured by the DRV425EVM
and converts the voltage measurements to magnetic field measurements. For
brevity, I refer to the DRV425EVM as simply "425."
'''

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

'''Evaluate the oscilloscope data from the DRV425EVM to convert voltages
to magnetic fields. Note that this program assumes the usage of a
Tektronix MSO24 oscilloscope with firmware version 2.2.6.1052, exporting
data with "ALL" selected as the source.
'''

# Read the CSV file into a Pandas DataFrame

# Work around to allow the DataFrame to be accessed globally
global csv_path
csv_path_1 = 'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MS024\003\MSO24_direct.csv'
csv_path_2 = 'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MS024\003\MSO24_ting.csv'


global scope_data
scope_data1 = pd.read_csv(csv_path_1, skiprows=10)
scope_data2 = pd.read_csv(csv_path_2, skiprows=10)


# Rename the columns to be more descriptive
# scope_data.rename(columns={'TIME': 't', 'CH1': 'V1', 'CH2': 'V2', 'CH3': 'V3'}, inplace=True)
scope_data1.rename(columns={'TIME': 't', 'CH1': 'V1'}, inplace=True)

# scope_data.drop(columns=['CH4'], inplace=True)

"""Note that the exported waveform from the MSO24 does not include vertical
offset information. If your oscilloscope does, you should subtract it
from the voltage output column here. Here is an example of how to do it
with the Tektronix TDS2022B:
"""

# Subtract vertical offset
# vertical_offset = pd.to_numeric(scope_data[1][9])
# scope_data.insert(6, column='V_out - Offset (V)', \
#                   value=scope_data['V_out (V)'] - vertical_offset)

"""Populate DataFrame with the final B field based on formula 1 from
the DRV425EVM datasheet: B = (V_out) / (R_shunt * G * Gfg)
Note that this assumes the reference voltage was subtracted from the
output voltage.
"""
scope_data.insert(2, column='B1', value = scope_data['V1'] / (R_shunt * G * Gfg))
# scope_data.insert(4, column='B2', value = scope_data['V2'] / (R_shunt * G * Gfg))
# scope_data.insert(6, column='B3', value = scope_data['V3'] / (R_shunt * G * Gfg))

"""Populate DataFrame with 425 values
For the most part, G and Gfg should not change
"""
# scope_data.insert(7, column='R_shunt', value = None)
# scope_data.at[0, 'R_shunt'] = R_shunt
# scope_data.insert(8, column='G', value = None)
# scope_data.at[0, 'G'] = G
# scope_data.insert(9, column='Gfg', value = None)
# scope_data.at[0, 'Gfg'] = Gfg
# print(scope_data.head())

"""Save the modified DataFrame to a new CSV file
Final units are:
    t: Seconds
    V1, V2, V3: Volts
    B1, B2, B3: Teslas
    R_shunt: Ohms
    G: V/V
    Gfg: mA/mT
"""
output_file_path = normalize_path(f'{os.path.dirname(csv_path)}/b_field_{os.path.basename(csv_path)}')
# scope_data.to_csv(output_file_path, index=False, header=True)
print(f'Data saved to {output_file_path}')

def plot_425():
# Plot the B (T) vs. Time (s) oscilloscope data

# Apply custom parameters
custom_params = {
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.spines.right": True,
    "axes.spines.top": True,
    "grid.linestyle": '-',
    "grid.alpha": 0.5,
    "grid.linewidth": 0.5,
    "grid.color": 'black',
    "axes.edgecolor": 'black',
    "axes.linewidth": 0.75
}


scope_data2= pd.read_csv(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Scope Data\MS024\003\MSO24_ting.csv', skiprows=10)
# scope_data2.rename(columns={'TIME': 't', 'CH1': 'V1', 'CH2': 'V2', 'CH3': 'V3'}, inplace=True)
scope_data2.rename(columns={'TIME': 't', 'CH1': 'V1'}, inplace=True)
R_shunt=100
G=4
Gfg=12.2
scope_data2.insert(2, column='B1', value = scope_data['V1'] / (R_shunt * G * Gfg))
# scope_data2.drop(columns=['CH4'], inplace=True)
print(scope_data2.head())
plt.rcParams.update(custom_params)

"""Plot data
I'm assuming here that channel 1 is the x-axis, channel 2 is the y-axis,
and channel 3 is the z-axis
"""
fig, ax = plt.subplots()
ax.plot(scope_data['t'], scope_data['V1'], label='Without T\'ing')
ax.plot(scope_data2['t'], scope_data2['V1'], alpha=0.75, label='With T\'ing')

# ax.plot(scope_data['t'], scope_data['B2'], color='green', label='y')
# ax.plot(scope_data['t'], scope_data['B3'], color='blue', label='z')

ax.set_title('Magnetic Field vs. Time in Room 376')
ax.set_xlabel('Time (s)')
ax.set_ylabel('B (T)')
# ax.set_ylim(-3*10**-6, 3*10**-6)
ax.grid(True)
ax.legend()
plt.show()

output_file_path = normalize_path(f'{os.path.dirname(csv_path)}/plot_b_{os.path.basename(csv_path)[:-4]}.png')
# fig.savefig(output_file_path, format='png')#, dpi=300, bbox_inches='tight')
print(f'Plot saved to {output_file_path}')
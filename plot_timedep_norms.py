import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import glob
from tkinter import filedialog

# time_averaged tells the script whether or not you want to plot the
# time-dependent data or the time-averaged data
time_averaged = False

# norms_present tells the script whether the data has norms already calculated
# by the scope (2), if the data has norms manually calculated (1), or if the
# data has no norms (0)
norms_present = 1

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
    return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


# Read in the data

if norms_present == 2:
    #TODO: Add the correct path to aug23
    files = glob.glob(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\aug23\norms_Tek001_*_ALL.csv')
elif norms_present == 1:
    files = glob.glob(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\008\norms_Tek001_*_ALL.csv')
elif norms_present == 0:
    files = glob.glob(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\007\Tek001_*_ALL.csv')
else:
    print('Invalid norms_present value. Please enter 0, 1, or 2.')


data = []    
for i in files:
    if i:
        print(i)
    data.append(pd.read_csv(i))

    # names=['TIME', 'CH1', 'CH2', 'CH3', 'CH4', 'Norm (V)', 'Norm (B)']

# print(data[0])

# print(data[0]['Norm (B)'].head())



# norms_present tells the script whether the data has norms already calculated
# by the scope (2), if the data has norms manually calculated (1), or if the
# data has no norms (0)
if norms_present == 2:
    data[0]['Norm (B)'] = data[0]['Norm (B)'] * 1e-6
    pass
elif norms_present == 1:
    pass
elif norms_present == 0:
    pass



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
    "font.size": 12.0
}

plt.rcParams.update(custom_params)

# Plot data
fig, ax = plt.subplots()

bar_colors = ['#062bb4', '#2822d4', '#822ee8', '#d96ae0', '#ee94a7', '#fcc2cf']

if time_averaged:
    avgs = []
    for i in data:
        avgs.append(np.mean(i['Norm (B)'] / 1e-6))
    
    bar_labels = ['Breaker on', 'Breaker off']
    # bar_labels = ['Motor', 'Background', 'Paint A', 'Paint B', 'Paint C', 'No Paint']
    # ax.axhline(y=np.mean(data[1]['Norm (B)']), color='red', linestyle='--', label='Background')

    ax.bar(bar_labels, avgs, color=bar_colors[0:len(bar_labels)])
    plt.xticks(rotation=45)

    # ax.plot(data[1]['TIME'], data[1]['Norm (B)'] / 1e-6, color='red',  alpha=0.5, linestyle='-', label='Background')
    # ax.plot(data[2]['TIME'], data[2]['Norm (B)'] / 1e-6, color=bar_colors[1], alpha=0.5, linestyle='-', label='Paint A')
    # ax.plot(data[3]['TIME'], data[3]['Norm (B)'] / 1e-6, color=bar_colors[2], linestyle='-', label='Paint B')
    # ax.plot(data[4]['TIME'], data[4]['Norm (B)'] / 1e-6, color=bar_colors[3], alpha=0.5, linestyle='-', label='Paint C')
    # ax.plot(data[5]['TIME'], data[5]['Norm (B)'] / 1e-6, color=bar_colors[4], alpha=0.5, linestyle='-', label='No Paint')
    ax.set_title('Room 376B Time-Averaged Background DC Magnetic Field Norms\n')
    ax.set_ylabel(r'Time-Averaged Norm($\vec{B}$) ($\mu$T)')   

else:
    ax.plot(data[0]['TIME'], data[0]['Norm (B)'] / 1e-6, color=bar_colors[0], alpha=0.5, linestyle='-', label='Breaker on')
    ax.plot(data[1]['TIME'], data[1]['Norm (B)'] / 1e-6, color='red',  alpha=0.5, linestyle='-', label='Breaker off')
    ax.set_title('Room 376B Background DC Magnetic Field Norms\n')
    ax.set_ylabel(r'Norm($\vec{B}$) ($\mu$T)')    
    ax.set_xlabel('Time (s)')
    ax.legend()

fig.set_size_inches(6, 4)
ax.grid(True, which='major')

plt.tight_layout()
plt.show()
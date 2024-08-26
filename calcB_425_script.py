import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import glob

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

def calcB_425(csv_path_in):
	# Read the CSV file into a Pandas DataFrame
    global scope_data
    scope_data = pd.read_csv(csv_path_in, skiprows=13)
    # scope_data2 = pd.read_csv(csv_path_2, skiprows=10)
    # scope_data3 = pd.read_csv(csv_path_3, skiprows=10)


    # Rename the columns to be more descriptive
    scope_data.rename(columns={'TIME': 't', 'CH1': 'V1', 'CH2': 'V2', 'CH3': 'V3', 'CH4':'V4'}, inplace=True)

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
    R_shunt = 1000
    G = 4
    Gfg = 12.2

    scope_data.insert(2, column='B1', value = scope_data['V1'] / (R_shunt * G * Gfg))
    scope_data.insert(4, column='B2', value = scope_data['V2'] / (R_shunt * G * Gfg))
    scope_data.insert(6, column='B3', value = scope_data['V3'] / (R_shunt * G * Gfg))

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


    # """Save the modified DataFrame to a new CSV file
    # Final units are:
    #     t: Seconds
    #     V1, V2, V3: Volts
    #     B1, B2, B3: Teslas
    #     R_shunt: Ohms
    #     G: V/V
    #     Gfg: mA/mT
    # """


    # Calculate mean in each dimension and find the norm of the whole field
    B1_mean = np.mean(scope_data['B1'])
    B2_mean = np.mean(scope_data['B2'])
    B3_mean = np.mean(scope_data['B3'])

    norm = np.sqrt(B1_mean**2 + B2_mean**2 + B3_mean**2)
    sig_B1_squared = (np.std(scope_data['B1'])/np.sqrt(len(scope_data['B1'])))**2
    sig_B2_squared = (np.std(scope_data['B2'])/np.sqrt(len(scope_data['B2'])))**2
    sig_B3_squared = (np.std(scope_data['B3'])/np.sqrt(len(scope_data['B3'])))**2    
    
    dNorm_dB1_squared = (B1_mean/norm)**2
    dNorm_dB2_squared = (B2_mean/norm)**2
    dNorm_dB3_squared = (B3_mean/norm)**2

    uncer_norm = np.sqrt( dNorm_dB1_squared*sig_B1_squared + dNorm_dB2_squared*sig_B2_squared + dNorm_dB3_squared*sig_B3_squared )


    # np.sqrt( np.std(scope_data['B1'])/np.sqrt(len(scope_data['B1'])) + np.std(scope_data['B2'])/np.sqrt(len(scope_data['B2'])) + np.std(scope_data['B3'])/np.sqrt(len(scope_data['B3'])) )
    print(f'Norm: {norm}, error: {uncer_norm}')

    output_file_path = normalize_path(f'{os.path.dirname(csv_path_in)}/dc_norm_{os.path.basename(csv_path_in)}')
    # scope_data.to_csv(output_file_path, index=False, header=True)

    print(f'Data saved to {output_file_path}')


    """Plot data
    I'm assuming here that channel 1 is the x-axis, channel 2 is the y-axis,
    channel 3 is the z-axis (x, y, and z for the DC fields), and channel 4 is the
    AC field.
    """
    # Apply custom parameters
    # custom_params = {
    #     "axes.spines.left": True,
    #     "axes.spines.bottom": True,
    #     "axes.spines.right": True,
    #     "axes.spines.top": True,
    #     "grid.linestyle": '--',
    #     "grid.alpha": 0.5,
    #     "grid.linewidth": 0.7,
    #     "grid.color": 'black',
    #     "axes.edgecolor": 'black',
    #     "axes.linewidth": 0.75
    # }

    # plt.rcParams.update(custom_params)

    # B1_mean = np.mean(scope_data['B1'])
    # B2_mean = np.mean(scope_data['B2'])
    # B3_mean = np.mean(scope_data['B3'])

    # norm = np.sqrt(B1_mean**2 + B2_mean**2 + B3_mean**2)

    # fig, ax = plt.subplots()

    # ax.axhline(y=B1_mean, color='orange', linestyle='--', label=r'$\langle B_{DC,x} \rangle$')
    # ax.axhline(y=B2_mean, color='blue', linestyle='--', label=r'$\langle B_{DC,y} \rangle$')
    # ax.axhline(y=B3_mean, color='red', linestyle='--', label=r'$\langle B_{DC,z} \rangle$')
    # ax.axhline(y=norm, color='black', linestyle='--', label=r'$\langle B_{DC} \rangle$')

    # Plot DC field data
    # ax.plot(scope_data['t'], scope_data['B1'], label=r'$B_{DC,x}$', color='orange')
    # ax.plot(scope_data['t'], scope_data['B2'], label=r'$B_{DC,y}$', color='blue')
    # ax.plot(scope_data['t'], scope_data['B3'], label=r'$B_{DC,z}$', color='red')

    # ax.plot(scope_data1['t'], scope_data1['V1'], label=r'$V_{DC,x}$', color='orange')
    # ax.plot(scope_data1['t'], scope_data1['V2'], label=r'$V_{DC,y}$', color='blue')
    # ax.plot(scope_data1['t'], scope_data1['V3'], label=r'$V_{DC,z}$', color='red')

    # Plot AC field data
    # ax.plot(scope_data1['t'], scope_data1['V4'], label=r'$V_{AC}$', color='green')

    # Plot MC90R calibration data
    # ax.plot(calibration_data['freq'], calibration_data['B/Vo'], marker='^', linestyle='None', label='Calibration Data')
    # Plot intepolated MC90R calibration data
    # ax.plot(x_new, y_new, marker='.', label='Interpolated', linestyle='-')
    # ax.plot(frequencies, interpolated_values, marker='^', linestyle='None', label='Interpolated')

    # ax.plot(scope_data2['t'], scope_data2['V1'], alpha=0.75, label='With T\'ing')

    # ax.plot(scope_data['t'], scope_data['B2'], color='green', label='y')
    # ax.plot(scope_data['t'], scope_data['B3'], color='blue', label='z')

    # ax.set_title('Background DC Magnetic Field Magnitudes in Room 376 (Non-Shielded)')
    # ax.set_xlabel('Time (s)')
    # ax.set_ylabel('B (T)')
    # ax.grid(True, which='both')
    # ax.legend()
    # plt.show()


    # output_file_path = normalize_path(f'{os.path.dirname(csv_path_in)}/plot_b_{os.path.basename(csv_path_in)[:-4]}.png')
    # fig.savefig(output_file_path, format='png')#, dpi=300, bbox_inches='tight')
    # print(f'Plot saved to {output_file_path}')

if __name__=='__main__':
    # Calculate norms of all the data:
    # data = glob.glob(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\Tek000_*_ALL.csv')
    # print(f'{len(data)}\n{data}')


    # for file in data:
    #     csv_path = file
        # print(csv_path)
        # calcB_425(csv_path)

    # calcB_425(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\Tek000_AA1_ALL.csv')

    # fig, ax = plt.subplots()

    # Plot data
    scope_data = pd.read_csv(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\Tek000_AA1_ALL.csv', skiprows=13)
    # print(norms.head())
    # Rename the columns to be more descriptive
    scope_data.rename(columns={'TIME': 't', 'CH1': 'V1', 'CH2': 'V2', 'CH3': 'V3', 'CH4':'V4'}, inplace=True)

    # x_values = np.linspace(0, 1, len(norms[0]))
    norm_labels = ['Background', 'Motor', 'Paint A', 'Paint B', 'Paint C', 'No Paint']
    norms = pd.read_csv(r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\dc_norms.csv',header=None)
    bar_colors = ['#062bb4', '#2822d4', '#822ee8', '#d96ae0', '#ee94a7', '#fcc2cf']

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

    fig, ax = plt.subplots()
    ax.bar(norm_labels[1:], (norms[0][1:] / 1e-6), color=bar_colors[0:5])
    ax.axhline(y=(norms[0][0]/1e-6), color='red', linestyle='--', label='Background')

    ax.set_ylim((np.amin(norms[0])) / 1e-6 - 0.25, (np.amax(norms[0]) / 1e-6) + 0.25)
    ax.grid(True, axis='y')
    ax.set_ylabel(r'B ($\mu$T)')
    ax.set_title('Room 376B DC Magnetic Field Norms')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
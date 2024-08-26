import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
    return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def get_data(file_pattern):
    # Read all CSV files matching the pattern and concatenate their data
    all_files = glob.glob(file_pattern)
    concatenated_data = []
    for filename in all_files:
        df = pd.read_csv(filename, header=None, usecols=[0,1], names=['Frequency', 'Voltage'])
        concatenated_data.append(df.values)
    return concatenated_data

def process_mc90r_data(data):
    """Process the data from MC90R sensor,
    assuming the data is in the format [frequency, voltage]
    """
    # Read in calibration data in Teslas/Volt and Volts/Tesla
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
    
    frequencies_khz = data[0] / 1000

    interpolated_calibration = get_interpolated_values(frequencies_khz)


    # Calculate the magnetic field
    # Multiply Vrms by sqrt(2) to convert from RMS to peak
    # Multiply by interpolated_calibration to convert from V to T
    # 1560 is the span, 1560/400 is the resolution (400 frequency bins)
    # Divide by sqrt(1560/400) to convert from T to T/sqrt(Hz)
    b_field = data[1]*np.sqrt(2)*interpolated_calibration / np.sqrt(1560/400)

    print(data[0])

    return data[0], b_field

def process_425_data(data):
    # Process the data from DRV425EVM sensor
    # Example processing (customize as needed)
    processed_data = np.fft.fft(data)
    freq = np.fft.fftfreq(len(data))
    return freq, np.abs(processed_data)

def plot_spectrum(mc90r_file_pattern, drv425_file_pattern):
    # Read and concatenate data from multiple CSV files
    mc90r_data = get_data(mc90r_file_pattern)
    drv425_data = get_data(drv425_file_pattern)
    
    # Process the data
    freq_mc90r, spectrum_mc90r = process_mc90r_data(mc90r_data)
    freq_drv425, spectrum_drv425 = process_425_data(drv425_data)
    
    # Plot the spectra
    plt.figure(figsize=(10, 6))
    
    plt.plot(freq_mc90r, spectrum_mc90r, label='MC90R')
    plt.plot(freq_drv425, spectrum_drv425, label='DRV425EVM')
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Magnetic Field Spectrum')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # Example usage
    mc90r_data_path = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\mc90r-s-*'
    drv425_data_path = r'G:\My Drive\Other\REUs\Summer 2024\UCD\Data\006\Without T\425-s-*'

    mc90r_data = get_data(mc90r_data_path)

    freqs, b_field = process_mc90r_data(mc90r_data[0])

    print(f'Shape of freqs: {np.shape(freqs)}\nShape of b_field{np.shape(b_field)}')

    # for data_set in mc90r_data:
    #     freqs, b_field = process_mc90r_data(data_set)

    #     print(f'Shape of freqs: {np.shape(freqs)}\nShape of b_field{np.shape(b_field)}')

    # print(process_mc90r_data(mc90r_data))

    # Plot the spectra
    # plot_spectrum(mc90r_data, drv425_data)
import os
import numpy as np
import pandas as pd

def normalize_path(in_path):
    # A quick function to ensure that any input paths are properly referenced
	return os.path.normpath(os.path.realpath(os.path.expanduser(in_path)))

# Open the file in binary mode
with open(r'A:\GJGJGJ', 'rb') as f:
    # Read the data into a NumPy array
	data = f.read()
	print(type(data))

    # array = np.fromfile(f, dtype=np.uint8)  # Change dtype according to your data
	


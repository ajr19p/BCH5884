#!/usr/bin/env python3
#https://github.com/ajr19p/BCH5884.git
## Import Libraries
import numpy as np
import scipy
import peakutils
import matplotlib.pyplot as plt
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = input("Enter the filename: ")


# Load data
data = np.loadtxt(filename, delimiter=',')


voltage = data[:, 0] # 0th column
current = data[:, 1] # 1st column


# Plot original data
plt.plot(voltage, current, c='#546C66', label='Original Plot')

# Estimate the baseline
baseline_values = peakutils.baseline(current,2)

# Plot the baseline
plt.plot(voltage, baseline_values, c='#EB55BF', label='Baseline')

# Subtract out the baseline
#corrected = current - baseline_values
#plt.plot(voltage, corrected, label='Baseline subtracted')

# Find peaks
#peaks_idx = np.argmax(current)
#peaks_idx = peakutils.indexes(current)
#plt.scatter(voltage[peaks_idx], current[peaks_idx], c='red', label='({:.4f}, {})'.format(voltage[peaks_idx], current[peaks_idx]))



from scipy.signal import find_peaks


#Find all peaks in this file, need to modify prominence and width for the specific data!!!!!!!!
peaks, peak_properties = find_peaks(current, prominence=(None, 0.6), width=5)

plt.plot(voltage[peaks], current[peaks], 'x', c='C1', label="Peak")
plt.vlines(x=voltage[peaks], ymin=current[peaks] - peak_properties["prominences"], ymax = current[peaks], color = "C1")

l = peak_properties["left_ips"]
r = peak_properties["right_ips"]

plt.hlines(y=peak_properties["width_heights"], xmin=voltage[peak_properties["left_ips"].astype(int)], xmax=voltage[peak_properties["right_ips"].astype(int)], color = "C1")

width = voltage[peak_properties["right_ips"].astype(int)] - voltage[peak_properties["left_ips"].astype(int)]
height = current[peaks] - (current[peaks] - peak_properties["prominences"])

for p in range(len(peaks)):
    print("Peak found at:", voltage[peaks[p]])
    print("\tWidth: {}".format(width[p]))
    print("\tHeight: {}".format(height[p]))

plt.title(filename)
plt.xlabel('Voltage')
plt.ylabel('Current')

plt.legend()
plt.savefig('out1.png', dpi=200)
plt.show()

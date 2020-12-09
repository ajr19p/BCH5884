#!/usr/bin/env python3
# https://github.com/ajr19p/BCH5884

import sys
import math

# Read in pdb file and create dictionary
def read_file(filename):
    data = []
    with open(filename, 'r') as f:
        for i, list in enumerate(f):
   
            d = list.strip().split()
            # Data Types
            types = [str, int, str, str, str, int, float, float, float, float, float, str]
            d = [t_i(d_i) for d_i, t_i in zip(d, types)]
            data.append(d)
    return data


def getmass(element):
    massdict = {"H": 1.01, "C": 12.0999, "N": 14.01,
        "O": 15.999, "P": 30.976, "S": 32.059, "Mg": 24.30}
    mass = massdict.get(element)
    return mass

# Calculate RMSD
def RMSD():
    read1 = read_file("2FA9noend.pdb")
    read2 = read_file("2FA9noend2mov.pdb")
    combined = min(len(read1), len(read2))

    total_sum = 0
    for i in range(combined):
        x = (read1[i][6]-read2[i][6])**2
        y = (read1[i][7]-read2[i][7])**2
        z = (read1[i][8]-read2[i][8])**2
        A = x + y + z
        total_sum = total_sum + A

    output = ((1/combined) * total_sum)**0.5
    return output


print(RMSD())

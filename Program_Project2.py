#!/usr/bin/env python3
#https://github.com/ajr19p/BCH5884.git
import numpy as np
from matplotlib import pyplot as plt
f=open('superose6_50.txt')
lines=f.readlines()
f.close()
t=[]
a=[]
for line in lines[3:]:
    words=line.split()
    try:
        t.append(float(words[0]))
        a.append(float(words[1]))
    except:
        print("Could not parse", line)
        continue

t=np.array(t)

#Use Numpy gradient to find rate of change/slope
a=np.array(a)
da=np.gradient(a)
dda=np.gradient(da)

# Set minimum threshold to distinguish from noise
min_ = 50

# Find where the sign in the first derivative changes
indices = np.where(np.diff(np.sign(da)))[0]
# Second derivative-specify where points are above noise
peaks = [i for i in indices if (dda[i] < 0 and a[i] > min_)]

'''
    Finds an edges of a peak by moving left and right starting at the peak
    A threshold parameter is used to filter the derivative

'''
def find_edges(peak, threshold=0.1):
    # Get the left and right derivatives of the chromatogram peaks
    left = da[:peak][::-1]
    right = da[peak+1:]

    # 1st sign change in derivative
    for i, p in enumerate(left):
        if p < 0 or p < threshold:
            left_edge = peak - i
            break

    for i, p in enumerate(right):
        if p > 0 or p > -threshold:
            right_edge = peak + i
            break

    return left_edge, right_edge

# Loop through peaks
for p in peaks:
    le, re = find_edges(p)
# Plot
    plt.scatter(t[p], a[p], c='r')
    plt.axvline(t[le], ls='--', c='black')
    plt.axvline(t[re], ls='--', c='black')
    print('Peak at {}. Range: [{}, {}]'.format(t[p], t[le], t[re]))


plt.plot(t,a, label='data')
plt.plot(t,da, label=r'$\nabla$')
plt.plot(t,dda, label= r'$\nabla^2$')
#plt.xlim(0,170)
plt.legend()
#plt.savefig('out.pdf')
plt.show()
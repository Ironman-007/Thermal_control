#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv
import math
import struct
import sys

data_len = 16

voltages = [-20.82, -4.01, 21.53]

reading_mean = []
reading_err  = []

RTDnum = 3 # which RTD

def read_data(filename):
    file = open(filename,"rb")
    content = file.read()
    data = []

    for i in np.arange(len(content)/data_len, dtype=int):
        word = content[i*data_len+4*RTDnum:i*data_len+4*(RTDnum+1)]
        # word = content[i*data_len:i*data_len+4]
        data.append(int.from_bytes(word, "little"))

    mean = np.mean(data)
    err  = np.std(data)

    return mean, err

mean, err = read_data("Temperature_cali_data_-20_82")
reading_mean.append(mean)
reading_err.append(err)

mean, err = read_data("Temperature_cali_data_-4_01")
reading_mean.append(mean)
reading_err.append(err)

mean, err = read_data("Temperature_cali_data_21_53")
reading_mean.append(mean)
reading_err.append(err)

# SVD
a1 = np.zeros((len(voltages), 2))
a1[:, 0] = 1
x1 = np.linspace(1, len(voltages), num=len(voltages), dtype = int)

for i in x1:
    a1[i-1, 1] = voltages[i-1]

u1, s1, vh1 = np.linalg.svd(a1, full_matrices=True)
u1 = u1[:, :2]
s1 = np.diag(s1)
v1 = vh1.transpose()

y1 = np.zeros((len(reading_mean), 1))
for i in x1:
    y1[i-1] = reading_mean[i-1]

A1 = np.dot(np.dot(np.dot(v1, inv(s1)), u1.transpose()), y1)
x_a1 = np.linspace(1, len(voltages), num=len(voltages), dtype = int)

a1_mean_svd = []

for i in x_a1:
    a1_mean_svd.append(A1[0][0] + A1[1][0]*x_a1[i-1])

print(A1[1][0], A1[0][0])

a = A1[1][0]
b = A1[0][0]

temps = []
for iii in voltages:
    temps.append(iii*a+b)

# Plot
fig, ax = plt.subplots()

ax.errorbar(voltages, reading_mean, reading_err, ecolor='r', label='raw data')
ax.plot(voltages, temps, label='SVD')

legend = ax.legend(loc='upper center')

plt.show()

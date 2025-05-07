import matplotlib.pyplot as plt
import numpy as np
import math
import struct
import sys
from sklearn.linear_model import LinearRegression

temps = [-17.6, -14.3, 13.7, 22.7, 23.8]

data_file_0 = "Temperature_cali_data_-17.6"
data_file_1 = "Temperature_cali_data_-14.3"
data_file_2 = "Temperature_cali_data_13.7"
data_file_3 = "Temperature_cali_data_22.7"
data_file_4 = "Temperature_cali_data_23.8"

bytecnt_per_frame = 16

def calculate_mean_std(data_file):
    with open(data_file, mode='rb') as file: # b is important -> binary
        fileContent = file.read()

    datacnt = len(fileContent)
    framecnt = int(datacnt/bytecnt_per_frame)

    rtd1 = []
    rtd2 = []
    rtd3 = []
    rtd4 = []

    for i in range(framecnt):
        frame_num_i = fileContent[i*bytecnt_per_frame]

        rtd1_i = fileContent[i * bytecnt_per_frame : i * bytecnt_per_frame + 4]
        rtd1.append(int.from_bytes(rtd1_i, "little"))

        rtd2_i = fileContent[i * bytecnt_per_frame + 4 : i * bytecnt_per_frame + 8]
        rtd2.append(int.from_bytes(rtd2_i, "little"))

        rtd3_i = fileContent[i * bytecnt_per_frame + 8 : i * bytecnt_per_frame + 12]
        rtd3.append(int.from_bytes(rtd3_i, "little"))

        rtd4_i = fileContent[i * bytecnt_per_frame + 12 : i * bytecnt_per_frame + 16]
        rtd4.append(int.from_bytes(rtd4_i, "little"))

    rtd1_mean = np.mean(rtd1)
    rtd1_std  = 3*np.std(rtd1)

    rtd2_mean = np.mean(rtd2)
    rtd2_std  = 3*np.std(rtd2)

    rtd3_mean = np.mean(rtd3)
    rtd3_std  = 3*np.std(rtd3)

    rtd4_mean = np.mean(rtd4)
    rtd4_std  = 3*np.std(rtd4)

    print([rtd1_mean, rtd2_mean, rtd3_mean, rtd4_mean, rtd1_std, rtd2_std, rtd3_std, rtd4_std])

    return [rtd1_mean, rtd2_mean, rtd3_mean, rtd4_mean, rtd1_std, rtd2_std, rtd3_std, rtd4_std]

fig = plt.figure()

RTD1_MEAN = []
RTD1_STD = []

RTD2_MEAN = []
RTD2_STD = []

RTD3_MEAN = []
RTD3_STD = []

RTD4_MEAN = []
RTD4_STD = []

RTD1_MEAN.append(calculate_mean_std(data_file_0)[0])
RTD2_MEAN.append(calculate_mean_std(data_file_0)[1])
RTD3_MEAN.append(calculate_mean_std(data_file_0)[2])
RTD4_MEAN.append(calculate_mean_std(data_file_0)[3])

RTD1_MEAN.append(calculate_mean_std(data_file_1)[0])
RTD2_MEAN.append(calculate_mean_std(data_file_1)[1])
RTD3_MEAN.append(calculate_mean_std(data_file_1)[2])
RTD4_MEAN.append(calculate_mean_std(data_file_1)[3])

RTD1_MEAN.append(calculate_mean_std(data_file_2)[0])
RTD2_MEAN.append(calculate_mean_std(data_file_2)[1])
RTD3_MEAN.append(calculate_mean_std(data_file_2)[2])
RTD4_MEAN.append(calculate_mean_std(data_file_2)[3])

RTD1_MEAN.append(calculate_mean_std(data_file_3)[0])
RTD2_MEAN.append(calculate_mean_std(data_file_3)[1])
RTD3_MEAN.append(calculate_mean_std(data_file_3)[2])
RTD4_MEAN.append(calculate_mean_std(data_file_3)[3])

RTD1_MEAN.append(calculate_mean_std(data_file_4)[0])
RTD2_MEAN.append(calculate_mean_std(data_file_4)[1])
RTD3_MEAN.append(calculate_mean_std(data_file_4)[2])
RTD4_MEAN.append(calculate_mean_std(data_file_4)[3])

RTD1_STD.append(calculate_mean_std(data_file_0)[4])
RTD2_STD.append(calculate_mean_std(data_file_0)[5])
RTD3_STD.append(calculate_mean_std(data_file_0)[6])
RTD4_STD.append(calculate_mean_std(data_file_0)[7])

RTD1_STD.append(calculate_mean_std(data_file_1)[4])
RTD2_STD.append(calculate_mean_std(data_file_1)[5])
RTD3_STD.append(calculate_mean_std(data_file_1)[6])
RTD4_STD.append(calculate_mean_std(data_file_1)[7])

RTD1_STD.append(calculate_mean_std(data_file_2)[4])
RTD2_STD.append(calculate_mean_std(data_file_2)[5])
RTD3_STD.append(calculate_mean_std(data_file_2)[6])
RTD4_STD.append(calculate_mean_std(data_file_2)[7])

RTD1_STD.append(calculate_mean_std(data_file_3)[4])
RTD2_STD.append(calculate_mean_std(data_file_3)[5])
RTD3_STD.append(calculate_mean_std(data_file_3)[6])
RTD4_STD.append(calculate_mean_std(data_file_3)[7])

RTD1_STD.append(calculate_mean_std(data_file_4)[4])
RTD2_STD.append(calculate_mean_std(data_file_4)[5])
RTD3_STD.append(calculate_mean_std(data_file_4)[6])
RTD4_STD.append(calculate_mean_std(data_file_4)[7])

plt.errorbar(temps, RTD1_MEAN, yerr=RTD1_STD, fmt ='o')
plt.errorbar(temps, RTD2_MEAN, yerr=RTD2_STD, fmt ='o')
plt.errorbar(temps, RTD3_MEAN, yerr=RTD3_STD, fmt ='o')
plt.errorbar(temps, RTD4_MEAN, yerr=RTD4_STD, fmt ='o')

plt.show()

def LR(x_data, y_data):
    # Reshape the data to fit the model
    X = np.array(x_data).reshape(-1, 1)
    Y = np.array(y_data).reshape(-1, 1)

    # Create a LinearRegression object
    model = LinearRegression()

    # Fit the model to the data
    model.fit(X, Y)

    # Get the slope and intercept of the line
    slope = model.coef_[0]
    intercept = model.intercept_

    return slope, intercept

# Perform linear regression
slope, intercept = LR(temps, RTD1_MEAN)
print("Slope:", slope)
print("Intercept:", intercept)

slope, intercept = LR(temps, RTD2_MEAN)
print("Slope:", slope)
print("Intercept:", intercept)

slope, intercept = LR(temps, RTD3_MEAN)
print("Slope:", slope)
print("Intercept:", intercept)

slope, intercept = LR(temps, RTD4_MEAN)
print("Slope:", slope)
print("Intercept:", intercept)

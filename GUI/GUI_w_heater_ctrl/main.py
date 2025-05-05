#!/usr/bin/env python

from PyQt5 import QtCore, QtWidgets, uic, QtGui
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QApplication, QVBoxLayout
import pyqtgraph as pg
import numpy as np
import datetime
import serial
import sys
import os
import time
from time import sleep
from colorama import Fore, Back, Style
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import struct
import os.path
from binascii import hexlify

a1 = 3.73009464
b1 = 2020.44166436
a2 = 3.72613712
b2 = 2013.50406392
a3 = 3.7352784
b3 = 2016.99632426
a4 = 3.74913261
b4 = 2016.57390942

DATA_NUM = 50
recv_data_cnt = 16

def read_current_time():
    now = datetime.datetime.now(datetime.timezone.utc)
    current_time = now.strftime("%Z:%j/%H:%M:%S")
    return current_time

PID_KP = 0.5
PID_KI = 0.1
PID_KD = 0.05

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setFixedSize(850, 837)

        #Load the UI Page
        uic.loadUi('Thermal_ctrl.ui', self)

        self.serial_ports_list = []
        self.serial_speed = [115200]
        self.RTD_options  = ['OFF', 'RTD1', 'RTD2', 'RTD3', 'RTD4']

        # Ref: https://stackoverflow.com/questions/59898215/break-an-infinit-loop-when-button-is-pressed
        self.timer = QtCore.QTimer(self, interval=5, timeout=self.read_port)
        self.ser=serial.Serial()

        self.clear_btn.clicked.connect(self.clear_plot)
        self.close_btn.clicked.connect(self.close)

        self.scan_btn.clicked.connect(self.scan)
        self.open_btn.clicked.connect(self.open_port)
        self.start_serial_btn.clicked.connect(self.start_read_port)
        self.stop_serial_btn.clicked.connect(self.stop_read_port)

        # self.temp_set_btn.clicked.connect(self.set_temp)
        self.recording_btn.clicked.connect(self.recording_data)
        # self.recording_btn.pressed.connect(self.recording_data)
        self.stoprecording_btn.clicked.connect(self.stoprecording_data)

        # self.load_set_btn.clicked.connect(self.set_load)

        self.manual_btn.clicked.connect(self.set_manual_recording)
        self.auto_btn.clicked.connect(self.set_auto_recording)

        self.set_heater_btn.clicked.connect(self.set_heater)

        self.recording_bar.setValue(0)
        self.recording     = 0
        self.recording_cnt = 0
        self.rec_mode      = 0 # 0: Manu; 1: Auto
        self.REC_DATA_LEN  = 0
        self.LOAD_R        = 50

        self.rtd1_plot.setBackground('w')
        self.rtd2_plot.setBackground('w')
        self.rtd3_plot.setBackground('w')
        self.rtd4_plot.setBackground('w')
        self.heater1_pwm_plt.setBackground('w')
        self.heater2_pwm_plt.setBackground('w')
        self.heater3_pwm_plt.setBackground('w')
        self.heater4_pwm_plt.setBackground('w')

        self.RTD_1_temp = [0] * DATA_NUM
        self.RTD_2_temp = [0] * DATA_NUM
        self.RTD_3_temp = [0] * DATA_NUM
        self.RTD_4_temp = [0] * DATA_NUM

        self.HEATER_1_PWM = [0] * DATA_NUM
        self.HEATER_2_PWM = [0] * DATA_NUM
        self.HEATER_3_PWM = [0] * DATA_NUM
        self.HEATER_4_PWM = [0] * DATA_NUM

        self.heater_pwm1 = 0
        self.heater_pwm2 = 0
        self.heater_pwm3 = 0
        self.heater_pwm4 = 0

        self.heater_target_temp1 = 0
        self.heater_target_temp2 = 0
        self.heater_target_temp3 = 0
        self.heater_target_temp4 = 0

        self.rtd_sel_1 = 0
        self.rtd_sel_2 = 0
        self.rtd_sel_3 = 0
        self.rtd_sel_4 = 0

        self.heater_1_error_old  = 0
        self.heater_1_error      = 0
        self.heater_1_error_acc  = 0
        self.heater_1_error_diff = 0

        self.heater_2_error_old  = 0
        self.heater_2_error      = 0
        self.heater_2_error_acc  = 0
        self.heater_2_error_diff = 0

        self.heater_3_error_old  = 0
        self.heater_3_error      = 0
        self.heater_3_error_acc  = 0
        self.heater_3_error_diff = 0

        self.heater_4_error_old  = 0
        self.heater_4_error      = 0
        self.heater_4_error_acc  = 0
        self.heater_4_error_diff = 0

        self.time_index = list(range(1, DATA_NUM+1))

        self.file = open("temp_no_valid_data", "wb")

        for x in self.serial_speed:
            self.speed_comboBox.addItem(str(x))

        for x in self.RTD_options:
            self.heater1_rtd_sel.addItem(x)
            self.heater2_rtd_sel.addItem(x)
            self.heater3_rtd_sel.addItem(x)
            self.heater4_rtd_sel.addItem(x)

    def scan(self):
        if os.name == 'nt':  # sys.platform == 'win32':
            from serial.tools.list_ports_windows import comports
        elif os.name == 'posix':
            from serial.tools.list_ports_posix import comports

        for info in comports(False):
            port, desc, hwid = info
        iterator = sorted(comports(False))

        self.serial_ports_list = [] # clear the list first
        for n, (port, desc, hwid) in enumerate(iterator, 1):
            self.serial_ports_list.append("{:20} ".format(port))

        ports_num = len(self.serial_ports_list)

        self.serial_comboBox.clear() # clear the list first
        for x in self.serial_ports_list:
            self.serial_comboBox.addItem(x)

        self.start_id = 0

        self.waveform_color = 'b'

    def open_port(self):
        index = self.serial_comboBox.currentIndex()
        serial_ports_port = self.serial_ports_list[index][:-1] # delete the \n at the end
        index = self.speed_comboBox.currentIndex()
        self.ser = serial.Serial(serial_ports_port, self.serial_speed[index])

        current_time = read_current_time()
        self.log.append(current_time + self.ser.name + " Opened @ " + str(self.serial_speed[index]) + "bps")

    def start_read_port(self):
        self.timer.start() # Start monitoring the serialport
        current_time = read_current_time()
        self.log.append(current_time + " :  Start monitoring the Serial Port...")

        self.RTD_1_temp = [0] * DATA_NUM
        self.RTD_2_temp = [0] * DATA_NUM
        self.RTD_3_temp = [0] * DATA_NUM
        self.RTD_4_temp = [0] * DATA_NUM

        self.HEATER_1_PWM = [0] * DATA_NUM
        self.HEATER_2_PWM = [0] * DATA_NUM
        self.HEATER_3_PWM = [0] * DATA_NUM
        self.HEATER_4_PWM = [0] * DATA_NUM

    def stop_read_port(self):
        current_time = read_current_time()
        self.log.append(current_time + " :  Stop monitoring the Serial Port.\n")
        self.timer.stop() # Stop the timer

    def recording_data(self):
        data_log_name = "Temperature_cali_data"

        while (os.path.isfile(data_log_name)):
            data_log_name = data_log_name + "1"
        self.file = open(data_log_name, "wb")

        current_time = read_current_time()
        self.log.append(current_time + " Start recording data...")

        self.recording = 1
        self.recording_cnt = 0

    def stoprecording_data(self):
        if (self.rec_mode == 0):
            current_time = read_current_time()
            self.log.append(current_time + " -------> Stop recording data. <-------")
            self.recording = 0

    def set_temp(self):
        set_temperature = self.temp_spinbox.value()
        tartget_temp = set_temperature.to_bytes(1, byteorder='little',signed=True)
        current_time = read_current_time()
        self.log.append(current_time + " Set platform temperature to " + str(set_temperature) + "degreeC.")
        self.ser.write(tartget_temp)

    def set_manual_recording(self):
        current_time = read_current_time()
        self.log.append(current_time + " Manually recording control.")
        self.rec_mode = 0
        self.recording_cnt = 0

    def set_auto_recording(self):
        current_time = read_current_time()
        self.REC_DATA_LEN = int(self.data_len_input.text())
        self.log.append(current_time + " Automatically recording control -> " + str(self.REC_DATA_LEN))
        self.rec_mode = 1
        self.recording_bar.setMaximum(self.REC_DATA_LEN)
        self.recording_cnt = 0

    def read_port(self):
        if (self.ser.inWaiting()):
            current_time = read_current_time()
            recv_data = self.ser.read(recv_data_cnt)

            rtd_1_temp_i = recv_data[0:4]
            rtd_1_temp_d = int.from_bytes(rtd_1_temp_i, "little")

            rtd_2_temp_i = recv_data[4:8]
            rtd_2_temp_d = int.from_bytes(rtd_2_temp_i, "little")

            rtd_3_temp_i = recv_data[8:12]
            rtd_3_temp_d = int.from_bytes(rtd_3_temp_i, "little")

            rtd_4_temp_i = recv_data[12:16]
            rtd_4_temp_d = int.from_bytes(rtd_4_temp_i, "little")

            rtd_1_temp_d = (rtd_1_temp_d - b1)/a1
            rtd_2_temp_d = (rtd_2_temp_d - b2)/a2
            rtd_3_temp_d = (rtd_3_temp_d - b3)/a3
            rtd_4_temp_d = (rtd_4_temp_d - b4)/a4

            # print(rtd_1_temp_d, rtd_2_temp_d, rtd_3_temp_d, rtd_4_temp_d)
            # show only two digits
            rtd_1_temp_d = round(rtd_1_temp_d, 2)
            rtd_2_temp_d = round(rtd_2_temp_d, 2)
            rtd_3_temp_d = round(rtd_3_temp_d, 2)
            rtd_4_temp_d = round(rtd_4_temp_d, 2)

            if (self.rtd_sel_1 == 1) :
                rtd_ctrl_temp_1 = rtd_1_temp_d
            elif (self.rtd_sel_1 == 2) :
                rtd_ctrl_temp_1 = rtd_2_temp_d
            elif (self.rtd_sel_1 == 3) :
                rtd_ctrl_temp_1 = rtd_3_temp_d
            elif (self.rtd_sel_1 == 4) :
                rtd_ctrl_temp_1 = rtd_4_temp_d

            if (self.rtd_sel_2 == 1) :
                rtd_ctrl_temp_2 = rtd_1_temp_d
            elif (self.rtd_sel_2 == 2) :
                rtd_ctrl_temp_2 = rtd_2_temp_d
            elif (self.rtd_sel_2 == 3) :
                rtd_ctrl_temp_2 = rtd_3_temp_d
            elif (self.rtd_sel_2 == 4) :
                rtd_ctrl_temp_2 = rtd_4_temp_d

            if (self.rtd_sel_3 == 1) :
                rtd_ctrl_temp_3 = rtd_1_temp_d
            elif (self.rtd_sel_3 == 2) :
                rtd_ctrl_temp_3 = rtd_2_temp_d
            elif (self.rtd_sel_3 == 3) :
                rtd_ctrl_temp_3 = rtd_3_temp_d
            elif (self.rtd_sel_3 == 4) :
                rtd_ctrl_temp_3 = rtd_4_temp_d

            if (self.rtd_sel_4 == 1) :
                rtd_ctrl_temp_4 = rtd_1_temp_d
            elif (self.rtd_sel_4 == 2) :
                rtd_ctrl_temp_4 = rtd_2_temp_d
            elif (self.rtd_sel_4 == 3) :
                rtd_ctrl_temp_4 = rtd_3_temp_d
            elif (self.rtd_sel_4 == 4) :
                rtd_ctrl_temp_4 = rtd_4_temp_d

            if(self.rtd_sel_1 == 0):
                self.heater_pwm1 = 0
            else:
                self.heater_1_error = self.heater_target_temp1 - rtd_ctrl_temp_1
                self.heater_1_error_acc += self.heater_1_error
                self.heater_1_error_diff = self.heater_1_error - self.heater_1_error_old
                self.heater_1_error_old = self.heater_1_error

                self.heater_pwm1 = int(PID_KP * self.heater_1_error + PID_KI * self.heater_1_error_acc + PID_KD * self.heater_1_error_diff)

                if (self.heater_pwm1 > 255):
                    self.heater_pwm1 = 255
                if (self.heater_pwm1 < 0):
                    self.heater_pwm1 = 1

            if(self.rtd_sel_2 == 0):
                self.heater_pwm2 = 0
            else:
                self.heater_2_error = self.heater_target_temp2 - rtd_ctrl_temp_2
                self.heater_2_error_acc += self.heater_2_error
                self.heater_2_error_diff = self.heater_2_error - self.heater_2_error_old
                self.heater_2_error_old = self.heater_2_error

                self.heater_pwm2 = int(
                    PID_KP * self.heater_2_error + PID_KI * self.heater_2_error_acc + PID_KD * self.heater_2_error_diff)

                if (self.heater_pwm2 > 255):
                    self.heater_pwm2 = 255
                if (self.heater_pwm2 < 0):
                    self.heater_pwm2 = 1

            if(self.rtd_sel_3 == 0):
                self.heater_pwm3 = 0
            else:
                self.heater_3_error = self.heater_target_temp3 - rtd_ctrl_temp_3
                self.heater_3_error_acc += self.heater_3_error
                self.heater_3_error_diff = self.heater_3_error - self.heater_3_error_old
                self.heater_3_error_old = self.heater_3_error

                self.heater_pwm3 = int(
                    PID_KP * self.heater_3_error + PID_KI * self.heater_3_error_acc + PID_KD * self.heater_3_error_diff)

                if (self.heater_pwm3 > 255):
                    self.heater_pwm3 = 255
                if (self.heater_pwm3 < 0):
                    self.heater_pwm3 = 1

            if(self.rtd_sel_4 == 0):
                self.heater_pwm4 = 0
            else:
                self.heater_4_error = self.heater_target_temp4 - rtd_ctrl_temp_4
                self.heater_4_error_acc += self.heater_4_error
                self.heater_4_error_diff = self.heater_4_error - self.heater_4_error_old
                self.heater_4_error_old = self.heater_4_error

                self.heater_pwm4 = int(
                    PID_KP * self.heater_4_error + PID_KI * self.heater_4_error_acc + PID_KD * self.heater_4_error_diff)

                if (self.heater_pwm4 > 255):
                    self.heater_pwm4 = 255
                if (self.heater_pwm4 < 0):
                    self.heater_pwm4 = 1

            self.HEATER_1_PWM.pop(0)
            self.HEATER_1_PWM.append(self.heater_pwm1)

            self.HEATER_2_PWM.pop(0)
            self.HEATER_2_PWM.append(self.heater_pwm2)

            self.HEATER_3_PWM.pop(0)
            self.HEATER_3_PWM.append(self.heater_pwm3)

            self.HEATER_4_PWM.pop(0)
            self.HEATER_4_PWM.append(self.heater_pwm4)

            self.heater1_pwm_plt.clear()
            self.heater2_pwm_plt.clear()
            self.heater3_pwm_plt.clear()
            self.heater4_pwm_plt.clear()

            self.heater1_pwm_plt.plot(self.time_index, self.HEATER_1_PWM, pen=pg.mkPen('b', width=3))
            self.heater2_pwm_plt.plot(self.time_index, self.HEATER_2_PWM, pen=pg.mkPen('r', width=3))
            self.heater3_pwm_plt.plot(self.time_index, self.HEATER_3_PWM, pen=pg.mkPen('k', width=3))
            self.heater4_pwm_plt.plot(self.time_index, self.HEATER_4_PWM, pen=pg.mkPen('g', width=3))

            self.log.append(current_time + " -> HEATER1: " + str(self.heater_pwm1) + " | HEATER2: " + str(self.heater_pwm2) +
                            " | HEATER3: " + str(self.heater_pwm3) + " | HEATER4: " + str(self.heater_pwm4))

            self.RTD_1_temp.pop(0)
            self.RTD_1_temp.append(rtd_1_temp_d)

            self.RTD_2_temp.pop(0)
            self.RTD_2_temp.append(rtd_2_temp_d)

            self.RTD_3_temp.pop(0)
            self.RTD_3_temp.append(rtd_3_temp_d)

            self.RTD_4_temp.pop(0)
            self.RTD_4_temp.append(rtd_4_temp_d)

            self.rtd1_plot.clear()
            self.rtd2_plot.clear()
            self.rtd3_plot.clear()
            self.rtd4_plot.clear()

            self.rtd1_plot.plot(self.time_index, self.RTD_1_temp, pen=pg.mkPen('b', width=3))
            self.rtd2_plot.plot(self.time_index, self.RTD_2_temp, pen=pg.mkPen('r', width=3))
            self.rtd3_plot.plot(self.time_index, self.RTD_3_temp, pen=pg.mkPen('k', width=3))
            self.rtd4_plot.plot(self.time_index, self.RTD_4_temp, pen=pg.mkPen('g', width=3))

            self.log.append(current_time + " -> RTD1: " + str(rtd_1_temp_d) + " | RTD2: " + str(rtd_2_temp_d) +
                            " | RTD3: " + str(rtd_3_temp_d) + " | RTD4: " + str(rtd_4_temp_d))

            if (self.rec_mode == 0):
                if self.recording == 1:
                    self.file.write(recv_data)
                    self.waveform_color = 'r'

                if self.recording == 0:
                    self.file.close()
                    self.waveform_color = 'b'

            if (self.rec_mode == 1):
                if self.recording == 1:
                    self.file.write(recv_data)
                    self.recording_cnt += 1
                    self.waveform_color = 'r'

                    self.recording_bar.setValue(self.recording_cnt)

                if self.recording_cnt == self.REC_DATA_LEN:
                    self.recording = 0
                    self.log.append(current_time + " -------> Stop automatic recording data. <-------")
                    self.recording_cnt = 0

                if self.recording == 0:
                    self.file.close()
                    self.waveform_color = 'b'

    def set_heater(self):
        self.heater_target_temp1 = int(self.heater1_temp_set.text())
        self.heater_target_temp2 = int(self.heater2_temp_set.text())
        self.heater_target_temp3 = int(self.heater3_temp_set.text())
        self.heater_target_temp4 = int(self.heater4_temp_set.text())

        self.rtd_sel_1 = self.heater1_rtd_sel.currentIndex()
        self.rtd_sel_2 = self.heater2_rtd_sel.currentIndex()
        self.rtd_sel_3 = self.heater3_rtd_sel.currentIndex()
        self.rtd_sel_4 = self.heater4_rtd_sel.currentIndex()

        current_time = read_current_time()
        self.log.append(current_time + " Set Heater PWM: " + str(self.rtd_sel_1) + " | " + str(self.rtd_sel_2) +
                        " | " + str(self.rtd_sel_3) + " | " + str(self.rtd_sel_4))

        self.log.append(current_time + " Set Heater temperature: " + str(self.heater_target_temp1) + " | " + str(self.heater_target_temp2) +
                        " | " + str(self.heater_target_temp3) + " | " + str(self.heater_target_temp4))

    def clear_plot(self):
        self.log.clear()
        self.rtd1_plot.clear()
        self.rtd2_plot.clear()
        self.rtd3_plot.clear()
        self.rtd4_plot.clear()

# driver code 
if __name__ == '__main__': 
    # creating apyqt5 application 
    app = QApplication(sys.argv) 
    # creating a window object 
    main = MainWindow() 
    # showing the window 
    main.show()
    # loop 
    sys.exit(app.exec_()) 

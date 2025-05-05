#pragma once

#include <Arduino.h>

#define packet2recv_LEN 4
#define packet2send_LEN 16

extern uint32_t heater_pwm_1;
extern uint32_t heater_pwm_2;
extern uint32_t heater_pwm_3;
extern uint32_t heater_pwm_4;

extern void Pack_data(void * data, int data_index, size_t data_length);

extern void Getdata_fromGUI(void);
extern void SendData2GUI(void);


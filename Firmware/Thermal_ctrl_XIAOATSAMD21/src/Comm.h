#pragma once

#include <Arduino.h>

#define packet2send_LEN 16

extern uint8_t packet2send[packet2send_LEN];

extern void Pack_data(void * data, int data_index, size_t data_length);

extern void SendData2GUI(void);

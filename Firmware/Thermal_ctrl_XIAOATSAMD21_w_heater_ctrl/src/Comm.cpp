#include <Arduino.h>

#include "Comm.h"

byte * temp_data;

uint8_t packet2send[packet2send_LEN] = {0};

void Pack_data(void * data, int data_index, size_t data_length) {
  temp_data = (byte *) data;
  memcpy(&packet2send[data_index], temp_data, data_length);
}

void SendData2GUI(void) {
  Serial.write(packet2send, packet2send_LEN);
}

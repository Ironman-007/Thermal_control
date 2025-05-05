#include <Arduino.h>

#include "Comm.h"

byte * temp_data;

uint32_t heater_pwm_1 = 0;
uint32_t heater_pwm_2 = 0;
uint32_t heater_pwm_3 = 0;
uint32_t heater_pwm_4 = 0;

uint8_t packet2send[packet2send_LEN] = {0};
char    packet2recv[packet2recv_LEN] = {0};

void Pack_data(void * data, int data_index, size_t data_length) {
  temp_data = (byte *) data;
  memcpy(&packet2send[data_index], temp_data, data_length);
}

void Getdata_fromGUI(void) {
  while (Serial.available()) {
    Serial.readBytes(packet2recv, packet2recv_LEN);
  }

  heater_pwm_1 = (uint32_t)(packet2recv[0]);
  heater_pwm_2 = (uint32_t)(packet2recv[1]);
  heater_pwm_3 = (uint32_t)(packet2recv[2]);
  heater_pwm_4 = (uint32_t)(packet2recv[3]);
}

void SendData2GUI(void) {
  Serial.write(packet2send, packet2send_LEN);
}

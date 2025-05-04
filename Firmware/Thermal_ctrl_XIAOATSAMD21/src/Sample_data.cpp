#include <Arduino.h>

#include "Sample_data.h"
#include "Comm.h"
#include "data2sample.h"
#include "system.h"

uint32_t rtd1 = 0;
uint32_t rtd2 = 0;
uint32_t rtd3 = 0;
uint32_t rtd4 = 0;

void RTD_init(void) {
  pinMode(RTD_PWR_EN, OUTPUT);
  analogReadResolution(12);
  digitalWrite(RTD_PWR_EN, LOW); // Enable power to the RTD
  delay(100); // Allow time for the RTD to stabilize
}

void RTD_power_off(void) {
  digitalWrite(RTD_PWR_EN, LOW); // Disable power to the RTD
}

void RTD_power_on(void) {
  digitalWrite(RTD_PWR_EN, HIGH); // Enable power to the RTD
  delay(EN_STABLE_TIME); // Allow time for the RTD to stabilize
}

void Update_sampling(void) {
  RTD_power_on();

  rtd1 = analogRead(RTD_CH1);
  rtd2 = analogRead(RTD_CH2);
  rtd3 = analogRead(RTD_CH3);
  rtd4 = analogRead(RTD_CH4);

  RTD_power_off(); // Disable power to the RTD

  Pack_data(&rtd1, 0, sizeof(rtd1));
  Pack_data(&rtd2, 0 + sizeof(rtd1), sizeof(rtd2));
  Pack_data(&rtd3, 0 + sizeof(rtd1) + sizeof(rtd2), sizeof(rtd3));
  Pack_data(&rtd4, 0 + sizeof(rtd1) + sizeof(rtd2) + sizeof(rtd3), sizeof(rtd4));
}



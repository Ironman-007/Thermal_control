#include "system.h"

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
  delay(100); // Allow time for the RTD to stabilize
}
#include "heater.h"

void heater_init(void) {
  pinMode(HEATER_PIN_1, OUTPUT);
  pinMode(HEATER_PIN_2, OUTPUT);
  pinMode(HEATER_PIN_3, OUTPUT);
  pinMode(HEATER_PIN_4, OUTPUT);

  digitalWrite(HEATER_PIN_1, LOW);
  digitalWrite(HEATER_PIN_2, LOW);
  digitalWrite(HEATER_PIN_3, LOW);
  digitalWrite(HEATER_PIN_4, LOW);
}

void heater_set_pwm(uint8_t heater_pwm_1, uint8_t heater_pwm_2, uint8_t heater_pwm_3, uint8_t heater_pwm_4) {
  analogWrite(HEATER_PIN_1, heater_pwm_1);
  analogWrite(HEATER_PIN_2, heater_pwm_2);
  analogWrite(HEATER_PIN_3, heater_pwm_3);
  analogWrite(HEATER_PIN_4, heater_pwm_4);
}


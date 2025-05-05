#pragma once

#include <Arduino.h>
#include "system.h"

#define HEATER_PIN_1 7
#define HEATER_PIN_2 8
#define HEATER_PIN_3 9
#define HEATER_PIN_4 10

extern void heater_init(void);
extern void heater_set_pwm(uint8_t heater_pwm_1, uint8_t heater_pwm_2, uint8_t heater_pwm_3, uint8_t heater_pwm_4);
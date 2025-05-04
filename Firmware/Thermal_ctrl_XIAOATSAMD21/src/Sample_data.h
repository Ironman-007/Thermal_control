#pragma once

#include <Arduino.h>

#define RTD_CH1 A3
#define RTD_CH2 A2
#define RTD_CH3 A1
#define RTD_CH4 A0

#define RTD_PWR_EN 6

#define EN_STABLE_TIME 10

// Read the RTD values
extern uint32_t rtd1;
extern uint32_t rtd2;
extern uint32_t rtd3;
extern uint32_t rtd4;

extern void RTD_init(void);
extern void RTD_power_off(void);
extern void RTD_power_on(void);

extern void Update_sampling(void);



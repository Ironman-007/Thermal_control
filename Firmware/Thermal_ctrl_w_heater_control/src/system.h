#include <Arduino.h>

#define RTD_CH1 A3
#define RTD_CH2 A2
#define RTD_CH3 A1
#define RTD_CH4 A0

#define RTD_PWR_EN 6

extern void RTD_init(void);
extern void RTD_power_off(void);
extern void RTD_power_on(void);
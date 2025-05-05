#include "system.h"
#include "Sample_data.h"
#include "heater.h"
#include "Comm.h"

void setup() {
  system_init();
  heater_init();
  RTD_init();
}

void loop() {
  Update_sampling();
  SendData2GUI();
  Getdata_fromGUI();
  heater_set_pwm(heater_pwm_1, heater_pwm_2, heater_pwm_3, heater_pwm_4);
  delay(Sampling_period);
}



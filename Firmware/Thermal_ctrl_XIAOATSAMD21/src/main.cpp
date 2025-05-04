#include "system.h"
#include "Sample_data.h"
#include "Comm.h"

void setup() {
  system_init();
  RTD_init();
}

void loop() {
  Update_sampling();
  SendData2GUI();
  delay(Sampling_period);
}



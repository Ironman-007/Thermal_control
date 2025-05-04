#include "system.h"

void system_init(void) {
  SerialUSB.begin(115200);
  while (!SerialUSB) {
    ;
  }
}

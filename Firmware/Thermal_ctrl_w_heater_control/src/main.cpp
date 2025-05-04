#include "system.h"

// Read the RTD values
int rtd1 = 0;
int rtd2 = 0;
int rtd3 = 0;
int rtd4 = 0;

void setup() {
  // put your setup code here, to run once:
  SerialUSB.begin(115200);
  while (!SerialUSB) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  analogReference(AR_DEFAULT); // Set the analog reference to default

  RTD_init();
}

void loop() {
  RTD_power_on();

  rtd1 = analogRead(RTD_CH1);
  rtd2 = analogRead(RTD_CH2);
  rtd3 = analogRead(RTD_CH3);
  rtd4 = analogRead(RTD_CH4);

  // mean value every 10 samples
  for (int i = 0; i < 10; i++) {
    rtd1 += analogRead(RTD_CH1);
    rtd2 += analogRead(RTD_CH2);
    rtd3 += analogRead(RTD_CH3);
    rtd4 += analogRead(RTD_CH4);
  }
  rtd1 /= 10;
  rtd2 /= 10;
  rtd3 /= 10;
  rtd4 /= 10;

  SerialUSB.print("RTD1: ");
  SerialUSB.print(rtd1);
  SerialUSB.print(",");

  SerialUSB.print("RTD2: ");
  SerialUSB.print(rtd2);
  SerialUSB.print(",");

  SerialUSB.print("RTD3: ");
  SerialUSB.print(rtd3);
  SerialUSB.print(",");

  SerialUSB.print("RTD4: ");
  SerialUSB.println(rtd4);

  RTD_power_off(); // Disable power to the RTD
  delay(100); // Wait for 1 second before the next reading
}


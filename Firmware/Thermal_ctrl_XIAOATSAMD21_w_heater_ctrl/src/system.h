#pragma once

#include <Arduino.h>
#include "Sample_data.h"

#define SAMPLE_FREQ     5

#define Sampling_period 1000/SAMPLE_FREQ - EN_STABLE_TIME // unit: ms

extern void system_init(void);
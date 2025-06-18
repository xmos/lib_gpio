// Copyright 2014-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <xs1.h>
#include <gpio.h>

port p_led = XS1_PORT_4C;

void flash_leds(client output_gpio_if led1, client output_gpio_if led2)
{
  while (1) {
    led1.output(1);
    led2.output(0);
    delay_milliseconds(200);
    led1.output(0);
    led2.output(1);
    delay_milliseconds(200);
  }
}

int main() {
  interface output_gpio_if i_led[2];
  char pin_map[2] = {1, 3}; // i_led[0] -> pin 1, i_led[1] -> pin 3
  par {
    output_gpio(i_led, 2, p_led, pin_map);
    flash_leds(i_led[0], i_led[1]);
  }
  return 0;
}

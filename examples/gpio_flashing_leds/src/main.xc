#include <xs1.h>
#include <gpio.h>

port p_led1 = XS1_PORT_1A;
port p_led2 = XS1_PORT_1B;

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
  interface output_gpio_if i_led1, i_led2;
  par {
    output_gpio(i_led1, p_led1);
    output_gpio(i_led2, p_led2);
    flash_leds(i_led1, i_led2);
  }
  return 0;
}

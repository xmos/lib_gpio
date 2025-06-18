// Copyright 2014-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <xs1.h>
#include <gpio.h>
#include <print.h>

// This example shows how to read the state of two buttons connected to GPIO pins.
port p_button = XS1_PORT_4D; // bits 0 and 1 are the 2 buttons
void button_task(client input_gpio_if button0, client input_gpio_if button1)
{
  int button0_state, button0_prev_state;
  int button1_state, button1_prev_state;

  button0_state = button0.input();
  button1_state = button1.input();
  button0_prev_state = button0_state;
  button1_prev_state = button1_state;

  while(1)
  {
    delay_milliseconds(50);
    button0_state = button0.input();
    button1_state = button1.input();
    if (button0_state != button0_prev_state) {
      if(button0_state == 0) {
        printstrln("Button 0 pressed");
      } else {
        printstrln("Button 0 released");
      }
      button0_prev_state = button0_state;
    }
    if (button1_state != button1_prev_state) {
      if(button1_state == 0) {
        printstrln("Button 1 pressed");
      } else {
        printstrln("Button 1 released");
      }
      button1_prev_state = button1_state;
    }
  }
}

int main() {
  input_gpio_if i_button[2];

  par {
    input_gpio(i_button, 2, p_button, null);
    button_task(i_button[0], i_button[1]);
  }
  return 0;
}

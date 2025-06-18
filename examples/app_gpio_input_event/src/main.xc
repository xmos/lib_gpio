// Copyright 2014-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <xs1.h>
#include <gpio.h>
#include <print.h>

// This example shows how to read the state of two buttons connected to GPIO pins using lib_gpio event API.
port p_button = XS1_PORT_4D; // bits 0 and 1 are the 2 buttons
void button_task(client input_gpio_if button0, client input_gpio_if button1)
{
  int button0_trigger_val = 0;
  int button1_trigger_val = 0;

  button0.event_when_pins_eq(button0_trigger_val);
  button1.event_when_pins_eq(button1_trigger_val);


  while(1)
  {
    select
    {
      case button0.event():
        if(button0_trigger_val == 0)
        {
          printstrln("Button 0 pressed");
        }
        else
        {
          printstrln("Button 0 released");
        }
        button0_trigger_val ^= 1; // Toggle the trigger value
        button0.event_when_pins_eq(button0_trigger_val);
      break;
      case button1.event():
        if(button1_trigger_val == 0)
        {
          printstrln("Button 1 pressed");
        }
        else
        {
          printstrln("Button 1 released");
        }
        button1_trigger_val ^= 1; // Toggle the trigger value
        button1.event_when_pins_eq(button1_trigger_val);
      break;

    }
  }
}

int main() {
  input_gpio_if i_button[2];

  par {
    input_gpio_with_events(i_button, 2, p_button, null);
    button_task(i_button[0], i_button[1]);
  }
  return 0;
}

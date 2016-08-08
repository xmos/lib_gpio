// Copyright (c) 2015-2016, XMOS Ltd, All rights reserved
#include <gpio.h>
#include <xs1.h>
#include <timer.h>
#include <syscall.h>
#include "debug_print.h"

#define NUM_CLIENTS (4)
#define NUM_TEST_EVENTS (2)

port input_port = XS1_PORT_4D;
port trigger_port = XS1_PORT_4B;

void read_port_on_event(client input_gpio_if input_port, unsigned int client_num,
                        client output_gpio_if trigger_port) {
    unsigned int completed_events = 0;
    unsigned int expected_value = (client_num & 1);

    /* Setup event that should trigger immediately */
    input_port.event_when_pins_eq(expected_value);
    debug_printf("xCORE client %d setup pins eq event\n", client_num);

    while (1) {
        select {
            case input_port.event():
                debug_printf("xCORE client %d got input port event\n", client_num);
                completed_events++;
                // Read value on pin to make sure it's correct
                unsigned int pin_data = input_port.input();
                if (pin_data != expected_value) {
                    debug_printf("ERROR: Data 0x%x read by client %d does not match expected data 0x%x\n",
                        pin_data, client_num, expected_value);
                }

                if (completed_events < NUM_TEST_EVENTS) {
                /* Setup event that should trigger later */
                // Flip expected_value each iteration of test
                expected_value = !expected_value;
                input_port.event_when_pins_eq(expected_value);
                debug_printf("xCORE client %d setup pins eq event\n", client_num);
                // Trigger simulator to output new expected_value
                debug_printf("xCORE client %d driving trigger port\n", client_num);
                trigger_port.output(1);
                } else {
                    // Allow other cores to complete
                    delay_microseconds(5);
                    _exit(0);
                }
                break;
        }
    }
}

int main(void) {
    interface input_gpio_if i_input_port[NUM_CLIENTS];
    interface output_gpio_if i_trigger_port[NUM_CLIENTS];
    par {
#if EVENTS
        input_gpio_with_events(i_input_port, NUM_CLIENTS, input_port, null);
#else
        input_gpio(i_input_port, NUM_CLIENTS, input_port, null);
#endif
        output_gpio(i_trigger_port, NUM_CLIENTS, trigger_port, null);
        par (int i = 0; i < NUM_CLIENTS; i++) {
            read_port_on_event(i_input_port[i], i, i_trigger_port[i]);
        }
    }
    return 0;
}

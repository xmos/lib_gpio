// Copyright (c) 2015-2021, XMOS Ltd, All rights reserved
// This software is available under the terms provided in LICENSE.txt.
#include <gpio.h>
#include <xs1.h>
#include <timer.h>
#include <syscall.h>
#include <platform.h>
#include "debug_print.h"

#ifndef CROSSTILE
#define CROSSTILE 0
#endif

#define NUM_CLIENTS (4)
#define TIMESTAMP_TEST_DELAY_MICROSECONDS (5)
#define TIMESTAMP_TEST_DELAY_CLOCKS (TIMESTAMP_TEST_DELAY_MICROSECONDS * XS1_TIMER_MHZ)
#define TIMESTAMP_TEST_DELAY_SLACK_CLOCKS (100 + CROSSTILE?100:0)

on tile[0] : port input_port = XS1_PORT_4D;

void read_port(client input_gpio_if input_port, unsigned int client_num) {
    unsigned int pin_data;
    unsigned int expected_value = (client_num & 1);
    if (SUPPLY_PIN_MAP) {
        expected_value = !expected_value;
    }
    
    if (TIMESTAMPS) {
        gpio_time_t ts1, ts2;
        pin_data = input_port.input_and_timestamp(ts1);
        // Wait known time before second input with timestamp
        delay_microseconds(TIMESTAMP_TEST_DELAY_MICROSECONDS);
        input_port.input_and_timestamp(ts2);
        // Check that the second ts is a later time than the first
        if (porttimeafter(ts1, ts2)) {
            debug_printf("ERROR: Second timestamp (%d) read by client %d appears to be earlier than first (%d)\n",
                ts2, client_num, ts1);
        }
        // Sanity check difference between timestamps
        if ((ts2 - ts1) <
            (TIMESTAMP_TEST_DELAY_CLOCKS - TIMESTAMP_TEST_DELAY_SLACK_CLOCKS)) {
            debug_printf("ERROR: Difference between timestamps (%d, %d) read by client %d smaller than expected\n",
                ts1, ts2, client_num);
        }
        if ((ts2 - ts1) >
            (TIMESTAMP_TEST_DELAY_CLOCKS + TIMESTAMP_TEST_DELAY_SLACK_CLOCKS)) {
            debug_printf("ERROR: Difference between timestamps (%d, %d) read by client %d larger than expected\n",
                ts1, ts2, client_num);
        }
    } else {
        pin_data = input_port.input();
    }

    if (pin_data != expected_value) {
        debug_printf("ERROR: Data 0x%x read by client %d does not match expected data 0x%x\n",
            pin_data, client_num, expected_value);
    } else {
        debug_printf("xCORE client %d input data correctly\n", client_num);
    }

    // Allow other cores to complete
    delay_microseconds(5);
    _exit(0);
}

#if SUPPLY_PIN_MAP
static char pin_map[NUM_CLIENTS] = {1, 0, 3, 2};
#else
#define pin_map null
#endif

int main(void) {
    interface input_gpio_if i_input_port[NUM_CLIENTS];
    par {
#if EVENTS
        on tile[0] : input_gpio_with_events(i_input_port, NUM_CLIENTS, input_port, pin_map);
#else
        on tile[0] : input_gpio(i_input_port, NUM_CLIENTS, input_port, pin_map);
#endif
        par (int i = 0; i < NUM_CLIENTS; i++) {
            on tile[CROSSTILE?i%2:0] : read_port(i_input_port[i], i);
        }
    }
    return 0;
}

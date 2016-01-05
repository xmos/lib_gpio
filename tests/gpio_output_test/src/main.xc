// Copyright (c) 2016, XMOS Ltd, All rights reserved
#include <gpio.h>
#include <xs1.h>
#include <syscall.h>
#include "debug_print.h"

#define NUM_CLIENTS (4)
#define TIMESTAMP_TEST_DELAY_MICROSECONDS (5)
#define TIMESTAMP_TEST_DELAY_CLOCKS (TIMESTAMP_TEST_DELAY_MICROSECONDS * XS1_TIMER_MHZ)
#define TIMESTAMP_TEST_DELAY_SLACK_CLOCKS (100)

port output_port = XS1_PORT_4D;
port trigger_port = XS1_PORT_4B;

void wait_for_termination_signal() {
    debug_printf("xCORE waiting for termination signal\n");
    select {
        case trigger_port when pinsneq(0) :> int _:
          _exit(0);
          break;
    }
}

void drive_port(client output_gpio_if output_port, unsigned int client_num) {
    unsigned int expected_pin_data = (client_num & 1);
    if (SUPPLY_PIN_MAP) {
        expected_pin_data = !expected_pin_data;
    }

    if (TIMESTAMPS) {
        gpio_time_t ts1, ts2;
        debug_printf("xCORE client %d driving port\n", client_num);
        ts1 = output_port.output_and_timestamp(expected_pin_data);
        // Wait known time before second input with timestamp
        delay_microseconds(TIMESTAMP_TEST_DELAY_MICROSECONDS);
        ts2 = output_port.output_and_timestamp(expected_pin_data);
        // Check that the second ts is a later time than the first
        if (porttimeafter(ts1, ts2)) {
            debug_printf("ERROR: Second timestamp (%d) received by client %d appears to be earlier than first (%d)\n",
                ts2, client_num, ts1);
        }
        // Sanity check difference between timestamps
        if ((ts2 - ts1) <
            (TIMESTAMP_TEST_DELAY_CLOCKS - TIMESTAMP_TEST_DELAY_SLACK_CLOCKS)) {
            debug_printf("ERROR: Difference between timestamps (%d, %d) received by client %d smaller than expected\n",
                ts1, ts2, client_num);
        }
        if ((ts2 - ts1) >
            (TIMESTAMP_TEST_DELAY_CLOCKS + TIMESTAMP_TEST_DELAY_SLACK_CLOCKS)) {
            debug_printf("ERROR: Difference between timestamps (%d, %d) received by client %d larger than expected\n",
                ts1, ts2, client_num);
        }
    } else {
        debug_printf("xCORE client %d driving port\n", client_num);
        output_port.output(expected_pin_data);
    }
}

int main(void) {
    interface output_gpio_if i_output_port[NUM_CLIENTS];
#if SUPPLY_PIN_MAP
    char pin_map[NUM_CLIENTS] = {1, 0, 3, 2};
#else
#define pin_map null
#endif
    par {
        output_gpio(i_output_port, NUM_CLIENTS, output_port, pin_map);
        par (int i = 0; i < NUM_CLIENTS; i++) {
            drive_port(i_output_port[i], i);
        }
    wait_for_termination_signal();
    }
    return 0;
}

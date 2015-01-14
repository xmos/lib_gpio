#include <gpio.h>
#include <xs1.h>
#include <timer.h>
#include <syscall.h>
#include "debug_print.h"

#define NUM_TEST_EVENTS (2)
#define TIMESTAMP_TEST_DELAY_MICROSECONDS (5)
#define TIMESTAMP_TEST_DELAY_CLOCKS (TIMESTAMP_TEST_DELAY_MICROSECONDS * XS1_TIMER_MHZ)
#define TIMESTAMP_TEST_DELAY_SLACK_CLOCKS (100)

port input_port = XS1_PORT_1A;
port trigger_port = XS1_PORT_4B;

void read_port_on_event(client input_gpio_if input_port) {
    unsigned int completed_events = 0;
    unsigned int expected_value = 1;

    /* Setup event that should trigger immediately */
    input_port.event_when_pins_eq(expected_value);
    debug_printf("xCORE setup pins eq event\n");

    while (1) {
        select {
            case input_port.event():
                debug_printf("xCORE got input port event\n");
                completed_events++;
                // Read value on pin to make sure it's correct
                unsigned int pin_data = input_port.input();
                if (pin_data != expected_value) {
                    debug_printf("ERROR: Data 0x%x read does not match expected data 0x%x\n",
                        pin_data, expected_value);
                }

                if (completed_events < NUM_TEST_EVENTS) {
                /* Setup event that should trigger later */
                // Flip expected_value each iteration of test
                expected_value = !expected_value;
                input_port.event_when_pins_eq(expected_value);
                debug_printf("xCORE setup pins eq event\n");
                // Trigger simulator to output new expected_value
                debug_printf("xCORE driving trigger port\n");
                trigger_port <: 1;
                } else {
                    _exit(0);
                }
                break;
        }
    }
}

void read_port(client input_gpio_if input_port) {
    unsigned int pin_data;
    unsigned int expected_value = 1;
    
    if (TIMESTAMPS) {
        gpio_time_t ts1, ts2;
        pin_data = input_port.input_and_timestamp(ts1);
        // Wait known time before second input with timestamp
        delay_microseconds(TIMESTAMP_TEST_DELAY_MICROSECONDS);
        input_port.input_and_timestamp(ts2);
        // Check that the second ts is a later time than the first
        if (porttimeafter(ts1, ts2)) {
            debug_printf("ERROR: Second timestamp (%d) read appears to be earlier than first (%d)\n",
                ts2, ts1);
        }
        // Sanity check difference between timestamps
        if ((ts2 - ts1) <
            (TIMESTAMP_TEST_DELAY_CLOCKS - TIMESTAMP_TEST_DELAY_SLACK_CLOCKS)) {
            debug_printf("ERROR: Difference between timestamps (%d, %d) read smaller than expected\n",
                ts1, ts2);
        }
        if ((ts2 - ts1) >
            (TIMESTAMP_TEST_DELAY_CLOCKS + TIMESTAMP_TEST_DELAY_SLACK_CLOCKS)) {
            debug_printf("ERROR: Difference between timestamps (%d, %d) read larger than expected\n",
                ts1, ts2);
        }
    } else {
        pin_data = input_port.input();
    }

    if (pin_data != expected_value) {
        debug_printf("ERROR: Data 0x%x read does not match expected data 0x%x\n",
            pin_data, expected_value);
    } else {
        debug_printf("xCORE input data correctly\n");
    }

    _exit(0);
}

int main(void) {
    interface input_gpio_if i_input_port;
    par {
        input_gpio_1bit_with_events(i_input_port, input_port);
#if EVENTS
        read_port_on_event(i_input_port);
#else
        read_port(i_input_port);
#endif
    }
    return 0;
}

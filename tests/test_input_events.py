#!/usr/bin/env python
# Copyright 2015-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import xmostest
from gpio_events_checker import GPIOEventsChecker

def do_input_events_test(events):
    resources = xmostest.request_resource("xsim")

    path = ''
    if not events:
        path += '_basic'
    else:
        if events:
            path += '_events'

    binary = 'gpio_input_events_test/bin/input' + path + \
        '/gpio_input_events_test_input' + path + '.xe'

    checker = GPIOEventsChecker(test_port="tile[0]:XS1_PORT_4D",
                                expected_test_port_data=0b1010,
                                num_clients=4,
                                trigger_port="tile[0]:XS1_PORT_4B")

    tester = xmostest.ComparisonTester(open('input_events_test%s.expected' % path),
                                       'lib_gpio', 'gpio_sim_tests',
                                       'input_events_test',
                                       {'events':events},
                                       regexp=True)

    xmostest.run_on_simulator(resources['xsim'], binary, simthreads = [checker],
                              tester = tester)

def runtest():
    do_input_events_test(events=False)
    do_input_events_test(events=True)

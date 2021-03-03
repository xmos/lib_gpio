#!/usr/bin/env python
# Copyright (c) 2015-2021, XMOS Ltd, All rights reserved
# This software is available under the terms provided in LICENSE.txt.
import xmostest
from gpio_events_checker import GPIOEventsChecker

def do_input_1bit_events_test():
    resources = xmostest.request_resource("xsim")

    binary = 'gpio_input_1bit_test/bin/input_events/gpio_input_1bit_test_input_events.xe'

    checker = GPIOEventsChecker(test_port="tile[0]:XS1_PORT_1A",
                                expected_test_port_data=0b1,
                                num_clients=1,
                                trigger_port="tile[0]:XS1_PORT_4B")

    tester = xmostest.ComparisonTester(open('input_1bit_events_test.expected'),
                                       'lib_gpio', 'gpio_sim_tests',
                                       'input_1bit_events_test',
                                       regexp=False)

    xmostest.run_on_simulator(resources['xsim'], binary, simthreads = [checker],
                              tester = tester)

def runtest():
    do_input_1bit_events_test()

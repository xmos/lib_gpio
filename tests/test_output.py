#!/usr/bin/env python
# Copyright (c) 2015-2019, XMOS Ltd, All rights reserved
import xmostest
from gpio_basic_checker import GPIOBasicChecker

def do_output_test(timestamps, supply_pin_map):
    resources = xmostest.request_resource("xsim")

    path = ''
    if not timestamps and not supply_pin_map:
        path += '_basic'
    else:
        if timestamps:
            path += '_timestamps'
        if supply_pin_map:
            path += '_supply_pin_map'

    binary = 'gpio_output_test/bin/output' + path + \
        '/gpio_output_test_output' + path + '.xe'

    checker = GPIOBasicChecker(mode="output",
                               test_port="tile[0]:XS1_PORT_4D",
                               expected_test_port_data=0b1010,
                               num_clients=4,
                               trigger_port="tile[0]:XS1_PORT_4B")

    if supply_pin_map:
        expected_result = 'output_supply_pin_map_test.expected'
    else:
        expected_result = 'output_test.expected'
    tester = xmostest.ComparisonTester(open(expected_result),
                                       'lib_gpio', 'gpio_sim_tests',
                                       'output_test',
                                       {'timestamps':timestamps,
                                       'supply_pin_map':supply_pin_map},
                                       regexp=True)

    xmostest.run_on_simulator(resources['xsim'], binary, simthreads = [checker],
                              tester = tester)

def runtest():
    do_output_test(timestamps=False, supply_pin_map=False)
    do_output_test(timestamps=False, supply_pin_map=True)
    do_output_test(timestamps=True, supply_pin_map=False)

#!/usr/bin/env python
# Copyright (c) 2015-2021, XMOS Ltd, All rights reserved
# This software is available under the terms provided in LICENSE.txt.
import xmostest
from gpio_basic_checker import GPIOBasicChecker

def do_input_1bit_basic_test(timestamps):
    resources = xmostest.request_resource("xsim")

    path = ''
    if not timestamps:
        path += '_basic'
    else:
        if timestamps:
            path += '_timestamps'

    binary = 'gpio_input_1bit_test/bin/input' + path + \
        '/gpio_input_1bit_test_input' + path + '.xe'

    checker = GPIOBasicChecker(mode="input",
                               test_port="tile[0]:XS1_PORT_1A",
                               expected_test_port_data=0b1,
                               num_clients=1)

    tester = xmostest.ComparisonTester(open('input_1bit_basic_test.expected'),
                                       'lib_gpio', 'gpio_sim_tests',
                                       'input_1bit_basic_test',
                                       {'timestamps':timestamps,},
                                       regexp=False)

    xmostest.run_on_simulator(resources['xsim'], binary, simthreads = [checker],
                              tester = tester)

def runtest():
    do_input_1bit_basic_test(timestamps=False)
    do_input_1bit_basic_test(timestamps=True)

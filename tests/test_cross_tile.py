#!/usr/bin/env python
import xmostest
from gpio_basic_checker import GPIOBasicChecker

def do_cross_tile_test(events, timestamps, supply_pin_map):
    resources = xmostest.request_resource("xsim")

    path = ''
    if not events and not timestamps and not supply_pin_map:
        path += '_basic'
    else:
        if events:
            path += '_events'
        if timestamps:
            path += '_timestamps'
        if supply_pin_map:
            path += '_supply_pin_map'

    binary = 'gpio_cross_tile_test/bin/input' + path + \
        '/gpio_cross_tile_test_input' + path + '.xe'

    checker = GPIOBasicChecker(mode="input",
                               test_port="tile[1]:XS1_PORT_4D",
                               expected_test_port_data=0b1010,
                               num_clients=4)

    tester = xmostest.ComparisonTester(open('input_basic_test.expected'),
                                       'lib_gpio', 'gpio_sim_tests',
                                       'input_basic_test',
                                       {'events':events,
                                       'timestamps':timestamps,
                                       'supply_pin_map':supply_pin_map},
                                       regexp=True)

    xmostest.run_on_simulator(resources['xsim'], binary, simthreads = [checker],
                              tester = tester)

def runtest():
    do_cross_tile_test(events=False, timestamps=False, supply_pin_map=False)
    do_cross_tile_test(events=False, timestamps=False, supply_pin_map=True)
    do_cross_tile_test(events=False, timestamps=True, supply_pin_map=False)
    do_cross_tile_test(events=True, timestamps=False, supply_pin_map=False)
    do_cross_tile_test(events=True, timestamps=True, supply_pin_map=False)

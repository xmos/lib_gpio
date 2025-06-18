#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
import Pyxsim
from Pyxsim import testers
from gpio_basic_checker import GPIOBasicChecker

@pytest.mark.parametrize("timestamps, supply_pin_map", [[False, False],
                                                        [False, True],
                                                        [True, False]
                                                        ])
def test_output(timestamps, supply_pin_map, capfd):
    timestamps = int(timestamps)
    supply_pin_map = int(supply_pin_map)
    path = f"gpio_output_test/bin/{timestamps}_{supply_pin_map}/gpio_output_test_{timestamps}_{supply_pin_map}.xe"
    build_ops = [f"TIMESTAMPS={timestamps}", f"SUPPLY_PIN_MAP={supply_pin_map}"]

    checker = GPIOBasicChecker(mode="output",
                               test_port="tile[0]:XS1_PORT_4D",
                               expected_test_port_data=0b1010,
                               num_clients=4,
                               trigger_port="tile[0]:XS1_PORT_4B")

    expected_result = "expected/output_test.expected"

    tester = testers.ComparisonTester(open(expected_result), regexp=True)

    assert Pyxsim.run_on_simulator(
        path, simthreads=[checker], tester=tester, capfd=capfd, build_options=build_ops)

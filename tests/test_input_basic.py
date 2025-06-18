#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
import Pyxsim
from Pyxsim import testers
from gpio_basic_checker import GPIOBasicChecker

@pytest.mark.parametrize("events, timestamps, supply_pin_map, crosstile", [
                        (False, False, False, False),
                        (False, False, True, False),
                        (False, True, False, False),
                        (True, False, False, False),
                        (True, True, False, False),
                        (False, False, False, True),
                        (True, True, True, True)
])
def test_input_basic(events, timestamps, supply_pin_map, crosstile, capfd):
    events = int(events)
    timestamps = int(timestamps)
    supply_pin_map = int(supply_pin_map)
    crosstile = int(crosstile)
    build_ops = [
        f"EVENTS={events}",
        f"TIMESTAMPS={timestamps}",
        f"SUPPLY_PIN_MAP={supply_pin_map}",
        f"CROSSTILE={crosstile}"
    ]

    path = f"gpio_input_basic_test/bin/{events}_{timestamps}_{supply_pin_map}_{crosstile}/gpio_input_basic_test_{events}_{timestamps}_{supply_pin_map}_{crosstile}.xe"

    expected_result = "expected/input_basic_test.expected"

    checker = GPIOBasicChecker(mode="input",
                               test_port="tile[0]:XS1_PORT_4D",
                               expected_test_port_data=0b1010,
                               num_clients=4)

    tester = testers.ComparisonTester(open(expected_result), regexp=True)

    assert Pyxsim.run_on_simulator(
        path, simthreads=[checker], tester=tester, capfd=capfd, build_options=build_ops)
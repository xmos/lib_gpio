#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
import Pyxsim
from Pyxsim import testers
from gpio_events_checker import GPIOEventsChecker

@pytest.mark.parametrize("events, timestamps", [(True, False)])
def test_input_1bit_events(events, timestamps, capfd):
    events = int(events)
    timestamps = int(timestamps)
    path = f"gpio_input_1bit_test/bin/{events}_{timestamps}/gpio_input_1bit_test_{events}_{timestamps}.xe"
    build_ops = [f"EVENTS={events}", f"TIMESTAMPS={timestamps}"]

    expected_result = "expected/input_1bit_events_test.expected"

    checker = GPIOEventsChecker(test_port="tile[0]:XS1_PORT_1A",
                                expected_test_port_data=0b1,
                                num_clients=1,
                                trigger_port="tile[0]:XS1_PORT_4B")

    tester = testers.ComparisonTester(open(expected_result), regexp=False)

    assert Pyxsim.run_on_simulator(
        path, simthreads=[checker], tester=tester, capfd=capfd, build_options=build_ops)

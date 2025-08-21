#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
import Pyxsim
from Pyxsim import testers
from pathlib import Path
from gpio_events_checker import GPIOEventsChecker

@pytest.mark.parametrize("events, timestamps", [(True, False)])
def test_input_1bit_events(events, timestamps, capfd):
    events = int(events)
    timestamps = int(timestamps)

    test_name = Path(__file__).stem
    file_path = Path(__file__).resolve().parent

    bin_path = file_path/f"test_input_1bit/bin/{events}_{timestamps}/test_input_1bit_{events}_{timestamps}.xe"
    assert bin_path.exists()

    expected_file = file_path/f"expected/{test_name}.expected"
    assert expected_file.exists()

    checker = GPIOEventsChecker(test_port="tile[0]:XS1_PORT_1A",
                                expected_test_port_data=0b1,
                                num_clients=1,
                                trigger_port="tile[0]:XS1_PORT_4B")

    tester = testers.ComparisonTester(open(expected_file), regexp=False)

    assert Pyxsim.run_on_simulator_(
        bin_path, do_xe_prebuild=False, simthreads=[checker], tester=tester, capfd=capfd)

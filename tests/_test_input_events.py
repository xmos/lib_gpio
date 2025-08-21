#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
from pathlib import Path
import Pyxsim
from Pyxsim import testers
from gpio_events_checker import GPIOEventsChecker

@pytest.mark.parametrize("events", [False, True])
def test_input_events(events, capfd):
    events = int(events)

    test_name = Path(__file__).stem
    file_path = Path(__file__).resolve().parent

    bin_path = file_path/f"{test_name}/bin/{events}/{test_name}_{events}.xe"
    assert bin_path.exists()

    if events:
        expected_file = file_path/f"expected/{test_name}_events.expected"
    else:
        expected_file = file_path/f"expected/{test_name}_basic.expected"

    assert expected_file.exists()

    checker = GPIOEventsChecker(test_port="tile[0]:XS1_PORT_4D",
                                expected_test_port_data=0b1010,
                                num_clients=4,
                                trigger_port="tile[0]:XS1_PORT_4B")

    tester = testers.ComparisonTester(open(expected_file), regexp=True)

    assert Pyxsim.run_on_simulator_(
        bin_path, do_xe_prebuild=False, simthreads=[checker], tester=tester, capfd=capfd)

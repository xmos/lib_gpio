#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
import Pyxsim
from Pyxsim import testers
from pathlib import Path
from gpio_basic_checker import GPIOBasicChecker
from helpers import print_expected_vs_output

@pytest.mark.parametrize("events, timestamps", [
    (False, False),
    (False, True)
])
def test_input_1bit_basic(events, timestamps, capfd, verbosity):
    events = int(events)
    timestamps = int(timestamps)

    test_name = Path(__file__).stem
    filepath = Path(__file__).resolve().parent

    bin_path = filepath/f"test_input_1bit/bin/{events}_{timestamps}/test_input_1bit_{events}_{timestamps}.xe"
    assert bin_path.exists()

    expected_file = filepath/f"expected/{test_name}.expected"
    assert expected_file.exists()

    with open(expected_file) as exp:
        expected = exp.read().splitlines()

    checker = GPIOBasicChecker(mode="input",
                               test_port="tile[0]:XS1_PORT_1A",
                               expected_test_port_data=0b1,
                               num_clients=1)

    tester = testers.ComparisonTester(expected, regexp=False)

    Pyxsim.run_on_simulator_(
        bin_path, do_xe_prebuild=False, simthreads=[checker], tester=None, capfd=capfd)

    output = print_expected_vs_output(expected, capfd, verbosity)

    assert tester.run(output), output

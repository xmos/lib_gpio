#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
import Pyxsim
from Pyxsim import testers
from pathlib import Path
from gpio_basic_checker import GPIOBasicChecker
from helpers import print_expected_vs_output


@pytest.mark.parametrize("timestamps, supply_pin_map", [[False, False],
                                                        [False, True],
                                                        [True, False]
                                                        ])
def test_output(timestamps, supply_pin_map, capfd, verbosity):

    timestamps = int(timestamps)
    supply_pin_map = int(supply_pin_map)

    test_name = Path(__file__).stem
    file_path = Path(__file__).resolve().parent

    bin_path = file_path/f"{test_name}/bin/{timestamps}_{supply_pin_map}/{test_name}_{timestamps}_{supply_pin_map}.xe"
    assert bin_path.exists()

    expected_file = file_path/f"expected/{test_name}.expected"
    assert expected_file.exists()

    checker = GPIOBasicChecker(mode="output",
                               test_port="tile[0]:XS1_PORT_4D",
                               expected_test_port_data=0b1010,
                               num_clients=4,
                               trigger_port="tile[0]:XS1_PORT_4B")

    with open(expected_file) as exp:
        expected = exp.read().splitlines()

    tester = testers.ComparisonTester(open(expected_file), regexp=True, ordered=False)

    Pyxsim.run_on_simulator_(
        bin_path, do_xe_prebuild=False, simthreads=[checker], tester=None, capfd=capfd)

    output = print_expected_vs_output(expected, capfd, verbosity)

    assert tester.run(output), output


#!/usr/bin/env python
# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest
from pathlib import Path
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

    test_name = Path(__file__).stem
    file_path = Path(__file__).resolve().parent

    bin_path = file_path/f"{test_name}/bin/{events}_{timestamps}_{supply_pin_map}_{crosstile}/{test_name}_{events}_{timestamps}_{supply_pin_map}_{crosstile}.xe"
    assert bin_path.exists()

    expected_file = file_path/f"expected/{test_name}.expected"
    assert expected_file.exists()

    checker = GPIOBasicChecker(mode="input",
                               test_port="tile[0]:XS1_PORT_4D",
                               expected_test_port_data=0b1010,
                               num_clients=4)

    tester = testers.ComparisonTester(open(expected_file), regexp=True)

    assert Pyxsim.run_on_simulator_(
        bin_path, do_xe_prebuild=False, simthreads=[checker], tester=tester, capfd=capfd)

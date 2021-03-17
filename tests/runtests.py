#!/usr/bin/env python
# Copyright 2015-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import xmostest

if __name__ == "__main__":
    xmostest.init()

    xmostest.register_group("lib_gpio",
                            "gpio_sim_tests",
                            "GPIO simulator tests",
    """
Tests are performed by running the GPIO library connected to a simulator model
(written as a python plugin to xsim). The simulator model checks that the pins
are driven and read by the ports as expected. Tests are run to test the
following features:

    * Inputting on a multibit port with multiple clients using the default pin map
    * Inputting on a multibit port with multiple clients using a specified pin map
    * Inputting on a 1bit port
    * Inputting with timestamps
    * Eventing on a multibit input port
    * Eventing on a 1bit input port
    * Outputting on a multibit port with multiple clients using the default pin map
    * Outputting on a multibit port with multiple clients using a specified pin map
    * Outputting with timestamps
""")

    xmostest.runtests()

    xmostest.finish()

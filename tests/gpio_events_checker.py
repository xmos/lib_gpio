# Copyright 2015-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import xmostest

class GPIOEventsChecker(xmostest.SimThread):
    """
    This simulator thread will write to pins to allow xCORE to event.
    """

    def __init__(self, test_port, expected_test_port_data, num_clients,
                 trigger_port):
        self._test_port = test_port
        self._expected_test_port_data = expected_test_port_data
        self._num_clients = num_clients
        self._trigger_port = trigger_port

        print("Checking events on port %s with %d clients" % (self._test_port,
              self._num_clients))
        print("Using port %s as trigger" % (self._trigger_port))

    def drive_port(self, xsi):
        # Check the xCORE is not trying to drive the port
        if xsi.is_port_driving(self._test_port):
            print("ERROR: xCORE driving port %s which expected to be input only"
                % (self._test_port))
        # Drive the test port
        xsi.drive_port_pins(self._test_port, self._expected_test_port_data)
        print("Checker driving port")
        # Flip bits of expected data for second part of test
        self._expected_test_port_data = ~self._expected_test_port_data
        # Delay driving new data to test port until num_client bits of
        # trigger_port go high
        expected_trigger_data = 0
        for i in range(0, self._num_clients):
            expected_trigger_data = (expected_trigger_data << 1) + 1
        print("Checker expecting 0x%x as trigger data" % (expected_trigger_data))
        while True:
            self.wait_for_port_pins_change([self._trigger_port])
            trigger_data = xsi.sample_port_pins(self._trigger_port)
            if trigger_data == expected_trigger_data:
                print("Checker received correct trigger")
                break
        # Drive the test port
        xsi.drive_port_pins(self._test_port, self._expected_test_port_data)
        print("Checker driving port")

    def run(self):
        self.drive_port(self.xsi)
        print("Checker complete")

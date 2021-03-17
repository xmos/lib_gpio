# Copyright 2015-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import xmostest

class GPIOBasicChecker(xmostest.SimThread):
    """
    This simulator thread will read and write to pins.
    """

    def __init__(self, mode, test_port, expected_test_port_data, num_clients,
                 trigger_port = None):
        self._mode = mode
        if self._mode != 'input' and self._mode != 'output':
            print("ERROR: Checker initialised in unsupported mode %s" %
                  (self._mode))
        self._test_port = test_port
        self._expected_test_port_data = expected_test_port_data
        self._num_clients = num_clients
        self._trigger_port = trigger_port

        print("Checking %s on port %s with %d clients" % (self._mode,
              self._test_port, self._num_clients))
        if self._trigger_port != None:
            print("Using port %s as trigger" % (self._trigger_port))

    def drive_port(self, xsi):
        # Check the xCORE is not trying to drive the port
        if xsi.is_port_driving(self._test_port):
            print("ERROR: xCORE driving port %s which expected to be input only"
                  % (self._test_port))
        # Drive the port
        xsi.drive_port_pins(self._test_port, self._expected_test_port_data)
        print("Checker driving port")

    def read_port(self, xsi):
        pin_values = []
        for client in range(0, self._num_clients):
            pin_values.append(-1)

        correct_pin_count = 0
        while (correct_pin_count < self._num_clients):
            # Wait for the xCORE to drive the port
            self.wait_for_port_pins_change([self._test_port])
            port_data = xsi.sample_port_pins(self._test_port)
            for client in range(0, self._num_clients):
                # Check for the updated pin
                pin_data = ((port_data >> client) & 1)
                if pin_values[client] == -1:
                    # Not yet seen the correct pin data yet
                    if pin_data == ((self._expected_test_port_data >>
                                     client) & 1):
                        pin_values[client] = pin_data
                        correct_pin_count +=1
                        print("Checker has seen correct value on pin %d " %
                              (client))
                else: # Check valid pin data has not been overwritten
                    if pin_values[client] != ((self._expected_test_port_data >>
                                               client) & 1):
                        print("ERROR: Data on pin %d changed unexpected" %
                              (client))
        print("Checker has seen all pins change")

        # Drive trigger port to allow xCORE program to terminate
        xsi.drive_port_pins(self._trigger_port, 1)
        print("Checker driving termination trigger")

    def run(self):
        if self._mode == 'input':
            # xCORE testing 'input' functionality means checker must drive port
            self.drive_port(self.xsi)
        elif self._mode == 'output':
            # xCORE testing 'output' functionality means checker must read port
            self.read_port(self.xsi)
        print("Checker complete")

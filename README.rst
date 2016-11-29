GPIO Library
============

Overview
--------

The XMOS GPIO library allows you to access xCORE ports as low-speed GPIO.

Although xCORE ports can be directly accessed via the xC programming
language this library allows more flexible usage. In particular, it
allows splitting a multi-pin output/input port to be able to use
the individual pins independently. It also allows accessing ports
across separate XMOS tiles or separate XMOS chips.

Features
........

 * Abstract interface to GPIO functionality of XMOS ports
 * Allow control of individual bits of multi-bit ports
 * Allow access to ports across tiles

Operating modes
...............

 * Multi-bit output for individual access to the pins of a multi-bit output port
 * Multi-bit input for individual access to the pins of a multi-bit input port
 * Multi-bit input for individual access to the pins of a multi-bit
   input port allowing the application to react to events on those pins

Software version and dependencies
.................................

.. libdeps::

Related application notes
.........................

Currently there are none.
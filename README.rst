GPIO Library
============

Overview
--------

The XMOS GPIO library allows you to access XMOS ports as low-speed
GPIO

Although XMOS ports can be directly accessed via the xC programming
language this library allows more flexible usage. In particular, it
allows splitting a multi-pin output/input port to be able to
the individual pins independently. It also allows accessing ports
across separate XMOS tiles or separate XMOS chips.

Features
........

 * Abstract interface to GPIO functionality of XMOS ports
 * Allow separate access to multibit ports
 * Allow access to ports across tiles

Operating modes
...............

 * Multibit output for individual access to the pins of a multibit output port
 * Multibit input for individual access to the pins of a multibit input port
 * Multibit input for individual access to the pins of a multibit
   input port allowing the application to react to events on those pins

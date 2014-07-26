.. rheader::

   GPIO |version|

GPIO Library
============

GPIO Libary
-----------

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

Components
...........

 * Input, output and bi-directional GPIO components based on a single
   port
 * Multibit output component for individual access to the pins of a
   multibit output port
 * Multibit input component for individual access to the pins of a
   multibit input port

Software version and dependencies
.................................

This document pertains to version |version| of the GPIO library. It is
intended to be used with version 13.x of the xTIMEcomposer studio tools.

The library does not have any dependencies (i.e. it does not rely on any
other libraries).

Related application notes
.........................

The following application notes use this library:

  * AN00113 - How to access individual pins of a multibit port
  * AN00005 - A simple flashing LEDs example using the GPIO library

Hardware characteristics
------------------------

TODO

Restrictions on directions of multibit ports
............................................

API
---

All gpio functions can be accessed via the ``gpio.h`` header::

  #include <gpio.h>

You will also have to add ``lib_gpio`` to the
``USED_MODULES`` field of your application Makefile.

TODO: how GPIO components connect to your code

|newpage|

GPIO interfaces
...............

.. doxygeninterface:: input_gpio_if

|newpage|

.. doxygeninterface:: output_gpio_if

|newpage|

.. doxygeninterface:: inout_gpio_if

|newpage|

Simple GPIO components
......................

.. doxygenfunction:: input_gpio
.. doxygenfunction:: output_gpio
.. doxygenfunction:: inout_gpio

|newpage|

Multibit GPIO components
........................

.. doxygenfunction:: multibit_input_gpio
.. doxygenfunction:: multibit_output_gpio

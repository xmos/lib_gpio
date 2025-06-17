#############################################
lib_gpio: GPIO abstraction for multibit ports
#############################################

***********
Inroduction
***********

The XMOS GPIO library allows accessing xcore ports as low-speed GPIO.

Although xcore ports can be directly accessed via the xC programming
language this library allows more flexible usage. In particular, it
allows splitting a multi-pin output/input port to be able to use
the individual pins independently. It also allows accessing ports
across separate XMOS tiles or separate XMOS chips.

``lib_gpio`` is intended to be used with the `XCommon CMake <https://www.xmos.com/file/xcommon-cmake-documentation/?version=latest>`_
, the `XMOS` application build and dependency management system.

To use this library, include ``lib_gpio`` in the application's ``APP_DEPENDENT_MODULES`` list in
`CMakeLists.txt`, for example:

.. code-block:: cmake

    set(APP_DEPENDENT_MODULES "lib_gpio")

Applications should then include the ``gpio.h`` header file.

|newpage|

**********************************************
Connecting external signals to multi-bit ports
**********************************************

Multi-bit ports can be connected to independent signals in either an
all output configuration (see :ref:`lib_gpio_n_bit_output`) or an all
input configuration (see :ref:`lib_gpio_n_bit_input`). This implies
two important restrictions:

* **Bi-directional signals cannot use this library**
* **The signals on the same port must go in the same direction**

To use bi-directional signals, a dedicated 1-bit hardware port needs
to be used.

.. _lib_gpio_n_bit_input:

.. figure:: images/n_bit_input.*

   Input configuration

.. _lib_gpio_n_bit_output:

.. figure:: images/n_bit_output.*

   Output configuration

Performance restrictions
========================

This library allows independent access to the pins of mulit-bit ports
by multiplexing the port output or input in software. This means that
there are some performance implications, namely:

* The internal buffering, serializing and de-serializing features of
  the xCORE port are not available.
* The software locking and multiplexing between individual bits of
  the port limits performance. As such, toggling
  pins at speed above 1Mhz, for example, is not achievable (on a
  62.5Mhz logical core). The limit may be lower depending on the other
  code is running on the core and how the other pins of the port are being
  driven.

As such, sharing multi-bit ports is most suitable for slow I/O such as
LEDs, buttons and reset lines.

|newpage|

*****
Usage
*****

There are three ways to use the GPIO library:

.. list-table::
  :header-rows: 1

  * - GPIO type
    - Description
  * - Output GPIO
    - Allows control of individual bits of a multi-bit output port.
  * - Input GPIO
    - Allows reading of individual bits of a multi-bit input port.
  * - Input GPIO with events
    - Allows reading of individual bits of a multi-bit input port and
      reacting to events on those pins.

Output GPIO usage
=================

Output GPIO components are instantiated as parallel tasks that run in a
``par`` statement. These components connect to the hardware ports of
the xCORE device. The application
can connect via an interface connection using an array of the ``output_gpio_if``
interface type like in :ref:`output_gpio_task_diag`.

.. _output_gpio_task_diag:

.. figure:: images/output_gpio_task_diag.*

   Output GPIO task diagram

For example, the following code instantiates an output GPIO component
for the first 3 pins of a port and connects to it

.. code-block:: C

  port p = XS1_PORT_4C;

  int main(void) {
    output_gpio_if i_gpio[3];
    par {
      output_gpio(i_gpio, 3, p, null);
      task1(i_gpio[0], i_gpio[1]);
      task2(i_gpio[2]);
    }
    return 0;
  }

Note that the connection is an array of interfaces, so several tasks
can connect to the same component instance, each controlling
different pins of the port.

The application can use the client end of the interface connection to
perform GPIO operations e.g.

.. code-block:: C

  void task1(client output_gpio_if gpio1, client output_gpio_if gpio2)
  {
    // ...
    gpio1.output(1);
    gpio2.output(0);
    delay_milliseconds(200);
    gpio1.output(0);
    gpio2.output(1);
    // ...
  }

More information on interfaces and tasks can be be found in
the `XMOS Programming Guide`_. By default the
output GPIO component does not use any logical cores of its
own. It is a *distributed* task which means it will perform its
function on the logical core of the application task connected to
it (provided the application task is on the same tile).

Input GPIO usage
================

There are two types of input GPIO component: those that support events
and those that do not support events. In both cases,
input GPIO components are instantiated as parallel tasks that run in a
``par`` statement. These components connect to the hardware ports of
the xCORE device. The application
can connect via an interface connection using an array of the ``input_gpio_if``
interface type like in :ref:`input_gpio_task_diag`.

.. _input_gpio_task_diag:

.. figure:: images/input_gpio_task_diag.*

   Input GPIO task diagram

For example, the following code instantiates an input GPIO component
for the first 3 pins of a port and connects to it

.. code-block:: C

  port p = XS1_PORT_4C;

  int main(void) {
    input_gpio_if i_gpio[3];
    par {
      input_gpio(i_gpio, 3, p, null);
      task1(i_gpio[0], i_gpio[1]);
      task2(i_gpio[2]);
    }
    return 0;
  }

Note that the connection is an array of interfaces, so several tasks
can connect to the same component instance, each controlling
different pins of the port.

|newpage|

The application can use the client end of the interface connection to
perform GPIO operations e.g.

.. code-block:: C

  void task1(client input_gpio_if gpio1, client input_gpio_if gpio2)
  {
    // ...
    val1 = gpio1.input();
    val2 = gpio2.input();
    // ...
    val1 = gpio1.input();
    val2 = gpio2.input();
    // ...
  }

More information on interfaces and tasks can be be found in
the `XMOS Programming Guide`_. By default the
output GPIO component does not use any logical cores of its
own. It is a *distributed* task which means it will perform its
function on the logical core of the application task connected to
it (provided the application task is on the same tile).

Input GPIO using events
=======================

The :c:func:`input_gpio_with_events` and
:c:func:`input_gpio_1bit_with_events` functions support the event
based functions of the input GPIO interface

.. code-block:: C

  port p = XS1_PORT_4C;
   
  int main(void) {
    input_gpio_if i_gpio[3];
    par {
      input_gpio_with_events(i_gpio, 3, p, null);
      task1(i_gpio[0], i_gpio[1]);
      task2(i_gpio[2]);
    }
    return 0;
  }

In this case the application can request an event on a pin change and
then select on the event happening e.g.

.. code-block:: C

  gpio.event_when_pins_eq(1);
  select {
    case gpio.event():
      // This event was caused by the pin value being 1
      // ...
      break;
  }


Pin maps
========

The GPIO tasks all take a ``pin_map`` argument. If this is ``null``
then the elements of the inteface array will correspond with the a bit
of the port based on the array element index. So the first element of
the array will control bit 0, the second with control bit 1 and so on.

Alternatively an array can be provided mapping array elements to
pins. For example, the following will map the array indices to pins 3,
2 and 7 of the port

.. code-block:: C

  char pin_map[3] = {3, 2, 7};

  int main() {
    // ...
    par {
      output_gpio(i_gpio, 3, p, pin_map);
      // ...

|newpage|

*********
GPIO APIs
*********

Output GPIO API
===============

Output GPIO components
----------------------

.. doxygenfunction:: output_gpio

Output GPIO interface
---------------------

.. doxygengroup:: output_gpio_if

|newpage|

Input GPIO API
==============

Input GPIO components
---------------------

.. doxygenfunction:: input_gpio
.. doxygenfunction:: input_gpio_with_events
.. doxygenfunction:: input_gpio_1bit_with_events

Input GPIO interface
--------------------

.. doxygengroup:: input_gpio_if

:orphan:

#############################################
lib_gpio: GPIO abstraction for multibit ports
#############################################

:vendor: XMOS
:version: 2.3.0
:scope: General Use
:description: GPIO abstraction for multibit ports
:category: General Purpose
:keywords: GPIO, multibit, ports
:devices: xcore-200, xcore.ai

*******
Summary
*******

The XMOS GPIO library allows accessing xcore ports as low-speed GPIO.

Although xcore ports can be directly accessed via the xC programming
language this library allows more flexible usage. In particular, it
allows splitting a multi-pin output/input port to be able to use
the individual pins independently. It also allows accessing ports
across separate XMOS tiles or separate XMOS chips.

********
Features
********

* Abstract interface to GPIO functionality of XMOS ports
* Allow control of individual bits of multi-bit ports
* Allow access to ports across tiles

************
Known issues
************

* None

****************
Development repo
****************

* `lib_gpio <https://www.github.com/xmos/lib_gpio>`_

**************
Required tools
**************

* XMOS XTC Tools: 15.3.1

*********************************
Required libraries (dependencies)
*********************************

* lib_xassert (www.github.com/xmos/lib_xassert)

*************************
Related application notes
*************************

* None

*******
Support
*******

This package is supported by XMOS Ltd. Issues can be raised against the software at
`www.xmos.com/support <https://www.xmos.com/support>`_

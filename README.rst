:orphan:

#############################################
lib_gpio: GPIO abstraction for multibit ports
#############################################

:vendor: XMOS
:version: 2.2.1
:scope: General Use
:description: GPIO abstraction for multibit ports
:category: General Purpose
:keywords: GPIO, ports
:devices: xcore-200, xcore.ai

*******
Summary
*******

`lib_gpio` provides access to xcore ports as low-speed GPIO.

While `xcore` ports can be accessed directly using the xC programming language, this library offers
more flexibility. In particular, it supports splitting a multi-pin input/output port so that the
individual pins can be used independently. It also enables accessing ports across separate `xcore`
tiles or even across different xcore devices.

********
Features
********

* Abstract interface to GPIO functionality of `xcore` ports
* Allow control of individual bits of multi-bit ports
* Allow access to ports across tiles

************
Known issues
************

* None

****************
Development repo
****************

* `lib_gpio <https://www.github.com/xmos/lib_gpio>`_ (https://www.github.com/xmos/lib_gpio)

**************
Required tools
**************

* XMOS XTC Tools: 15.3.1

*********************************
Required libraries (dependencies)
*********************************

* `lib_xassert <https://www.xmos.com/libraries/lib_assert>`_ (https://www.xmos.com/libraries/lib_xassert)

*************************
Related application notes
*************************

* None

*******
Support
*******

This package is supported by XMOS Ltd. Issues can be raised against the software at
`www.xmos.com/support <https://www.xmos.com/support>`_ or using GitHub `issues <https://github.com/xmos/lib_gpio/issues>`_.

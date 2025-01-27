cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(app_gpio_flashing_leds)

set(APP_HW_TARGET XK-EVK-XU316)

set(APP_DEPENDENT_MODULES "lib_gpio")

set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_LIST_DIR}/../../..)

XMOS_REGISTER_APP()

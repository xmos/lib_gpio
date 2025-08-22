cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(lib_gpio_tests)

add_subdirectory(test_input_1bit)
add_subdirectory(test_input_basic)
add_subdirectory(test_input_events)
add_subdirectory(test_output)


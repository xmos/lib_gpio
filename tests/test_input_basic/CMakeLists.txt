cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(test_input_basic)

set(COMMON_FLAGS -O3 -g -DDEBUG_PRINT_ENABLE=1 -report)

include(${CMAKE_CURRENT_LIST_DIR}/../test_deps.cmake)

set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_LIST_DIR}/../../..)

set(APP_HW_TARGET XK-EVK-XU316)

foreach(EVENTS RANGE 0 1)
    foreach(TIMESTAMPS RANGE 0 1)
        foreach(SUPPLY_PIN_MAP RANGE 0 1)
            foreach(CROSSTILE RANGE 0 1)
                set(APP_COMPILER_FLAGS_${EVENTS}_${TIMESTAMPS}_${SUPPLY_PIN_MAP}_${CROSSTILE}
                    ${COMMON_FLAGS}
                    -DEVENTS=${EVENTS} -DTIMESTAMPS=${TIMESTAMPS}
                    -DSUPPLY_PIN_MAP=${SUPPLY_PIN_MAP} -DCROSSTILE=${CROSSTILE})
            endforeach()
        endforeach()
    endforeach()
endforeach()

XMOS_REGISTER_APP()

COMMON_FLAGS = -O2 -g -save-temps -DDEBUG_PRINT_ENABLE=1 -report


XCOREAI ?= 0
ifeq ($(XCOREAI),0)
TARGET = SLICEKIT-L16
XCC_FLAGS_input_basic = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_events = $(COMMON_FLAGS) -DEVENTS=1 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_timestamps = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_events_timestamps = $(COMMON_FLAGS) -DEVENTS=1 -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_supply_pin_map = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=1 -DCROSSTILE=0
XCC_FLAGS_input_crosstile = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=1
XCC_FLAGS_input_events_timestamps_supply_pin_map_crosstile = $(COMMON_FLAGS) -DEVENTS=1 -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=1 -DCROSSTILE=1
else
TARGET = XCORE-AI-EXPLORER
XCC_FLAGS_input_basic_xcoreai = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_events_xcoreai = $(COMMON_FLAGS) -DEVENTS=1 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_timestamps_xcoreai = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_events_timestamps_xcoreai = $(COMMON_FLAGS) -DEVENTS=1 -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=0
XCC_FLAGS_input_supply_pin_map_xcoreai = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=1 -DCROSSTILE=0
XCC_FLAGS_input_crosstile_xcoreai = $(COMMON_FLAGS) -DEVENTS=0 -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0 -DCROSSTILE=1
XCC_FLAGS_input_events_timestamps_supply_pin_map_crosstile_xcoreai = $(COMMON_FLAGS) -DEVENTS=1 -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=1 -DCROSSTILE=1
endif

# The APP_NAME variable determines the name of the final .xe file. It should
# not include the .xe postfix. If left blank the name will default to
# the project name

APP_NAME =

# The USED_MODULES variable lists other module used by the application.

USED_MODULES = lib_gpio lib_logging

#=============================================================================
# The following part of the Makefile includes the common build infrastructure
# for compiling XMOS applications. You should not need to edit below here.

XMOS_MAKE_PATH ?= ../..
include $(XMOS_MAKE_PATH)/xcommon/module_xcommon/build/Makefile.common

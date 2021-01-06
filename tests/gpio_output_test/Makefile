COMMON_FLAGS = -O2 -g -save-temps -DDEBUG_PRINT_ENABLE=1 -report

# Xcore.ai Builds
# Use `xmake XCOREAI=1`
XCOREAI ?= 0
ifeq ($(XCOREAI),0)
TARGET = SLICEKIT-L16
XCC_FLAGS_output_basic = $(COMMON_FLAGS) -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0
XCC_FLAGS_output_timestamps = $(COMMON_FLAGS) -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=0
XCC_FLAGS_output_supply_pin_map = $(COMMON_FLAGS) -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=1
else
TARGET = XCORE-AI-EXPLORER
XCC_FLAGS_output_basic_xcoreai = $(COMMON_FLAGS) -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=0
XCC_FLAGS_output_timestamps_xcoreai = $(COMMON_FLAGS) -DTIMESTAMPS=1 -DSUPPLY_PIN_MAP=0
XCC_FLAGS_output_supply_pin_map_xcoreai = $(COMMON_FLAGS) -DTIMESTAMPS=0 -DSUPPLY_PIN_MAP=1
endif

APP_NAME =

# The USED_MODULES variable lists other module used by the application.

USED_MODULES = lib_gpio lib_logging

#=============================================================================
# The following part of the Makefile includes the common build infrastructure
# for compiling XMOS applications. You should not need to edit below here.

XMOS_MAKE_PATH ?= ../..
include $(XMOS_MAKE_PATH)/xcommon/module_xcommon/build/Makefile.common

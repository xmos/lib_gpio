# The flags passed to xcc when building the application
# You can also set the following to override flags for a particular language:
# XCC_XC_FLAGS, XCC_C_FLAGS, XCC_ASM_FLAGS, XCC_CPP_FLAGS
# If the variable XCC_MAP_FLAGS is set it overrides the flags passed to
# xcc for the final link (mapping) stage.
COMMON_FLAGS = -O2 -g

# Xcore.ai Builds
# Use `xmake XCOREAI=1`
XCOREAI ?= 0
ifeq ($(XCOREAI),0)
TARGET = SLICEKIT-L16
XCC_FLAGS = $(COMMON_FLAGS)
APP_NAME = gpio_flashing_leds
else
TARGET = XCORE-AI-EXPLORER
XCC_FLAGS_xcoreai = $(COMMON_FLAGS) -DXCOREAI=1
APP_NAME = gpio_flashing_leds_xcoreai
endif

# The USED_MODULES variable lists other module used by the application.
USED_MODULES = lib_gpio

# The XCORE_ARM_PROJECT variable, if set to 1, configures this
# project to create both xCORE and ARM binaries.
XCORE_ARM_PROJECT = 0

XMOS_MAKE_PATH ?= ../..
-include $(XMOS_MAKE_PATH)/xcommon/module_xcommon/build/Makefile.common

set(LIB_NAME lib_gpio)
set(LIB_VERSION 2.2.0)
set(LIB_INCLUDES api)
set(LIB_COMPILER_FLAGS -O3 -Wall -Werror)
set(LIB_DEPENDENT_MODULES "lib_xassert(4.3.1)")

XMOS_REGISTER_MODULE()

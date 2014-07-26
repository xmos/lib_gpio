#ifndef __gpio_h__
#define __gpio_h__
#include <stdint.h>
#include <stddef.h>

#ifdef __XC__

typedef uint16_t gpio_time_t;

/** This interface provides access to a GPIO that can perform input
    operations only. All GPIOs are single bit. */
typedef interface input_gpio_if
{
  /** Perform an input on a GPIO
   *
   *  \returns The value input from the port in the least significant bit.
   *           The rest of the value will be zero extended.
   */
 unsigned input(void);

  /** Perform an input on a GPIO and get a timestamp
   *
   *  \param   timestamp  This pass-by-reference parameter will be set
   *                      to the time the value was input. This timestamp
   *                      is on a timebase relative to the GPIO.
   *
   *  \returns The value input from the port in the least significant bit.
   *           The rest of the value will be zero extended.
   */
 unsigned input_and_timestamp(gpio_time_t &timestamp);
} input_gpio_if;

/** This interface provides access to a GPIO that can perform output
    operations only.  All GPIOs are single bit. */
typedef interface output_gpio_if
{
  /** Perform an output on a GPIO.
   *
   *  \param data  The value to be output. The least significant bit
   *               represents the 1-bit value to be output.
   */
 void output(unsigned data);

  /** Perform an output on a GPIO and get a timestamp of when the output
   *  occurs.
   *
   *  \param data  The value to be output. The least significant bit
   *               represents the 1-bit value to be output.
   *
   *  \returns     The time the value was input. This timestamp
   *               is on a timebase relative to the GPIO.
   */
 gpio_time_t output_and_timestamp(unsigned data);
} output_gpio_if;



/** This interface provides access to a GPIO that can perform input and output
    operations. */
typedef interface inout_gpio_if
{
  /** Perform an input on a GPIO
   *
   *  \returns The value input from the port in the least significant bit.
   *           The rest of the value will be zero extended.
   */
 unsigned input(void);

  /** Perform an input on a GPIO and get a timestamp
   *
   *
   *  \param   timestamp  This pass-by-reference parameter will be set
   *                      to the time the value was input. This timestamp
   *                      is on a timebase relative to the GPIO.
   *
   *  \returns The value input from the port in the least significant bit.
   *           The rest of the value will be zero extended.
   */
 unsigned input_and_timestamp(gpio_time_t &timestamp);

  /** Perform an output on a GPIO.
   *
   *  \param data  The value to be output. The least significant bit
   *               represents the 1-bit value to be output.
   */
 void output(unsigned data);

  /** Perform an output on a GPIO and get a timestamp of when the output
   *  occurs.
   *
   *  \param data  The value to be output. The least significant bit
   *               represents the 1-bit value to be output.
   *
   *  \returns     The time the value was input. This timestamp
   *               is on a timebase relative to the GPIO.
   */
 gpio_time_t output_and_timestamp(unsigned data);
} inout_gpio_if;


[[distributable]]
void inout_gpio(server inout_gpio_if i, port p);

[[distributable]]
void input_gpio(server input_gpio_if i, port p);

[[distributable]]
void output_gpio(server output_gpio_if i, port p);


[[distributable]]
void multibit_output_gpio(server output_gpio_if i[n], size_t n, unsigned pin_map[n], port p_gpio);

[[distributable]]
void multibit_input_gpio(server input_gpio_if i[n], size_t n, port p, unsigned pin_map[n]);

#endif
#endif // __gpio_h__

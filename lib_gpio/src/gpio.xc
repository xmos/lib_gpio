#include <gpio.h>

[[distributable]]
void inout_gpio(server inout_gpio_if i, port p) {
  while (1) {
    select {
    case i.output(unsigned data):
      p <: data;
      break;
    case i.output_and_timestamp(unsigned data) -> gpio_time_t ts:
      p <: data @ ts;
      break;
    case i.input() -> unsigned result:
      p :> result;
      break;
    case i.input_and_timestamp(gpio_time_t &ts) -> unsigned result:
      p :> result @ ts;
      break;
    }
  }
}

[[distributable]]
void input_gpio(server input_gpio_if i, port p) {
  while (1) {
    select {
    case i.input() -> unsigned result:
      p :> result;
      break;
    case i.input_and_timestamp(gpio_time_t &ts) -> unsigned result:
      p :> result @ ts;
      break;
    }
  }
}

[[distributable]]
void output_gpio(server output_gpio_if i, port p) {
  while (1) {
    select {
    case i.output(unsigned data):
      p <: data;
      break;
    case i.output_and_timestamp(unsigned data) -> gpio_time_t ts:
      p <: data @ ts;
      break;
    }
  }
}



[[distributable]]
void multibit_output_gpio(server output_gpio_if i[n], size_t n,
                          unsigned pinput_map[n], port p)
{
  unsigned current_val = 0;
  while (1) {
    select {
    case i[int j].output(unsigned data):
      unsigned pos = pinput_map[j];
      current_val &= ~(1 << pos);
      current_val |= ((data & 1) << pos);
      p <: current_val;
      break;

    case i[int j].output_and_timestamp(unsigned data) -> gpio_time_t ts:
      unsigned pos = pinput_map[j];
      current_val &= ~(1 << pos);
      current_val |= ((data & 1) << pos);
      p <: current_val @ ts;
      break;
    }
  }
}

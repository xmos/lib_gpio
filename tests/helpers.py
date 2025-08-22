# Copyright 2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
from itertools import zip_longest

# Print the comparison in human friendly format
def print_expected_vs_output(expected, capfd, verbosity):
    out, err = capfd.readouterr()
    output = out.split('\n')[:-1] # Need to trim last line
    with capfd.disabled():
        if verbosity > 0:
            print(f"\n{'***EXPECTED***':<40}***ACTUAL***")
        if err:
            print(f"Exceptions encountered: {err}") # Show any exceptions
        for e, o in zip_longest(expected, output, fillvalue = ''):
            if verbosity > 0:
                print(f"{str(e):<40}{str(o)}")

    return output



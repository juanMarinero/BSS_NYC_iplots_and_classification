#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

import numpy as np


def generate_random_color(val):
    # seed for reproducibility in each unique value
    seed = hash(val)
    seed = abs(seed) % (2 ** 32)  # seed must be between 0 and 2**32 - 1
    np.random.seed(seed)

    # Generate a random RGB color
    RGB = np.random.randint(0, 250, size=3)

    # Return the CSS style for the background color
    return f"background-color: rgb({RGB[0]}, {RGB[1]}, {RGB[2]})"

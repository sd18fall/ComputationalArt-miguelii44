"""Miguel Castillo II Computational Art Mini-project"""

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """Build a random function.

    Builds a random function of depth at least min_depth and depth at most
    max_depth. (See the assignment write-up for the definition of depth
    in this context)

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment writ-eup for details on the representation of
        these functions)
    """
    random_depth = random.randint(min_depth, max_depth)
    functions = ["prod", "sin_pi", "cos_pi", "avg", "sin2", "cos2"]
    gigafunction = []
    choice = random.choice(functions)
    if random_depth <= 0:
        xy = ["x", "y"]
        gigafunction.append(random.choice(xy))
        return gigafunction
    elif choice == "prod" or choice == "avg":
        gigafunction.append(choice)
        gigafunction.append(build_random_function(min_depth-1, max_depth-1))
        gigafunction.append(build_random_function(min_depth-1, max_depth-1))
        return gigafunction
    elif choice == "sin_pi" or choice == "cos_pi" or choice =="cos2" or choice == "sin2":
        gigafunction.append(choice)
        gigafunction.append(build_random_function(max_depth-1, max_depth-1))
        return gigafunction
    # return gigafunction


    #for i in range(random_depth):

def evaluate_random_function(f, x, y):
    """Evaluate the random function f with inputs x,y.

    The representation of the function f is defined in the assignment write-up.

    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function

    Returns:
        The function value

    Examples:
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == "x":
        return x

    elif f[0] == "y":
        return y

    elif f[0] == "avg":
        return ((evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y))*0.5)

    elif f[0] == "sin_pi":
        return math.sin(math.pi * evaluate_random_function(f[1], x, y))

    elif f[0] == "cos_pi":
        return math.cos(math.pi * evaluate_random_function(f[1], x, y))

    elif f[0] == "prod":
        return (evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y))

    elif f[0] == "cos2":
        return math.cos(math.pi * (evaluate_random_function(f[1], x, y) * evaluate_random_function(f[1], x, y)))

    elif f[0] == "sin2":
        return math.sin(math.pi * (evaluate_random_function(f[1], x, y) * evaluate_random_function(f[1], x, y)))

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    output_range = output_interval_end - output_interval_start
    input_range = input_interval_end - input_interval_start
    remapped = (((val - input_interval_start)*(output_range) / input_range) + output_interval_start)
    return remapped

def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """Generate a test image with random pixels and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(5, 6)
    print(red_function)
    green_function = build_random_function(5, 6)
    blue_function = build_random_function(5, 6)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myartv2.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")

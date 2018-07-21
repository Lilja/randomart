from PIL import Image
import numpy as np
from random import randint
img_array = []

width = 500
height = 400

def brushsize(array, x_index, y_index, size, rgb_tuple):
    """
    Paint brush by
     * x_index - size
     * x_index + size
     * y_index - size
     * y_index + size
    """
    temp = 0

    for new_pos in range(size):
        new_x_index_left = x_index - new_pos
        new_x_index_right = x_index + new_pos
        new_y_index_left = y_index - new_pos
        new_y_index_right = y_index + new_pos
        positions = [
            (
                new_x_index_left,
                y_index
            ),
            (
                new_x_index_right,
                y_index
            ),
            (
                new_y_index_left,
                x_index
            ),
            (
                new_y_index_right,
                x_index
            )
        ]

        for entry in position:
            x = entry[0]
            y = entry[1]
            array[x, y] = rgb_tuple
    return array

def x_and_y_pos_to_array_position(x_pos, y_pos):
    # https://softwareengineering.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid
    return x_pos + width * y_pos

def array_position_to_x_and_y(array_pos):
    # https://softwareengineering.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid
    return (array_pos / width), (array_pos % width)

def random_position():
    return randint(0, width-1), randint(0, height-1)

def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)

def random_brush_size():
    return randint(0, 5)

img_array = [(255, 255, 255)] * (width*height)

for _ in range(5000):
    x, y = random_position()
    color = random_color()

    print("X: {} Y: {}".format(x, y))
    idx = x_and_y_pos_to_array_position(x, y)
    print("Idx: {} Color: {}".format(idx, color))
    img_array[idx] = color
# print(img_array)
img = Image.new('RGB', (width,height))
img.putdata(img_array)
img.save('img.png')

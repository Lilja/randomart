from PIL import Image
import sys
import yaml
from random_api import *

img_array = []


def x_and_y_pos_to_array_position(x_pos, y_pos, width):
    # https://softwareengineering.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid
    return x_pos + width * y_pos


def array_position_to_x_and_y(array_pos, width):
    # https://softwareengineering.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid
    return (array_pos / width), (array_pos % width)


def config():
    print("Loading YAML")
    conf = yaml.safe_load(open('.env.yaml'))
    print("Done loading YAML")

    keys = conf['keys']
    dims = conf['dimensions']

    width = int(dims.split('x')[0])
    height = int(dims.split('x')[1])

    print("Setting up a canvas of {} x {}".format(width, height))

    output_file_name = conf['filename']
    print("Saving file as {}".format(output_file_name))

    # Initalize an array of width * height with these colors  as standard
    print("Instantiating array")
    img_array = [(0, 0, 0, 255)] * (width * height)

    iterations = conf['iterations']
    print("Will run for {} iteration(s)".format(iterations))

    print("Instantiating Random.org API clients")
    clients = APIClients([
        RandomOrgClient(key)
        for key in keys
    ])

    return img_array, clients, width, height, output_file_name, iterations


def create_color_pool(clients, number_of_colors):
    print("Requesting random colors")
    colors = [
        color
        for color in generate_random_colors(clients.get_client(), number_of_colors)
    ]
    print("{} color(s) loaded.".format(number_of_colors))
    return colors


def create_color_pool_order(clients, number_of_colors):
    print("Requesting random color order")
    color_order = load_random_color_order(clients.get_client(), number_of_colors, number_of_colors-1)
    print("{} color order loaded.".format(number_of_colors))
    return color_order


def run_iteration(clients, img_array, colors, number_of_colors, number_of_xy_positions, total_plots, number_of_runs, width, height):
    color_order = create_color_pool_order(clients, number_of_colors)

    for color_idx in color_order:
        color = colors[color_idx]

        for x, y in generate_integers(clients.get_client(), number_of_xy_positions, width, height):
            idx = x_and_y_pos_to_array_position(x, y, width)
            img_array[idx] = color
            total_plots += number_of_xy_positions

        print("- {} ints requested, {} total points plotted.".format(number_of_xy_positions, total_plots))
    return img_array


def main(arg):
    img_array, clients, width, height, output_file_name, iterations = config()

    number_of_xy_positions_to_create = 100
    number_of_colors_to_create = 10
    total_plots = 0

    colors = create_color_pool(clients, number_of_colors_to_create)

    iterator = 0
    while iterator < 4:
        iterator += 1
        img_array = run_iteration(
            clients,
            img_array,
            colors,
            number_of_colors_to_create,
            number_of_xy_positions_to_create,
            total_plots,
            iterator,
            width,
            height
        )

    img = Image.new('RGBA', (width, height))
    img.putdata(img_array)
    img.show()
    img.save(output_file_name)


if __name__ == '__main__':
    main(sys.argv)

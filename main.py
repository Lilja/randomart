from PIL import Image
from random import randint
import sys
import yaml
from rdoclient_py3 import RandomOrgClient

img_array = []

width = 500
height = 400


def random_org_api(method, params, api_key):
    headers = {
        'Content-Type': 'application/json-rpc'
    }
    params = {
        'jsonrpc': '2.0',
        'method': method,
        'params': {
            'apiKey': api_key,
            **params
        },
        'id': 1234
    }
    print(params)
    url = 'https://api.random.org/json-rpc/1/invoke'
    return requests.get(url, headers=headers, params=params)

def random_integer(client, minimum, maximum, api_key):
    response = client.generate_signed_integers(1000, minimum, maximum)
    data = response.json()['result']['random']['data']
    for rnd in data:
        yield rnd

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
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    alpha = randint(0, 255)
    return r, g, b, alpha

def random_brush_size():
    return randint(0, 5)

def format_number_of_requests(number_of_requests):
    return "I have {} requests left today".format(number_of_requests)

def main(arg):
    conf = yaml.safe_load(open('.env.yaml'))
    key = conf['key']

    img_array = [(255, 255, 255, 255)] * (width*height)

    for _ in range(5000):
        x, y = random_position()
        color = random_color()

        print("X: {} Y: {}".format(x, y))
        idx = x_and_y_pos_to_array_position(x, y)
        print("Idx: {} Color: {}".format(idx, color))
        img_array[idx] = color

    r = RandomOrgClient(key)
    print(r.get_requests_left())
    img = Image.new('RGBA', (width,height))
    img.putdata(img_array)
    img.save('img.png')

if __name__ == '__main__':
    main(sys.argv)

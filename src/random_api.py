from random import randint
from typing import List

from rdoclient_py3 import RandomOrgClient


def brushsize(array, x_index, y_index, size, rgb_tuple):
    """
    Paint brush by
     * x_index - size
     * x_index + size
     * y_index - size
     * y_index + size
    """

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

        for entry in positions:
            x = entry[0]
            y = entry[1]
            array[x, y] = rgb_tuple
    return array


def random_integer(client, n, minimum, maximum):
    response = client.generate_signed_integers(n, minimum, maximum)
    data = response['data']
    for rnd in data:
        yield rnd


def generate_integers(client, n, width, height):
    _x = random_integer(client, n, 0, width - 1)
    _y = random_integer(client, n, 0, height - 1)

    for x, y in zip(_x, _y):
        yield x, y


def random_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    alpha = randint(0, 255)
    return r, g, b, alpha


def generate_random_colors(client, n):
    _r = random_integer(client, n, 0, 255)
    _g = random_integer(client, n, 0, 255)
    _b = random_integer(client, n, 0, 255)
    _a = random_integer(client, n, 0, 255)

    for r, g, b, a in zip(_r, _g, _b, _a):
        yield (r, g, b, a)


def random_brush_size():
    return randint(0, 5)


def format_number_of_requests(number_of_requests):
    return "I have {} requests left today".format(number_of_requests)


def get_random_color(colors):
    return colors[randint(0, len(colors))]


def load_random_color_order(client: RandomOrgClient, amount: int, maximum: int):
    data = client.generate_signed_integers(amount, 0, maximum)
    for entry in data['data']:
        yield entry


class APIClients(object):
    def __init__(self, clients: List[RandomOrgClient]):
        self.clients = clients
        self.state = 0

    def get_client(self):
        start = self.state
        self.state = (self.state + 1) % len(self.clients)
        client = self.clients[self.state]

        while client.get_bits_left() < 1000:
            print(client.get_bits_left())
            if start == self.state:
                raise ValueError('No more clients')
            self.state = (self.state + 1) % len(self.clients)
            client = self.clients[self.state]
        return client

import configmaker
from collections import namedtuple


Action = namedtuple('Action', 'header template')


def get_action(name):
    return configmaker.read(name + '.cfg')



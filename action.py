import glob, os
import config
import configmaker
from collections import namedtuple


Action = namedtuple('Action', 'header template')

# actions = dict()
#
# os.chdir(config.PATH_ACTIONS)
#
#
# for file in glob.glob("*.cfg"):
#     action = configmaker.read(file)
#     actions[file.replace('.cfg', '')] = action
#
#     globals()[file.replace('.cfg', '')] = action


def get_action(name):
    return configmaker.read(name + '.cfg')



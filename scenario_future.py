import random
import os
import config
from string import Formatter
from scheduler import SCHEDULER_HEADER, make_scheduler_config
from generators.common import id_generator
from action import get_action


class Scenario:
    def __init__(self, name):
        self.name = name
        self.matrix = ['//Generated by Sequoia v.{}'.format(config.VERSION)]
        self.scheduler_config = [SCHEDULER_HEADER]
        self.checksum = []

    def get_matrix(self):
        return self.matrix

    def get_config(self):
        return self.scheduler_config

    def get_checksum(self):
        return int(sum(self.checksum))

    def add_step(self, action_name, step, generator, chkfn=None):
        action = get_action(action_name)
        self.matrix.append('')
        self.matrix.append(action.header)
        self.scheduler_config.append(make_scheduler_config(step))

        try:
            for params in generator:
                params['Step'] = step
                mes = action.template.format(**params)
                if chkfn is not None:
                    self.checksum.append(chkfn(params))
                self._matchparams(action, params)
                self.matrix.append(mes)

        except AttributeError as e:
            print(e)
        except DoNotMatchError as e:
            print(e)
            print(e.unmatched)
            return

    def add_static_step(self, step, rand, **args):
        self.matrix.append('')
        self.scheduler_config.append(make_scheduler_config(step))

        id = 'Static'
        if rand:
            id = id_generator(3)

        try:
            header = '#id,#GlobalStep,#Action,#Execute,#TestCase,#Timeout,#Comment'
            message = '{ID},{Step},SetStatic,TRUE,,0,'.format(ID=id, Step=step)

            for k, v in args.items():
                header += ',#' + k
                message += ',' + str(v)

            self.matrix.append(header)
            self.matrix.append(message)

        except AttributeError as e:
            print(e)
        except DoNotMatchError as e:
            print(e)
            print(e.unmatched)
            return

    def push(self, obj, view=False):
        filename, data = None, None

        if obj == 'matrix':
            filename = os.path.join(config.PATH_BASELINES, self.name + '_baseline.csv')
            data = "\n".join(self.matrix)
        elif obj == 'config':
            filename = os.path.join(config.PATH_CONFIGS, self.name + '_config.cfg')
            data = "\n".join(self.scheduler_config)

        with open(filename, 'w') as fout:
            fout.write(data)

            if view:
                print(data)
            else:
                print('\nFile {} was successfully written\n'.format(filename))

    def _matchparams(self, action, generator_params):
        action_params = self._get_action_params(action.template)
        diff = set(action_params) - set(generator_params.keys())

        if diff:
            raise DoNotMatchError(diff)

    def _get_action_params(self, action):
        return [fn for _, fn, _, _ in Formatter().parse(action) if fn is not None]


class DoNotMatchError(Exception):
    def __init__(self, unmatched):
        super().__init__('Error: The following parameters do not match:')

        self.unmatched = '[' + ', '.join(unmatched) + ']'


class Generator:
    def __init__(self):
        pass

    def si_generator(self, n):
        d = {
            'id': 0,
            'price': 0
        }

        for _ in range(n):
            d['id'] = random.randint(1, 10)
            d['price'] = random.randint(1, 10)

            yield d

    def deal_generator(self, n):
        d = {
            'id': 0,
            'price': 0,
            'qty': 0
        }

        for _ in range(n):
            d['id'] = random.randint(1, 10)
            d['price'] = random.randint(1, 10)
            d['qty'] = random.randint(10, 100)

            yield d

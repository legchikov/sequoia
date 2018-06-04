import string
import random

SEED = 10


def range_generator(start=0, end=10, step=1, timeout=100):
    """Generation behave like range(), continuously increase value of parameter N on step
    Input:
    :param start:
    :param end:
    :param step:
    :param timeout:

    Output:
    :param ID:
    """

    # init params
    params = {
        "ID": 0,
        "Timeout": timeout
    }

    # generation
    for _ in range(start, end, step):
        # next
        params['ID'] += 1

        yield params


def execute_script_generator(script_name, parameters='', timeout=10):
    if isinstance(parameters, (list, tuple)) is False:
        parameters = [parameters]
    for p in parameters:
        params = {
            'ID': id_generator(3),
            'Timeout': timeout,
            'ScriptName': script_name,
            'Parameters': p
        }
        yield params


def static_generator(d, randid=False):
    if randid:
        d['ID'] = id_generator(3)
    else:
        d['ID'] = 'Static'
    return d


def verify_ts_generator(scheduler, status, timeout=30000):
    params = {
        'ID': id_generator(3),
        'Timeout': timeout,
        'Scheduler': scheduler,
        'Status': status
    }
    yield params


def verify_countdb_generator(count, query, timeout=10000):
    params = {
        'ID': id_generator(3),
        'Timeout': timeout,
        'Count': count,
        'Query': query
    }
    yield params


def id_generator(size=3, chars=string.ascii_uppercase + string.digits):
    global SEED
    random.seed(SEED)
    SEED += 1
    return ''.join(random.choice(chars) for _ in range(size))

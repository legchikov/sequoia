import string
import random

SEED = 10


def range_generator(start=0, end=10, step=1):
    """Generation behave like range(), continuously increase value of parameter N on step
    Input:
    :param start:
    :param end:
    :param step:

    Output:
    :param N:
    """

    # init params
    params = {
        "N": 0
    }

    # generation
    for _ in range(start, end, step):
        # next
        params['N'] += 1

        yield params


def execute_script_generator(script_name, timeout=10):
    params = {
        'ID': id_generator(3),
        'Timeout': timeout,
        'ScriptName': script_name
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

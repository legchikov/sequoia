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


def transfer_generator(file):
    params = {
        'N': 0,
        'SecAcc': ''
    }

    with open(file) as input:
        for acc in input:
            params['N'] += 1
            params['SecAcc'] = acc.replace('\n', '')

            yield params


def send_broadcast_generator(start=0, end=10, step=1, max_order=9999, timeout=100):
    params = {
        'Timeout': 0,
        'N': 0,
        'zN': 0,
        'Participant': '',
        'Partition': 1,
        'Side': '',
        'Price': '',
        'Qty': '',
    }

    for _ in range(start, end, step):
        # specific condition
        params['N'] += 1
        params['zN'] = str(params['N']).zfill(4)
        params['Commodity'] = (params['N'] % 50) + 1
        params['Price'] = random.randrange(3, 100)
        params['Qty'] = random.randrange(3, 50)

        if params['N'] % max_order == 0:
            params['Partition'] += 1

        if params['N'] == 1:
            params['Timeout'] = 300
        else:
            params['Timeout'] = timeout

        # Buy
        params['Participant'] = '03'
        params['Side'] = 'Buy'
        yield params

        # Sell
        params['Participant'] = '05'
        params['Side'] = 'Sell'
        yield params


def verify_allocation_generator(start=0, end=10, step=1, timeout=1000):
    params = {
        'N': 0,
        'Timeout': timeout,
        'Side': '',
    }

    for _ in range(start, end, step):
        params['N'] += 1

        # Buy
        params['Side'] = 'Buy'
        yield params

        # Sell
        params['Side'] = 'Sell'
        yield params


def send_sese023_generator(start=0, end=10, step=1, timeout=0):
    params = {
        'N': 0,
        'Timeout': timeout,
        'Side': '',
        'SideType': '',
        'BIC': '',
        'SecurityAccount': '',
    }
    for _ in range(start, end, step):
        params['N'] += 1

        # Sell
        params['Side'] = 'Sell'
        params['SideType'] = 'RECE'
        params['BIC'] = 'IGTESTAE'
        params['SecurityAccount'] = '555000018542'
        params['DepositoryBIC_DELI'] = 'CDPLSGSG'
        params['Party_DELI'] = 'NCBICNNK'
        params['DepositoryBIC_RECE'] = ''
        params['Party_RECE'] = ''
        yield params

        # Buy
        params['Side'] = 'Buy'
        params['SideType'] = 'DELI'
        params['BIC'] = 'IGTESTAC'
        params['SecurityAccount'] = '555000018486'

        params['DepositoryBIC_RECE'] = 'CDPLSGSG'
        params['Party_RECE'] = 'NCBICNNK'
        params['DepositoryBIC_DELI'] = ''
        params['Party_DELI'] = ''
        yield params


def execute_script_generator(step, script_name, timeout=0):
    params = {
        'ID': id_generator(3),
        'Step': step,
        'Timeout': timeout,
        'ScriptName': script_name
    }
    yield params


def static_generator(d):
    return d


def verify_ts_generator(step, scheduler, status, timeout=30000):
    params = {
        'ID': id_generator(3),
        'Step': step,
        'Timeout': timeout,
        'Scheduler': scheduler,
        'Status': status
    }
    yield params


def add_securities_generator(start=0, end=10, step=1, instr=10, timeout=0):
    params = {
        'ID': 0,
        'Timeout': timeout,
        'N': 0,
    }

    for _ in range(start, min(end, instr), step):
        params['ID'] += 1
        params['N'] += 1

        yield params


def add_cash_generator(start=0, end=10, step=1, timeout=0):
    params = {
        'ID': 0,
        'Timeout': timeout,
        'Participant': 0,
    }

    for _ in range(start, end, step):
        params['ID'] += 1
        params['Participant'] += 1

        yield params


def verify_countdb_generator(step, count, query, timeout=10000):
    params = {
        'ID': id_generator(3),
        'Step': step,
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

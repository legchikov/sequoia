import operator


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


def send_deal_generator(start=0, end=10, step=1, prefix=100000, max_order=60000):
    """
    Input:
    :param start:
    :param end:
    :param step:
    :param prefix:
    :param max_order:

    Output:
    :param ID:          id of message
    :param Commodity:   commodity of message
    :param Partition:   number of partition
    :param OrderNumber: number of deal (unique among partition)
    :param TradeNumber: number of trade (unique)
    :param Price:       price
    :param Qt:          quantity

    :return:
    """
    # init params
    params = {
        "ID":          0,
        "Commodity":   0,
        "Partition":   0,
        "OrderNumber": 0,
        "TradeNumber": 0,
        "Price":       10,
        "Qty":         7
    }
    # supporting vars

    # generation
    for _ in range(start, end, step):
        # specific condition
        if params['OrderNumber'] == max_order:
            prefix += 100000
            params['OrderNumber'] = 1
            params['Partition'] += 1

        # next
        params['ID'] += 1
        params['Commodity'] = params['OrderNumber'] % 1800
        params['TradeNumber'] = params['OrderNumber'] + prefix
        params['OrderNumber'] += 1

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

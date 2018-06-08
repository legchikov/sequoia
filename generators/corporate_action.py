
def verify_entitlements_generator(stop, start=0, step=1, status=None, timeout=0):
    params = {
        'ID': 0,
        'Timeout': timeout,
        'Status': status,
    }

    for _ in range(start, stop, step):
        params['ID'] += 1

        yield params

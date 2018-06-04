
def verify_entitlements_generator(start=0, end=10, step=1, status=None, timeout=0):
    params = {
        'ID': 0,
        'Timeout': timeout,
        'Status': status,
    }

    for _ in range(start, end, step):
        params['ID'] += 1

        yield params


def verify_secpositions_generator(balance=0, timeout=100):
    params = {
        'Timeout': timeout,
        'Balance': balance,
    }

    yield params

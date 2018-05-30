def settlement_checksum(params):
    tmp = 0
    tmp += params['Qty'] * 2
    tmp += params['Price']
    tmp += 7  # SI_STATUS
    tmp += 13  # SI_SUB_STATUS
    tmp += 6  # PREVIOUS_SI_STATUS
    tmp += 25  # PREVIOUS_SI_SUB_STATUS
    tmp += 0.5  # SIDE
    return tmp

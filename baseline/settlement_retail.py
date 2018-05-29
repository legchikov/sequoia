from scenario import render, sc
from generator import send_broadcast_generator, verify_allocation_generator, send_sese023_generator, \
    execute_script_generator, static_generator, verify_ts_generator, add_cash_generator, add_securities_generator, \
    verify_countdb_generator

from action import get_action

if __name__ == '__main__':

    # Count of messages
    count = 100
    participants = 1  # count of pairs
    instruments = 50
    settlement_cycle = -3

    # Construct the action
    exescript = get_action('ExecuteScript')
    static = get_action('SetStatic')

    send_broadcast = get_action('SendBroadcast')
    verify_allocation = get_action('VerifyAllocation')
    send023 = get_action('SendSese023')
    add_securities = get_action('AddSecurityPosition')
    add_cash = get_action('SendCashBalanceTransactionDB')

    verify_ts = get_action('VerifyTimeScheduleInfo')
    verify_count = get_action('CountDB')

    # Scenario
    sc(exescript, 'CleanSystem', execute_script_generator('Purge.sh'))
    sc(exescript, 'ResetTimeSchedules', execute_script_generator('Turnoff.sh'))

    sc(static, 'Static', static_generator({'Prefix': "@{gen('ggg')}",
                                           'ISIN': 1000000,
                                           'SettlCycle': settlement_cycle}))

    sc(send_broadcast, 'SendDeal', send_broadcast_generator(end=count), True)
    sc(verify_allocation, 'VerifyAllocation', verify_allocation_generator(end=count))
    sc(send023, 'SendSi', send_sese023_generator(end=count))
    sc(add_cash, 'AddCashBalance', add_cash_generator(end=participants))
    sc(add_securities, 'AddSecurityBalance', add_securities_generator(end=count, instr=instruments))

    sc(exescript, 'Netting', execute_script_generator('Netting.sh'))
    sc(verify_ts, 'VerificationNetting', verify_ts_generator('SGXNetting', 'Completed'))
    sc(exescript, 'Processing', execute_script_generator('Processing.sh'))
    sc(verify_ts, 'VerificationProcessing', verify_ts_generator('SGXProcessing', 'Completed'))

    checksum = render(sc, 'checksum')
    sc(static, 'Checksum', static_generator({'Checksum': checksum}, randid=True))

    sc(verify_count, 'VerifyCountSI',
       verify_countdb_generator(count=count * 2, query="SELECT COUNT(*) AS ActualCount FROM ATSD_MOB_SETTLEMENT_INS "
                                                       "WHERE LATEST=1 and SI_STATUS=7 and SI_SUB_STATUS=13 and "
                                                       "REASON_CODE=0 and CREATED_USER='OPEN_API' and "
                                                       "EXTERNAL_REQUEST_ID LIKE 'BIZ@{Static.Prefix}%'"))

    sc(verify_count, 'VerifyCountNoSI',
       verify_countdb_generator(count=0, query="SELECT COUNT(*) AS ActualCount FROM ATSD_MOB_SETTLEMENT_INS "
                                               "WHERE LATEST=1 and (SI_STATUS<>7 or SI_SUB_STATUS<>13 or REASON_CODE<>0)"))

    sc(verify_count, 'VerifyCountNoOptimizedTable',
       verify_countdb_generator(count=0, query="SELECT COUNT(*) AS ActualCount FROM ATSD_TAD_OPTIMIZED_SI "
                                               "WHERE LATEST=1 and (SETTLEMENT_STATUS<>1 or OPTIMIZATION_ALGORITHM<>0)"))

    # Matrix
    matrix = render(sc, 'matrix')
    steps = render(sc, 'steps')

    # Output
    f = open(f'output\settlement_retail_baseline.csv', 'w')

    for line in matrix:
        f.write(line + '\n')
        print(line)
    f.close()

    f = open(f'output\settlement_retail_config.csv', 'w')
    f.write('Global step,Step kind,Start at,Start at type,Parameter,Ask for continue,Ask if failed,Execute,Comment\n')
    for line in steps:
        f.write(line + ',Default,,End of previous step,,1,0,1,' + '\n')
        print(line)
    f.close()

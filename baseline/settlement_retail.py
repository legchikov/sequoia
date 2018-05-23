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
    sc(exescript, execute_script_generator('CleanSystem', 'Purge.sh'))
    sc(exescript, execute_script_generator('ResetTimeSchedules', 'Turnoff.sh'))
    sc(static, static_generator({'ISIN': 1000000}))
    sc(send_broadcast, send_broadcast_generator(end=count))
    sc(verify_allocation, verify_allocation_generator(end=count))
    sc(send023, send_sese023_generator(end=count))
    sc(add_cash, add_cash_generator(end=participants))
    sc(add_securities, add_securities_generator(end=instruments))

    sc(exescript, execute_script_generator('Netting', 'Netting.sh'))
    sc(verify_ts, verify_ts_generator('VerificationNetting', 'SGXNetting', 'Completed'))
    sc(exescript, execute_script_generator('Processing', 'Processing.sh'))
    sc(verify_ts, verify_ts_generator('VerificationProcessing', 'SGXProcessing', 'Completed'))

    sc(verify_count, verify_countdb_generator(step='VerifyCountSI',
                                              count=count*2,
                                              query="SELECT COUNT(*) AS ActualCount FROM ATSD_MOB_SETTLEMENT_INS "
                                              "WHERE LATEST=1 and SI_STATUS=7 and SI_SUB_STATUS=13 and "
                                              "REASON_CODE=0 and CREATED_USER='OPEN_API' and "
                                              "EXTERNAL_REQUEST_ID LIKE 'BIZ@{Static.Prefix}%'"))

    sc(verify_count, verify_countdb_generator(step='VerifyCountNoSI',
                                              count=0,
                                              query="SELECT COUNT(*) AS ActualCount FROM ATSD_MOB_SETTLEMENT_INS "
                                              "WHERE LATEST=1 and (SI_STATUS<>7 or SI_SUB_STATUS<>13 or REASON_CODE<>0)"))

    sc(verify_count, verify_countdb_generator(step='VerifyCountNoOptimizedTable',
                                              count=0,
                                              query="SELECT COUNT(*) AS ActualCount FROM ATSD_TAD_OPTIMIZED_SI "
                                              "WHERE LATEST=1 and (SETTLEMENT_STATUS<>1 or OPTIMIZATION_ALGORITHM<>0)"))

    # Matrix
    matrix = render(sc)

    # Output
    f = open(f'output\settlement_retail_{count}.csv', 'w')

    for line in matrix:
        f.write(line + '\n')
        print(line)
    f.close()

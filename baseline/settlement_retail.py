from scenario_future import Scenario

from checksum import settlement_checksum
from generators.common import execute_script_generator, verify_ts_generator
import generators.settlement as settlgnr


if __name__ == '__main__':

    # Baseline properties
    count = 1
    participants = 1  # count of pairs
    instruments = 50
    settlement_cycle = -3

    # Scenario
    sc = Scenario('settlement_retail')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))

    sc.add_step('ExecuteScript', 'ResetTimeSchedules',
                execute_script_generator('turn_off.sh', parameters=('SGXNetting', 'SGXProcessing')))

    sc.add_static_step('InitStatic', False, Prefix="@{gen('ggg')}", ISIN=1000000, SettlCycle=settlement_cycle)

    sc.add_step('SendBroadcast', 'SendDeal', settlgnr.send_broadcast_generator(stop=count), settlement_checksum)
    sc.add_step('VerifyAllocation', 'VerifyAllocation', settlgnr.verify_allocation_generator(end=count))
    sc.add_step('SendSese023', 'SendSi', settlgnr.send_sese023_generator(stop=count, buyacc='555000018486'))
    sc.add_step('SendCashBalanceTransactionDB', 'AddCashBalance', settlgnr.add_cash_generator(participants))
    sc.add_step('AddSecurityPosition', 'AddSecurityBalance', settlgnr.add_securities_generator(count, instr=instruments))

    sc.add_step('ExecuteScript', 'Netting',
                execute_script_generator('turn_on.sh', parameters='SGXNetting'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationNetting', verify_ts_generator('SGXNetting', 'Completed'))

    sc.add_step('ExecuteScript', 'Processing',
                execute_script_generator('turn_on.sh', parameters='SGXProcessing'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationProcessing', verify_ts_generator('SGXProcessing', 'Completed'))

    sc.add_static_step('Checksum', True, Checksum=sc.get_checksum())

    # sc.add_static_step('VerifyCountSI', True, CountOfEntries=count,
    #                    Query="SELECT COUNT(*) AS ActualCount FROM "
    #                          "ATSD_MOB_SETTLEMENT_INS "
    #                          "WHERE LATEST=1 and SI_STATUS=7 and SI_SUB_STATUS=13 and "
    #                          "REASON_CODE=0 and CREATED_USER='OPEN_API' and "
    #                          "EXTERNAL_REQUEST_ID LIKE 'BIZ@{Static.Prefix}%'")

    sc.push('matrix', view=True)
    sc.push('config')


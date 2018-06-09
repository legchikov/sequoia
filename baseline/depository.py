from scenario_future import Scenario
from generators.common import execute_script_generator, verify_ts_generator, range_generator
import generators.settlement as settlgnr
import generators.depository as gnr


if __name__ == '__main__':

    # Baseline properties
    count = 10
    participants = 1
    settlement_cycle = -3

    # Scenario
    sc = Scenario('depository')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))
    schedulers = ('SGSProcessing', 'SGXNetting', 'SGXProcessing')

    sc.add_step('ExecuteScript', 'ResetTimeSchedules',
                execute_script_generator('turn_off.sh', parameters=schedulers))

    sc.add_static_step('InitStatic', False, Instr="INSTR_0@{gen('ggg')}", Prefix="@{gen('ggg')}",
                       ISIN=1000000, SettlCycle=settlement_cycle)

    # Depository
    sc.add_step('SubmitSecurityDepositDB', 'SubmitSecurityDeposit', execute_script_generator(''))
    sc.add_step('VerifySecurityDeposit', 'VerifySecurityDeposit', execute_script_generator(''))

    sc.add_step('SubmitSecurityTransferDB', 'SubmitSecurityTransfer', range_generator(1, count+1))
    sc.add_step('VerifySecurityTransfer', 'VerifySecurityTransfer', range_generator(1, count+1))

    sc.add_step('ExecuteScript', 'SGSProcessing',
                execute_script_generator('turn_on.sh', parameters='SGSProcessing'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerifySGSProcessing',
                verify_ts_generator('SGSProcessing', 'Completed'))

    sc.add_step('VerifySecurityPositionsDepository', 'VerifyFreeBalance',
                gnr.verify_secpositions_generator(balance=count, timeout=10000))

    # Clearing account transfer
    sc.add_step('SubmitSecurityTransferDBPool', 'SendPoolTransfer',
                gnr.verify_secpositions_generator(balance=count))
    sc.add_step('VerifySecurityPositionsPool', 'VerifyPoolTransfer',
                gnr.verify_secpositions_generator(balance=count, timeout=10000))

    # Settlement
    sc.add_step('SendBroadcast', 'SendDeal', settlgnr.send_broadcast_generator(stop=1, qty=count))
    sc.add_step('VerifyAllocation', 'VerifyAllocation', settlgnr.verify_allocation_generator(end=1))
    sc.add_step('SendSese023', 'SendSi', settlgnr.send_sese023_generator(stop=1, sellacc='@{V_pool_1.PositionAccountID}'))
    sc.add_step('SendCashBalanceTransactionDB', 'AddCashBalance', settlgnr.add_cash_generator(stop=participants))

    sc.add_step('ExecuteScript', 'Netting', execute_script_generator('Netting.sh'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationNetting', verify_ts_generator('SGXNetting', 'Completed'))
    sc.add_step('ExecuteScript', 'Processing', execute_script_generator('Processing.sh'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationProcessing', verify_ts_generator('SGXProcessing', 'Completed'))

    sc.push('matrix', view=True)
    sc.push('config')

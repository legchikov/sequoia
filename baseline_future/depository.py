from scenario_future import Scenario
from generators.common import execute_script_generator, verify_ts_generator, range_generator
import generators.depository as gnr


if __name__ == '__main__':

    # Baseline properties
    count = 1000

    # Scenario
    sc = Scenario('depository')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))
    schedulers = ('SGSProcessing', 'SGXNetting', 'SGXProcessing')

    sc.add_step('ExecuteScript', 'ResetTimeSchedules',
                execute_script_generator('turn_off.sh', parameters=schedulers))

    sc.add_static_step('InitStatic', False, Instr="INSTR_0@{gen('ggg')}")

    sc.add_step('SubmitSecurityDepositDB', 'SubmitSecurityDeposit', execute_script_generator(''))
    sc.add_step('VerifySecurityDeposit', 'VerifySecurityDeposit', execute_script_generator(''))

    sc.add_step('SubmitSecurityTransferDB', 'SubmitSecurityTransfer', range_generator(1, count+1))
    sc.add_step('VerifySecurityTransfer', 'VerifySecurityTransfer', range_generator(1, count+1))

    sc.add_step('ExecuteScript', 'SGSProcessing',
                execute_script_generator('turn_on.sh', parameters='SGSProcessing'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerifySGSProcessing',
                verify_ts_generator('SGSProcessing', 'Completed'))

    sc.add_step('VerifySecurityPositionsDepository', 'VerifyAddFreeBalance',
                gnr.verify_secpositions_generator(balance=count, timeout=10000))

    sc.push('matrix', view=True)
    sc.push('config')

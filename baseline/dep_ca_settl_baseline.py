from scenario_future import Scenario
from generators.common import execute_script_generator, verify_ts_generator, range_generator
import generators.settlement as settlgnr
import generators.depository as depgnr
import generators.corporate_action as cagnr

if __name__ == '__main__':

    # Baseline properties
    count_dep = 500
    count_ca = 11
    count_settl = 10
    participants = 1
    settlement_cycle = -3

    # Scenario
    sc = Scenario('dep-ca-settl')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))
    schedulers = ('TS_REC_CAPTURE', 'TS_ENT_COMP', 'TS_ISS_PAY_REMIND_SECU', 'TS_ISS_PAY_RECEIPT_SECU',
                  'TS_INV_PAY_DIST_SECU', 'SGSProcessing', 'SGXNetting', 'SGXProcessing')

    sc.add_step('ExecuteScript', 'ResetTimeSchedules',
                execute_script_generator('turn_off.sh', parameters=schedulers))

    sc.add_static_step('InitStatic', False, Instr="INSTR_015", Prefix="@{gen('ggg')}", ISIN=1000000,
                       SettlCycle=settlement_cycle)

    # Depository
    sc.add_step('SubmitSecurityDepositDB', 'SubmitSecurityDeposit', execute_script_generator())
    sc.add_step('VerifySecurityDeposit', 'VerifySecurityDeposit', execute_script_generator(timeout=10000))

    sc.add_step('SubmitSecurityTransferDB', 'SubmitSecurityTransfer', range_generator(count_dep))
    sc.add_step('VerifySecurityTransfer', 'VerifySecurityTransfer', range_generator(count_dep, timeout=1000))

    sc.add_step('ExecuteScript', 'SGSProcessing',
                execute_script_generator('turn_on.sh', parameters='SGSProcessing'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerifySGSProcessing',
                verify_ts_generator('SGSProcessing', 'Completed'))

    sc.add_step('VerifySecurityPositionsDepository', 'VerifyFreeBalance',
                depgnr.verify_secpositions_generator(balance=count_dep, timeout=10000))

    # Corporate Actions
    sc.add_step('AddSecurityPositionCA', 'CreateSecurityBalances', range_generator(count_ca))
    sc.add_step('AddRepeatingGroupCA', 'Create_CADiaryEntry', range_generator(count_ca))
    sc.add_step('CreateCADiaryEntry', 'Create_CADiaryEntry', range_generator(count_ca))
    sc.add_step('VerifyCADiaryEntry', 'VerifyCADiaryEntry', range_generator(count_ca, timeout=10000))
    sc.add_step('VerifyCAOption', 'VerifyCAOption', range_generator(count_ca, timeout=10000))

    sc.add_step('ExecuteScript', 'RC_Trigger', execute_script_generator('turn_on.sh', parameters='TS_REC_CAPTURE'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationRC', verify_ts_generator('TS_REC_CAPTURE', 'Completed'))

    sc.add_step('ExecuteScript', 'EC_Trigger', execute_script_generator('turn_on.sh', parameters='TS_ENT_COMP'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationEC', verify_ts_generator('TS_ENT_COMP', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlements', cagnr.verify_entitlements_generator(1, status='0'))

    sc.add_step('AddSecurityPositionCA2', 'AddSecurityBalance', range_generator(count_ca))

    sc.add_step('ExecuteScript', 'REMIND_Trigger',
                execute_script_generator('turn_on.sh', parameters='TS_ISS_PAY_REMIND_SECU'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationREMIND',
                verify_ts_generator('TS_ISS_PAY_REMIND_SECU', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlementsAfterREMIND',
                cagnr.verify_entitlements_generator(count_ca, status='0'))

    sc.add_step('ExecuteScript', 'PAY_REC_Trigger',
                execute_script_generator('turn_on.sh', parameters='TS_ISS_PAY_RECEIPT_SECU'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationPAY_REC',
                verify_ts_generator('TS_ISS_PAY_RECEIPT_SECU', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlementsAfterPAY_REC',
                cagnr.verify_entitlements_generator(count_ca, status='Pending Settlement'))

    sc.add_step('ExecuteScript', 'PAY_DIC_Trigger',
                execute_script_generator('turn_on.sh', parameters='TS_INV_PAY_DIST_SECU'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationPAY_DIC',
                verify_ts_generator('TS_INV_PAY_DIST_SECU', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlementsAfterPAY_DIC',
                cagnr.verify_entitlements_generator(count_ca, status='Complete', timeout=1000))

    # Clearing account transfer
    sc.add_step('SubmitSecurityTransferDBPool', 'SendPoolTransfer',
                depgnr.verify_secpositions_generator(balance=count_dep))
    sc.add_step('VerifySecurityPositionsPool', 'VerifyPoolTransfer',
                depgnr.verify_secpositions_generator(balance=count_dep, timeout=10000))

    # Settlement
    sc.add_step('SendBroadcast', 'SendDeal',
                settlgnr.send_broadcast_generator(stop=count_settl, qty=count_dep // count_settl,
                                                  commodity='@{Static.Instr.substring(7)}'))

    sc.add_step('VerifyAllocation', 'VerifyAllocation', settlgnr.verify_allocation_generator(end=count_settl))
    sc.add_step('SendSese023', 'SendSi', settlgnr.send_sese023_generator(end=count_settl,
                                                                         sellacc='@{V_pool_1.PositionAccountID}',
                                                                         buyacc='555000018486'))

    sc.add_step('SendCashBalanceTransactionDB', 'AddCashBalance', settlgnr.add_cash_generator(end=participants))

    sc.add_step('ExecuteScript', 'Netting', execute_script_generator('Netting.sh'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationNetting', verify_ts_generator('SGXNetting', 'Completed'))
    sc.add_step('ExecuteScript', 'Processing', execute_script_generator('Processing.sh'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationProcessing', verify_ts_generator('SGXProcessing', 'Completed'))

    sc.push('matrix', view=True)
    sc.push('config')

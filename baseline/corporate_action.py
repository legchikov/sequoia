from scenario_future import Scenario
from generators.common import execute_script_generator, verify_ts_generator, range_generator
import generators.corporate_action as cagnr


if __name__ == '__main__':

    # Baseline properties
    count = 50

    # Scenario
    sc = Scenario('corporate_action')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))

    schedulers = ('TS_REC_CAPTURE', 'TS_ENT_COMP', 'TS_ISS_PAY_REMIND_SECU',
                  'TS_ISS_PAY_RECEIPT_SECU', 'TS_INV_PAY_DIST_SECU')

    sc.add_step('ExecuteScript', 'ResetTimeSchedules',
                execute_script_generator('turn_off.sh', parameters=schedulers))

    # sc.add_static_step('InitStatic', False, Instr="INSTR_0@{(gen('ggg')%20)+1}")
    sc.add_static_step('InitStatic', False, Instr="INSTR_015")

    sc.add_step('AddSecurityPositionCA', 'CreateSecurityBalances', range_generator(count))
    sc.add_step('AddRepeatingGroupCA', 'Create_CADiaryEntry', range_generator(1))
    sc.add_step('CreateCADiaryEntry', 'Create_CADiaryEntry', range_generator(1))
    sc.add_step('VerifyCADiaryEntry', 'VerifyCADiaryEntry', range_generator(1, timeout=10000))
    sc.add_step('VerifyCAOption', 'VerifyCAOption', range_generator(1, timeout=10000))

    sc.add_step('ExecuteScript', 'RC_Trigger', execute_script_generator('turn_on.sh', parameters='TS_REC_CAPTURE'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationRC', verify_ts_generator('TS_REC_CAPTURE', 'Completed'))

    sc.add_step('ExecuteScript', 'EC_Trigger', execute_script_generator('turn_on.sh', parameters='TS_ENT_COMP'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationEC', verify_ts_generator('TS_ENT_COMP', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlements', cagnr.verify_entitlements_generator(count, status='0'))

    sc.add_step('AddSecurityPositionCA2', 'AddSecurityBalance', range_generator(1))

    sc.add_step('ExecuteScript', 'REMIND_Trigger',
                execute_script_generator('turn_on.sh', parameters='TS_ISS_PAY_REMIND_SECU'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationREMIND',
                verify_ts_generator('TS_ISS_PAY_REMIND_SECU', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlementsAfterREMIND',
                cagnr.verify_entitlements_generator(count, status='0'))

    sc.add_step('ExecuteScript', 'PAY_REC_Trigger',
                execute_script_generator('turn_on.sh', parameters='TS_ISS_PAY_RECEIPT_SECU'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationPAY_REC',
                verify_ts_generator('TS_ISS_PAY_RECEIPT_SECU', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlementsAfterPAY_REC',
                cagnr.verify_entitlements_generator(count, status='Pending Settlement'))

    sc.add_step('ExecuteScript', 'PAY_DIC_Trigger',
                execute_script_generator('turn_on.sh', parameters='TS_INV_PAY_DIST_SECU'))
    sc.add_step('VerifyTimeScheduleInfo', 'VerificationPAY_DIC',
                verify_ts_generator('TS_INV_PAY_DIST_SECU', 'Completed'))
    sc.add_step('VerifyCAEntitlements', 'VerifyCAEntitlementsAfterPAY_DIC',
                cagnr.verify_entitlements_generator(count, status='Complete'))

    sc.push('matrix', view=True)
    sc.push('config')

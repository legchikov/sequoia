from scenario_future import Scenario

from checksum import settlement_checksum
from generators.common import execute_script_generator, verify_ts_generator
import generators.settlement as gnr


if __name__ == '__main__':

    # Baseline properties
    count = 100
    participants = 1  # count of pairs
    instruments = 50
    settlement_cycle = -2

    # Scenario
    sc = Scenario('depository')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))
    schedulers = ('SGSProcessing', 'SGXNetting', 'SGXProcessing')

    sc.add_step('ExecuteScript', 'ResetTimeSchedules',
                execute_script_generator('turn_off.sh', parameters=schedulers))

    sc.add_static_step('InitStatic', False, Prefix="@{gen('ggg')}", ISIN=1000000, SettlCycle=settlement_cycle)

    sc.add_step('SendBroadcast', 'SendDeal', gnr.send_broadcast_generator(end=count), settlement_checksum)

from scenario_future import Scenario
from generators.common import execute_script_generator
from checksum import settlement_checksum
import generators.settlement as settlgnr


if __name__ == '__main__':

    # Baseline properties
    count = 100
    participants = 1  # count of pairs
    instruments = 50
    settlement_cycle = -3

    # Scenario
    sc = Scenario('omx')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))
    sc.add_static_step('InitStatic', False, Prefix="@{gen('ggg')}", ISIN=1000000, SettlCycle=settlement_cycle)

    sc.add_step('SendBroadcast', 'SendDeal', settlgnr.send_broadcast_generator(stop=count), settlement_checksum)
    sc.add_step('VerifyAllocation', 'VerifyAllocation', settlgnr.verify_allocation_generator(end=count))

    sc.push('matrix', view=True)
    sc.push('config')

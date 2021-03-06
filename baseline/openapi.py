from scenario_future import Scenario

from checksum import settlement_checksum
from generators.common import execute_script_generator
import generators.settlement as settlgnr


if __name__ == '__main__':

    # Baseline properties
    count = 100
    settlement_cycle = -3

    # Scenario
    sc = Scenario('openapi')

    sc.add_step('ExecuteScript', 'CleanSystem', execute_script_generator('Purge.sh'))
    sc.add_static_step('InitStatic', False, Prefix="@{gen('ggg')}", ISIN=1000000, SettlCycle=settlement_cycle)
    sc.add_step('SendBroadcast', 'SendDeal', settlgnr.send_broadcast_generator(stop=count), settlement_checksum)
    sc.add_step('VerifyAllocation', 'VerifyAllocation', settlgnr.verify_allocation_generator(end=count))
    sc.add_step('SendSese023', 'SendSi', settlgnr.send_sese023_generator(stop=count))

    sc.push('matrix', view=True)
    sc.push('config')

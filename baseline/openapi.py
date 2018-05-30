from scenario import render, sc, push
from action import get_action
from generators.common import execute_script_generator, static_generator
import generators.settlement as gnr


if __name__ == '__main__':

    # Baseline properties
    name = 'openapi'
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

    # Scenario
    sc(exescript, 'CleanSystem', execute_script_generator('Purge.sh'))

    sc(static, 'Static', static_generator({'Prefix': "@{gen('ggg')}",
                                           'ISIN': 1000000,
                                           'SettlCycle': settlement_cycle}))

    sc(send_broadcast, 'SendDeal', gnr.send_broadcast_generator(end=count))
    sc(verify_allocation, 'VerifyAllocation', gnr.verify_allocation_generator(end=count))
    sc(send023, 'SendSi', gnr.send_sese023_generator(end=count))

    # Matrix
    matrix = render(sc, 'matrix')
    scheduler_config = render(sc, 'scheduler_config')

    # Write to file
    push(name, matrix, 'matrix')
    push(name, scheduler_config, 'scheduler_config')

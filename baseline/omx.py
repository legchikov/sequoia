from scenario import render, sc
from generator import send_broadcast_generator, verify_allocation_generator,  \
    execute_script_generator, static_generator

from action import get_action


if __name__ == '__main__':

    # Count of messages
    count = 100
    participants = 1  # count of pairs
    instruments = 50
    settlement_cycle = -3

    # Construct the action
    exescript = get_action('ExecuteScript')
    static = get_action('SetStatic')

    send_broadcast = get_action('SendBroadcast')
    verify_allocation = get_action('VerifyAllocation')

    # Scenario
    sc(exescript, 'CleanSystem', execute_script_generator('CleanSystem', 'Purge.sh'))

    sc(static, 'Static', static_generator({'Prefix': "@{gen('ggg')}",
                                 'ISIN': 1000000,
                                 'SettlCycle': settlement_cycle}))

    sc(send_broadcast, 'SendDeal', send_broadcast_generator(end=count))
    sc(verify_allocation, 'VerifyAllocation', verify_allocation_generator(end=count))

    # Matrix
    matrix = render(sc)

    # Output
    f = open(f'output\omx_{count}.csv', 'w')

    for line in matrix:
        f.write(line + '\n')
        print(line)
    f.close()
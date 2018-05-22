from scenario import render, sc
from generator import send_broadcast_generator, \
    verify_allocation_generator, send_sese023_generator, execute_script_generator, static_generator
from action import get_action


if __name__ == '__main__':

    # Construct the action
    purge = get_action('ExecuteScript')
    reset_ts = get_action('ExecuteScript')
    static = get_action('SetStatic')
    send_broadcast = get_action('SendBroadcast')
    verify_allocation = get_action('VerifyAllocation')
    send023 = get_action('SendSese023')
    start_netting = get_action('ExecuteScript')
    start_processing = get_action('ExecuteScript')

    # Scenario
    sc(purge, execute_script_generator('CleanSystem', 'Purge.sh'))
    sc(reset_ts, execute_script_generator('ResetTimeSchedules', 'Turnoff.sh'))
    sc(static, static_generator(1000000))
    sc(send_broadcast, send_broadcast_generator(start=0, end=1000))
    sc(verify_allocation, verify_allocation_generator(start=0, end=1000))
    sc(send023, send_sese023_generator(start=0, end=1000))
    sc(start_netting, execute_script_generator('Netting', 'Netting.sh'))
    sc(start_processing, execute_script_generator('Processing', 'Processing.sh'))

    # Matrix
    matrix = render(sc)

    # Output
    f = open(r'output\settlement_retail_1000.csv', 'w')

    for line in matrix:
        f.write(line + '\n')
        print(line)
    f.close()

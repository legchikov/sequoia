from scenario import render
from scenario import sc
from generator import transfer_generator, range_generator
from action import get_action


if __name__ == '__main__':

    # Actions
    submit_security_transfer_action = get_action('submit_security_transfer')
    send_pricing_update = get_action('send_pricing_update')

    # Scenario
    sc(
        submit_security_transfer_action,
        transfer_generator(r'C:\Users\dmitriy.legchikov1\Downloads\Baseline_generator\account-clear.csv')
    )

    sc(
        send_pricing_update,
        range_generator(start=0, end=10, step=1)
    )

    # Matrix
    matrix = render(sc)

    # Output
    for line in matrix:
        print(line)

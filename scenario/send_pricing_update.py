from scenario import render, sc
from generator import range_generator
from action import get_action


if __name__ == '__main__':

    # Construct the action
    send_pricing_update = get_action('send_pricing_update')

    # Scenario
    sc(send_pricing_update, range_generator(start=0, end=10, step=1))
    # scenario(send_pricing_update, range_generator(start=0, end=10, step=1))

    # Matrix
    matrix = render(sc)

    # Output
    for line in matrix:
        print(line)



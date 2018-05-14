from scenario import render, sc
from generator import send_deal_generator
from action import get_action


if __name__ == '__main__':

    # Actions
    send_deal_action = get_action('send_deal')

    # Scenario
    sc(
        send_deal_action,
        send_deal_generator(start=1, end=11, step=1)
    )

    # Matrix
    matrix = render(sc)

    # Output
    for line in matrix:
        print(line)



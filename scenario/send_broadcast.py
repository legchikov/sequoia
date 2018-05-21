from scenario import render, sc
from generator import send_broadcast_generator, verify_allocation_generator, send_sese023_generator
from action import get_action


if __name__ == '__main__':

    # Construct the action
    send_broadcast = get_action('SendBroadcast')
    verify_allocation = get_action('VerifyAllocation')
    send023 = get_action('SendSese023')

    # Scenario
    sc(send_broadcast, send_broadcast_generator(start=0, end=10, step=1))
    sc(verify_allocation, verify_allocation_generator(start=0, end=10, step=1))
    sc(send023, send_sese023_generator(start=0, end=10, step=1))

    # Matrix
    matrix = render(sc)

    static = '''#id,#GlobalStep,#Action,#Execute,#TestCase,#timeout,#Comment,#ScriptDirectory,#ScriptName,#Parameters,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
CS,CleanSystem,ExecuteScript,TRUE,,0,,./,Purge.sh,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#id,#GlobalStep,#Action,#Execute,#TestCase,#timeout,#Comment,#ScriptDirectory,#ScriptName,#Parameters,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
R_TS,ResetTimeSchedules,ExecuteScript,TRUE,,0,,./,Turnoff.sh,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#id,#GlobalStep,#Action,#Execute,#TestCase,#timeout,#Comment,#Prefix,#ISIN,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Static,Static,SetStatic,TRUE,,0,,@{gen('ggg')},1000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
'''

    # Output
    f = open(r'C:\Users\dmitriy.legchikov1\Documents\Legchikov\Sequoia\output\send_broadcast.csv', 'w')
    f.write(static)
    for line in matrix:
        f.write(line)
        f.write('\n')
        print(line)
    f.close()

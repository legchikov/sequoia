import os
import config
from collections import namedtuple


Action = namedtuple('Action', 'name header template')


def get_action(action_name):
    try:
        with open(os.path.join(config.PATH_ACTIONS, action_name + '.cfg')) as file:
            header = []
            template = []

            for line in file:
                line = _clean_comments(line)
                if line.startswith('@Params'):
                    break
                h, t = line.split(':', 1)
                header.append(h.strip())
                template.append(t.strip())

            header_str = ','.join(header)
            template_str = ','.join(template)
            return Action(action_name, header_str, template_str)
    except FileNotFoundError as e:
        print('[ERROR]: Config file "{}" has not found.'.format(e.filename))
        return


def make_action(action_name):
    header = input('Enter header:\n').replace('"', '').split(',')
    message = input('Enter message:\n')
    message = _screening(message)
    message = _split(message)

    with open('actions/{}.cfg'.format(action_name), 'w') as file:
        max_length = max(len(h) for h in header)
        for p in zip(header, message):
            if len(p[0]) == 0 and len(p[1]) == 0:
                pass
            else:
                file.write('{pair[0]:{max}} : {pair[1]}\n'.format(pair=p, max=max_length))

        print('{}.cfg was created.'.format(action_name))


def make_action_json(action_name):
    header = input('Enter header:\n').replace('"', '').split(',')
    message = input('Enter message:\n')
    message = _screening(message)
    message = _split(message)
    jsonmessage = dict()

    import json
    import yaml
    with open('actions_json/{}.yaml'.format(action_name), 'w') as file:
        max_length = max(len(h) for h in header)
        for p in zip(header, message):
            if len(p[0]) == 0 and len(p[1]) == 0:
                pass
            else:
                jsonmessage[p[0]] = str(p[1])

        # json.dump(jsonmessage, file, indent=4)
        yaml.dump(jsonmessage, file, default_flow_style=False)
        # file.write(simplejson.dumps(simplejson.loads(jsonmessage), indent=4, sort_keys=True))

        print('{}.json was created.'.format(action_name))


def make_from_file(action_name, file_name):
    header = ''
    message = []
    with open(file_name) as infile:
        with open('actions/{}.cfg'.format(action_name), 'w') as outfile:
            for line in infile:
                if line.startswith('#'):
                    header = line.replace('"', '').replace('\n', '').split(',')
                else:
                    if header:
                        message = _screening(line)
                        message = _split(message)
                        break
            max_length = max(len(h) for h in header)
            for p in zip(header, message):
                if len(p[0]) == 0 and len(p[1]) == 0:
                    pass
                else:
                    outfile.write('{pair[0]:{max}} : {pair[1]}\n'.format(pair=p, max=max_length))

            print('{}.cfg was created.'.format(action_name))


def make_from_all_file(filename):
    start_action = True
    header = ''
    message = ''

    with open(filename) as infile:
        for line in infile:
            line = line.replace('\n', '')
            if line.startswith(','):
                pass
            elif line.startswith('#'):
                start_action = True
                header = line
            elif start_action:
                message = line
            else:
                header = ''
                message = ''

            if header and message:
                lst = message.split(',')
                action_name = str(lst[2])

                from os import listdir
                from os.path import isfile, join
                onlyfiles = [f for f in listdir(r'C:\Users\dmitry.legchikov\Documents\GitHub\sequoia\actions') if isfile(join(r'C:\Users\dmitry.legchikov\Documents\GitHub\sequoia\actions', f))]
                # print(header)
                # print(message)
                # print(onlyfiles)
                if action_name + '.cfg' not in onlyfiles:
                    _make_action(action_name, header, message)
                    # print('{} was created'.format(action_name))
                # else:
                #     print('fail')


def _make_action(action_name, head, mess):
    header = head.replace('"', '').split(',')
    message = mess
    message = _screening(message)
    message = _split(message)

    with open('actions/{}.cfg'.format(action_name), 'w') as file:
        max_length = max(len(h) for h in header)
        for p in zip(header, message):
            if len(p[0]) == 0 and len(p[1]) == 0:
                pass
            else:
                file.write('{pair[0]:{max}} : {pair[1]}\n'.format(pair=p, max=max_length))

        print('{}.cfg was created.'.format(action_name))


def _screening(s):
    """Screening '{' and '}' so that the format() function will work correctly with parameters"""
    return s.replace('{', '{{').replace('}', '}}')


def _clean_comments(s):
    """Remove comments"""
    sep = '//'
    rest = s.split(sep)[0]
    return rest


def _split(s):
    """
    Split by comma but with ignoring commas which inner in curly brackets

    "Buy_2400001","@{format(time(-2),'yyyyMMdd')}","36000"
    ->
    ["Buy_2400001", "@{format(time(-2),'yyyyMMdd')}", "36000"]
    """

    parts = []
    bracket_level = 0
    current = []
    for c in (s + ","):
        if c == "," and bracket_level == 0:
            parts.append("".join(current))
            current = []
        else:
            if c == "{":
                bracket_level += 1
            elif c == "}":
                bracket_level -= 1
            current.append(c)
    return parts


if __name__ == '__main__':
    # :TODO: interface via ParseArguments
    # mode = sys.argv[0]
    mode = 'make'
    # mode = 'makejson'
    # mode = 'makeall'
    # mode = 'read'
    # mode = 'make_from_file'
    action = input('Enter action:\n')

    if mode == 'read':
        get_action(action)
    elif mode == 'make':
        make_action(action)
    elif mode == 'make_from_file':
        filename = input('Enter full the file path:\n')
        make_from_file(action, filename)
    elif mode == 'makeall':
        make_from_all_file(r'C:\Users\dmitry.legchikov\Documents\GitHub\sequoia\matrixes\CA_bl13_for_20_instr_without_purge.csv')
    elif mode == 'makejson':
        make_action_json(action)
    else:
        print('incorrect mode')

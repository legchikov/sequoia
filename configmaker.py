import os
import config
import action


def read(action_name):
    try:
        with open(os.path.join(config.PATH_ACTIONS, action_name)) as file:
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
            return action.Action(header_str, template_str)
    except FileNotFoundError as e:
        print('[ERROR]: Config file "{}" has not found.'.format(e.filename))
        return


def make(action_name):
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
    # mode = sys.argv[0]
    mode = 'make'
    # mode = 'read'
    # mode = 'make_from_file'
    action = input('Enter action:\n')

    if mode == 'read':
        read(action)
    elif mode == 'make':
        make(action)
    elif mode == 'make_from_file':
        filename = input('Enter full the file path:\n')
        make_from_file(action, filename)
    else:
        print('incorrect mode')


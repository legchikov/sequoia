import yaml
from collections import OrderedDict, namedtuple

Action = namedtuple('Action', 'name header template')


def load(name):
    header_str = ''
    template_str = ''
    for h, t in yaml.load(open('actions_future/header.yaml')).items():
        header_str += h + ','
        template_str += t + ','
    for h, t in yaml.load(open('actions_future/{}.yaml'.format(name))).items():
        header_str += h + ','
        template_str += t + ','

    return Action(name, header_str, template_str)


def make(name, header, template):
    header_cleaned = header.replace('"', '')
    template_cleaned = screen(template)

    header_lst = header_cleaned.split(',')
    template_lst = split(template_cleaned)

    yamldata = OrderedDict()

    with open('actions_future/{}.yaml'.format(name), 'w') as file:
        for p in zip(header_lst, template_lst):
            if len(p[0]) == 0 and len(p[1]) == 0:
                pass
            else:
                yamldata[p[0]] = str(p[1])

        ordered_dump(yamldata, stream=file, Dumper=yaml.SafeDumper, default_flow_style=False)


def split(s):
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


def screen(s):
    """Screening '{' and '}' so that the format() function will work correctly with parameters"""
    return s.replace('{', '{{').replace('}', '}}')


def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


name = input('Enter name:\n')
header = input('Enter header:\n')
template = input('Enter template:\n')

make(name, header, template)


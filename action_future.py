import yaml
import collections
import yamlordereddictloader


class Action:
    def __init__(self, name, header, template):
        self.name = name
        self.header = header
        self.template = template

    def make(self):
        header_cleaned = self.header.replace('"', '')
        template_cleaned = self.screen(self.template)

        header_lst = header_cleaned.split(',')
        template_lst = self.split(template_cleaned)

        # yamlconfig = collections.OrderedDict()
        yamlconfig = dict()

        with open('actions_future/{}.yaml'.format(self.name), 'w') as file:
            for p in zip(header_lst, template_lst):
                if len(p[0]) == 0 and len(p[1]) == 0:
                    pass
                else:
                    yamlconfig[p[0]] = str(p[1])

            yaml.dump(yamlconfig, file, default_flow_style=False, Loader=yamlordereddictloader.Loader)


    def split(self, s):
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

    def screen(self, s):
        """Screening '{' and '}' so that the format() function will work correctly with parameters"""
        return s.replace('{', '{{').replace('}', '}}')



name = input('Enter name:\n')
header = input('Enter header:\n')
template = input('Enter template:\n')
a = Action(name, header, template)
a.make()

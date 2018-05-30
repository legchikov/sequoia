SCHEDULER_HEADER = 'Global step,Step kind,Start at,Start at type,Parameter,Ask for continue,Ask if failed,Execute,Comment'


def make_scheduler_config(step, ask=1, execute=1):
    return '{Step},Default,,End of previous step,,{Ask},0,{Execute},'.format(Step=step, Ask=ask, Execute=execute)

""" Generic Utilities module """


def create_select_data(it, **kwargs):
    if not isinstance(it, (list, tuple)):
        it = [it]

    ret = []
    for i in it:
        if isinstance(i, dict):
            name = i.get('name')
            value = i.get('value')
        else:
            try:
                if kwargs.get('exclude_types'):
                    types_str = ''
                else:
                    types_str = f' - ({", ".join(i.type())})' if i.type() else ''
                name = f'{i.name()}{types_str}'
                value = i.id()
            except AttributeError:
                name = str(i)
                value = name.lower().replace(' ', '-')
        ret.append({'name': name, 'value': value})
    return ret

def update_selected(options, value, selected=True):
    for o in options:
        if o['value'] != value:
            continue
        o['selected'] = selected
        break

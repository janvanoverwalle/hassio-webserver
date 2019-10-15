""" Generic Utilities module """


def create_select_data(it):
    if not isinstance(it, (list, tuple)):
        it = [it]

    ret = []
    for i in it:
        if isinstance(i, dict):
            name = i.get('name')
            value = i.get('value')
        else:
            try:
                types_str = f' - ({", ".join(i.type())})' if i.type() else ''
                name = f'{i.name()}{types_str}'
                value = i.id()
            except AttributeError:
                name = str(i)
                value = name.lower().replace(' ', '-')
        ret.append({'name': name, 'value': value})
    return ret


def highlight_conditions(str):
    return str.replace('[', '<i>[').replace(']', ']</i>')

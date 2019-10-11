""" Generic Utilities module """


def create_select_data(it):
    ret = []
    for i in it:
        try:
            name = f'{i.name()} - ({", ".join(i.type())})'
            value = i.id()
        except AttributeError:
            name = str(i)
            value = name.lower().replace(' ', '-')
        ret.append({'name': name, 'value': value})
    return ret

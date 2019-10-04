""" Generic Utilities module """


def create_select_data(it):
    ret = []
    for i in it:
        ret.append({'name': str(i), 'value': str(i).lower().replace(' ', '-')})
    return ret

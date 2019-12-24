import json


class Celestial(object):
    def __init__(self, celestial_file, **kwargs):
        self.__celestial_file = celestial_file
        with open(self.__celestial_file) as json_file:
            self.__json_data = json.load(json_file)
        self.auto_save = kwargs.get('auto_save', True)

    def save(self, *args, **kwargs):
        if args:
            filename = args[0]
        else:
            filename = kwargs.get('as', self.__celestial_file)
        with open(filename, 'w') as json_file:
            json.dump(self.__json_data, json_file, indent=2)

    def get_celestial(self, date):
        if not date:
            return self.__json_data['celestial']
        return self.__json_data['celestial'].get(str(date), [])

    def set_celestial(self, date, *args):
        if not weather:
            del self.__json_data['celestial'][str(date)]
        else:
            data = args[0] if isinstance(weather[0], (list, tuple)) else args
            self.__json_data['celestial'][str(date)] = list(data)
        if self.auto_save:
            self.save()

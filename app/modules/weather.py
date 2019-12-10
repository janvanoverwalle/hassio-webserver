import json


class Weather(object):
    def __init__(self, weather_file, **kwargs):
        self.__weather_file = weather_file
        with open(self.__weather_file) as json_file:
            self.__json_data = json.load(json_file)
        self.auto_save = kwargs.get('auto_save', True)

    def save(self, *args, **kwargs):
        if args:
            filename = args[0]
        else:
            filename = kwargs.get('as', self.__weather_file)
        with open(filename, 'w') as json_file:
            json.dump(self.__json_data, json_file, indent=2)

    def get_description(self, tag):
        return self.__json_data['descriptions'].get(tag)

    def set_description(self, tag, description):
        self.__json_data['descriptions'][tag] = description
        if self.auto_save:
            self.save()

    def get_weather(self, date):
        if not date:
            return self.__json_data['weather']
        return self.__json_data['weather'].get(str(date), [])

    def set_weather(self, date, *args):
        if not weather:
            del self.__json_data[str(date)]
        else:
            data = args[0] if isinstance(weather[0], (list, tuple)) else args
            self.__json_data[str(date)] = list(data)
        if self.auto_save:
            self.save()

    def get_weather_descriptions(self, date):
        weather = self.get_weather(date)
        return [self.get_description(w) for w in weather]

    def to_json(self, date=None):
        return self.get_weather(date)

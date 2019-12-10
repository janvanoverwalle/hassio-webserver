import datetime
import json
import re
from pathlib import Path
from .date import DonjonDate, ElderanDate
from ..weather import Weather


class DonjonCalendar(object):
    def __init__(self, cfg_path, **kwargs):
        self.__cfg_path = cfg_path
        self.__calendar_file = self.__cfg_path/'calendar.json'
        with open(self.__calendar_file) as json_file:
            self.__json_data = json.load(json_file)
        weather_file = self.__cfg_path/'weather.json'
        self.weather = Weather(weather_file) if weather_file.exists() else None
        self.__date_class = kwargs.get('date_class', DonjonDate)
        self.auto_save = kwargs.get('auto_save', True)

    @property
    def date_class(self):
        return self.__date_class

    def __str__(self):
        return str(self.__json_data)

    def save(self, *args, **kwargs):
        if args:
            filename = args[0]
        else:
            filename = kwargs.get('as', self.__calendar_file)
        with open(filename, 'w') as json_file:
            json.dump(self.__json_data, json_file, indent=2)

    def _update_list(self, m_list, v_list):
        while len(m_list) > len(values):
            del m_list[-1]
        while len(m_list) < len(values):
            m_list.append(None)

        for index in range(len(m_list)):
            m_list[index] = values[index]

    def _update_dict(self, m_dict, v_dict):
        for k in list(m_dict.keys()):
            if k not in v_dict:
                del m_dict[k]
        for k, v in v_dict.items():
            m_dict[k] = v

    def _get_element(self, m_iter, m_index=None):
        if m_index is None:
            return m_iter
        elif isinstance(m_iter, dict):
            return m_iter.get(m_index)
        elif isinstance(m_index, (int, float)):
            return m_iter[int(m_index)]
        else:
            try:
                return m_iter.index(str(m_index))
            except ValueError:
                pass
        return None

    def _set_element(self, m_iter, *args, **kwargs):
        if not args and not kwargs:
            return

        if isinstance(args[0], list):
            self._update_list(m_iter, args[0])
            return

        if isinstance(args[0], dict):
            self._update_dict(m_iter, args[0])
            return

        index = kwargs.get('index', kwargs.get('key', args[0]))
        if isinstance(m_iter, list) and not isinstance(index, int):
            index = m_iter.index(str(index))

        value = None
        has_value = False
        if 'value' in kwargs:
            value = kwargs['value']
            has_value = True
        if not has_value and len(args) > 1:
            value = args[1]
            has_value = True
        if not has_value:
            return
        m_iter[index] = value

    ### Custom Properties ###

    @property
    def current_date(self):
        return self.__json_data.get('current_date', self.year)

    @current_date.setter
    def current_date(self, value):
        self.__json_data['current_date'] = str(value)
        if self.auto_save:
            self.save()

    @property
    def campaign_start(self):
        if not hasattr(self, '__campaign_start'):
            date = self.__json_data.get('campaign_start', f'{self.year}-1-1')
            self.__campaign_start = self.__date_class.from_iso_format(date)
        return self.__campaign_start

    @campaign_start.setter
    def campaign_start(self, value):
        if isinstance(value, self.__date_class):
            self.__campaign_start = value
        else:
            self.__campaign_start = self.__date_class.from_iso_format(value)
        self.__json_data['campaign_start'] = str(self.__campaign_start)
        if self.auto_save:
            self.save()

    ### Properties ###

    @property
    def year(self):
        return self.__json_data['year']

    def _set_year(self, value):
        self.__json_data['year'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def days_in_year(self):
        return self.__json_data['year_len']

    def _set_days_in_year(self, value):
        self.__json_data['year_len'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def months_in_year(self):
        return self.__json_data['n_months']

    def _set_months_in_year(self, value):
        self.__json_data['n_months'] = int(value)
        if self.auto_save:
            self.save()

    def get_months(self, month=None):
        return self._get_element(self.__json_data['months'], month)

    def _set_months(self, *args, **kwargs):
        self._set_element(self.__json_data['months'], *args, **kwargs)
        self.months_in_year = len(self.__json_data['months'])  # autosaves

    def get_days_in_months(self, month=None):
        if isinstance(month, int):
            month = self.get_months(month)
        return self._get_element(self.__json_data['month_len'], month)

    def set_days_in_months(self, *args, **kwargs):
        self._set_element(self.__json_data['month_len'], *args, **kwargs)
        if self.auto_save:
            self.save()

    @property
    def days_in_week(self):
        return self.__json_data['week_len']

    @days_in_week.setter
    def days_in_week(self, value):
        self.__json_data['week_len'] = int(value)
        if self.auto_save:
            self.save()

    def get_weekdays(self, weekday=None):
        return self._get_element(self.__json_data['weekdays'], weekday)

    def set_weekdays(self, *args, **kwargs):
        self._set_element(self.__json_data['weekdays'], *args, **kwargs)
        self.days_in_week = len(self.__json_data['weekdays'])  # autosaves

    @property
    def first_weekday(self):
        return self.__json_data['first_day']

    @first_weekday.setter
    def first_weekday(self, value):
        self.__json_data['first_day'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def number_of_moons(self):
        return self.__json_data['n_moons']

    @number_of_moons.setter
    def number_of_moons(self, value):
        self.__json_data['n_moons'] = int(value)
        if self.auto_save:
            self.save()

    def get_moons(self, moon=None):
        return self._get_element(self.__json_data['moons'], moon)

    def set_moons(self, *args, **kwargs):
        self._set_element(self.__json_data['moons'], *args, **kwargs)
        self.number_of_moons = len(self.__json_data['moons'])  # autosaves

    def get_lunar_cycles(self, moon=None):
        return self._get_element(self.__json_data['lunar_cyc'], moon)

    def set_lunar_cycles(self, *args, **kwargs):
        self._set_element(self.__json_data['lunar_cyc'], *args, **kwargs)
        if self.auto_save:
            self.save()

    def get_lunar_shifts(self, moon=None):
        return self._get_element(self.__json_data['lunar_shf'], moon)

    def set_lunar_shifts(self, *args, **kwargs):
        self._set_element(self.__json_data['lunar_shf'], *args, **kwargs)
        if self.auto_save:
            self.save()

    def get_notes(self, date=None, **kwargs):
        notes = self.__json_data['notes']

        if not date and not kwargs:
            return notes

        if date:
            if not isinstance(date, DonjonDate):
                date = self.__date_class.from_iso_format(str(date))
            return notes.get(date.donjon_format())

        if not kwargs:
            return None

        year = kwargs.get('year', kwargs.get('y'))
        year = int(year) if year else year
        month = kwargs.get('month', kwargs.get('m'))
        month = int(month) if month else month
        day = kwargs.get('day', kwargs.get('d'))
        day = int(day) if day else day

        if year and month and day:
            return notes.get(f'{year}-{month}-{day}')
        if year:
            notes = {k: v for k, v in notes.items() if str(year) == k.split('-')[0]}
        if month:
            notes = {k: v for k, v in notes.items() if str(month) == k.split('-')[1]}
        if day:
            notes = {k: v for k, v in notes.items() if str(day) == k.split('-')[2]}
        return notes if notes else None

    def set_notes(self, *args, **kwargs):
        self._set_element(self.__json_data['notes'], *args, **kwargs)
        if self.auto_save:
            self.save()

    ### Utilities ###

    @property
    def day_of_year(self):
        days = sum([self.get_days_in_months(i) for i in range(self.today.month-1)])
        return days + self.today.day

    @property
    def today(self):
        if not hasattr(self, '__today'):
            self.__today = self.__date_class.today()
        return self.__today

    @today.setter
    def today(self, value):
        if isinstance(value, self.__date_class):
            self.__today = value
        else:
            self.__today = self.__date_class.from_iso_format(value)
        self.__json_data['current_date'] = str(self.__today)
        self.__json_data['era'] = self.__today.era
        if self.auto_save:
            self.save()

    def days_before(self, date=None):
        if not date:
            date = self.today
        elif not isinstance(date, self.__date_class):
            date = self.__date_class.from_iso_format(str(date))
        return date.to_ordinal()

    def days_since(self, date=None):
        if not date:
            date = self.__date_class.from_iso_format('1-1-1')
        elif not isinstance(date, self.__date_class):
            date = self.__date_class.from_iso_format(str(date))
        return self.today - date

    def weekday(self, date=None):
        if not date:
            date = self.__date_class.from_iso_format('1-1-1')
        elif not isinstance(date, self.__date_class):
            date = self.__date_class.from_iso_format(str(date))

        y1 = self.__date_class.from_iso_format(f'{self.year}-1-1')
        days_since = self.days_before(date) - self.days_before(y1)
        days_since += self.first_weekday
        weekday = days_since % self.days_in_week
        return self.get_weekdays(weekday)

    def _to_json(self, year, month=None, day=None):
        if isinstance(year, DonjonDate):
            date = year
            day = date.day
            month = date.month
            year = date.year
        else:
            date = None
        # TODO: Need all days in year/month, not just those with notes
        notes = self.get_notes(year=year, month=month, day=day)
        if date or not notes:
            json_data = {str(date): {'notes': notes}}
        else:
            json_data = {k:{'notes': v} for k,v in notes.items()}
        for k, v in json_data.items():
            v['weather'] = self.weather.get_weather(k)
            v['weather_descriptions'] = self.weather.get_weather_descriptions(k)
        return json.dumps(json_data if json_data else {})

    def to_json_day(self, date=None):
        if not date:
            date = self.today
        return self._to_json(date)

    def to_json_month(self, date=None):
        if not date:
            date = self.today
        return self._to_json(year=date.year, month=date.month)

    def to_json_year(self, date=None):
        if not date:
            date = self.today
        return self._to_json(year=date.year)


class ElderanCalendar(DonjonCalendar):
    def __init__(self):
        path = Path(__file__).parents[2]/'data'/'elderan'
        super().__init__(path, date_class=ElderanDate)

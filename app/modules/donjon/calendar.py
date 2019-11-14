import datetime
import json
import re
from pathlib import Path


class DonjonCalendar(object):
    def __init__(self, calendar_file, auto_save=True):
        self._calendar_file = calendar_file
        with open(self._calendar_file) as json_file:
            self._json_data = json.load(json_file)
        self.auto_save = auto_save

    def __str__(self):
        return str(self._json_data)

    def save(self, *args, **kwargs):
        if args:
            filename = args[0]
        else:
            filename = kwargs.get('as', self._calendar_file)
        with open(filename, 'w') as json_file:
            json.dump(self._json_data, json_file, indent=2)

    def _parse_date_parameters(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            date = list(map(int, re.split(r'\D+', str(args[0]))))
            year = int(date[0])
            month = int(date[1]) if len(date) > 1 else 0
            day = int(date[2]) if len(date) > 2 else 0
        else:
            year = int(kwargs.get('year', kwargs.get('y', args[0])))
            month = int(kwargs.get('month', kwargs.get('m', args[1] if len(args) > 1 else 0)))
            day = int(kwargs.get('day', kwargs.get('d', args[2] if len(args) > 2 else 0)))
        return year, month, day

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
    def current_year(self):
        return self._json_data.get('current_year', self.year)

    @current_year.setter
    def current_year(self, value):
        self._json_data['current_year'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def month_of_year(self):
        return self._json_data.get('month_of_year', 1)

    @month_of_year.setter
    def month_of_year(self, value):
        self._json_data['month_of_year'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def day_of_month(self):
        return self._json_data.get('day_of_month', 1)

    @day_of_month.setter
    def day_of_month(self, value):
        self._json_data['day_of_month'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def campaign_start(self):
        return self._json_data.get('campaign_start', f'{self.year}-1-1')

    @campaign_start.setter
    def campaign_start(self, value):
        self._json_data['campaign_start'] = str(value)
        if self.auto_save:
            self.save()

    ### Properties ###

    @property
    def year(self):
        return self._json_data['year']

    def _set_year(self, value):
        self._json_data['year'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def days_in_year(self):
        return self._json_data['year_len']

    def _set_days_in_year(self, value):
        self._json_data['year_len'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def months_in_year(self):
        return self._json_data['n_months']

    def _set_months_in_year(self, value):
        self._json_data['n_months'] = int(value)
        if self.auto_save:
            self.save()

    def get_months(self, month=None):
        return self._get_element(self._json_data['months'], month)

    def _set_months(self, *args, **kwargs):
        self._set_element(self._json_data['months'], *args, **kwargs)
        self.months_in_year = len(self._json_data['months'])  # autosaves

    def get_days_in_months(self, month=None):
        if isinstance(month, int):
            month = self.get_months(month)
        return self._get_element(self._json_data['month_len'], month)

    def set_days_in_months(self, *args, **kwargs):
        self._set_element(self._json_data['month_len'], *args, **kwargs)
        if self.auto_save:
            self.save()

    @property
    def days_in_week(self):
        return self._json_data['week_len']

    @days_in_week.setter
    def days_in_week(self, value):
        self._json_data['week_len'] = int(value)
        if self.auto_save:
            self.save()

    def get_weekdays(self, weekday=None):
        return self._get_element(self._json_data['weekdays'], weekday)

    def set_weekdays(self, *args, **kwargs):
        self._set_element(self._json_data['weekdays'], *args, **kwargs)
        self.days_in_week = len(self._json_data['weekdays'])  # autosaves

    @property
    def first_weekday(self):
        return self._json_data['first_day']

    @first_weekday.setter
    def first_weekday(self, value):
        self._json_data['first_day'] = int(value)
        if self.auto_save:
            self.save()

    @property
    def number_of_moons(self):
        return self._json_data['n_moons']

    @number_of_moons.setter
    def number_of_moons(self, value):
        self._json_data['n_moons'] = int(value)
        if self.auto_save:
            self.save()

    def get_moons(self, moon=None):
        return self._get_element(self._json_data['moons'], moon)

    def set_moons(self, *args, **kwargs):
        self._set_element(self._json_data['moons'], *args, **kwargs)
        self.number_of_moons = len(self._json_data['moons'])  # autosaves

    def get_lunar_cycles(self, moon=None):
        return self._get_element(self._json_data['lunar_cyc'], moon)

    def set_lunar_cycles(self, *args, **kwargs):
        self._set_element(self._json_data['lunar_cyc'], *args, **kwargs)
        if self.auto_save:
            self.save()

    def get_lunar_shifts(self, moon=None):
        return self._get_element(self._json_data['lunar_shf'], moon)

    def set_lunar_shifts(self, *args, **kwargs):
        self._set_element(self._json_data['lunar_shf'], *args, **kwargs)
        if self.auto_save:
            self.save()

    def get_notes(self, *args, **kwargs):
        notes = self._json_data['notes']
        if not args and not kwargs:
            return notes
        if args:
            datestamp = list(map(int, re.split(r'\D+', args[0])))
            return notes['-'.join(list(map(str, datestamp)))]
        if kwargs:
            datestamp = kwargs.get('date', kwargs.get('datestamp'))
            if datestamp:
                datestamp = list(map(int, re.split(r'\D+', datestamp)))
                return notes['-'.join(list(map(str, datestamp)))]

            year = int(kwargs.get('year', kwargs.get('y', 0)))
            month = int(kwargs.get('month', kwargs.get('m', 0)))
            day = int(kwargs.get('day', kwargs.get('d', 0)))
            if year and month and day:
                return notes[f'{year}-{month}-{day}']
            if year:
                notes = {k: v for k, v in notes.items() if str(year) == k.split('-')[0]}
            if month:
                notes = {k: v for k, v in notes.items() if str(month) == k.split('-')[1]}
            if day:
                notes = {k: v for k, v in notes.items() if str(day) == k.split('-')[2]}
            return notes
        return {}

    def set_notes(self, *args, **kwargs):
        self._set_element(self._json_data['notes'], *args, **kwargs)
        if self.auto_save:
            self.save()

    ### Utilities ###

    @property
    def day_of_year(self):
        days = sum([self.get_days_in_months(i) for i in range(self.month_of_year-1)])
        return days + self.day_of_month

    def days_before(self, *args, **kwargs):
        if not args and not kwargs:
            return self.days_since()
        else:
            year, month, day = self._parse_date_parameters(*args, **kwargs)
            days_since = sum([self.get_days_in_months(i) for i in range(month-1)])
            days_since += day
        while year < self.current_year:
            days_since += self.days_in_year
            year += 1
        return days_since

    def days_since(self, *args, **kwargs):
        if not args and not kwargs:
            year = self.year
            days_since = self.day_of_year
        else:
            year, month, day = self._parse_date_parameters(*args, **kwargs)
            days_since = sum([self.get_days_in_months(i+month) for i in range(self.month_of_year - month)])
            days_since = days_since + (self.day_of_month - day)
        while year < self.current_year:
            days_since += self.days_in_year
            year += 1
        return days_since

    def weekday(self, *args, **kwargs):
        if not args and not kwargs:
            days_since = self.days_since()
        else:
            year, month, day = self._parse_date_parameters(*args, **kwargs)
            days_since = self.days_before(year, month, day)

        days_since += self.first_weekday
        weekday = days_since % self.days_in_week
        return self.get_weekdays(weekday-1)  # -1 to account for 0-indexed list

    @property
    def today(self):
        return (self.current_year, self.month_of_year, self.day_of_month)
        # TODO: format needs to be overwritten to account for custom ranges and months
        # return datetime.datetime(today[0], today[1], today[2]).strftime(format)

    @today.setter
    def today(self, value):
        year, month, day = self._parse_date_parameters(value)
        self.current_year = year
        self.month_of_year = month
        self.day_of_month = day


class ElderanCalendar(DonjonCalendar):
    def __init__(self):
        path = Path(__file__).parents[2]/'data'/'elderan-calendar.json'
        super().__init__(path)

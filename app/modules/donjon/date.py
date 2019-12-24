import json
import math
import os
import re
from pathlib import Path

MINYEAR = 1
MAXYEAR = 9999


def cmp(a, b):
    # Essentially the 'cmp' funcntion in Python2
    return (a > b) - (a < b)


def _cmperror(x, y):
    raise TypeError((f'can\'t compare \'{type(x).__name__}\' '
                     f'to \'{type(y).__name__}\''))


def _ord_ind(n):
    return 'tsnrhtdd'[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4]


class DonjonDate(object):
    """Loosely based on 'date' class from
    https://svn.python.org/projects/sandbox/trunk/datetime/datetime.py"""

    def __init__(self, calendar_file, year, month=None, day=None, era=None):
        if not calendar_file:
            raise ValueError('no calendar file specified', calendar_file)

        with open(calendar_file) as json_file:
            json_data = json.load(json_file)

        if not json_data:
            raise ValueError('calendar file is empty or not json valid',
                             calendar_file)

        self.__weekdays = json_data.get('weekdays', [])
        self.__days_in_week = json_data.get('week_len', 0)
        self.__first_day_of_week = 0
        self.__months = json_data.get('months', [])
        self.__days_in_month = json_data.get('month_len', [])
        self.__days_in_year = json_data.get('year_len', 0)
        self.__months_in_year = json_data.get('n_months', 0)

        self.__year = year
        self.__month = month
        self.__day = day
        self.__era = era

    # Helpers

    def _check_date_fields(self, year, month, day):
        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError(f'year must be in {MINYEAR}..{MAXYEAR}', year)
        miy = self.__months_in_year
        if not 1 <= month <= miy:
            raise ValueError(f'month must be in 1..{miy}', month)
        dim = self._days_in_month(month)
        if not 1 <= day <= dim:
            raise ValueError(f'day must be in 1..{dim}', day)

    def _days_before_year(self, year):
        return (year - 1) * self.__days_in_year

    def _days_in_month(self, month):
        """Assumes 1-based month argument"""
        return self.__days_in_month[self.__months[month-1]]

    def _days_before_month(self, month):
        miy = self.__months_in_year
        if not 1 <= month <= miy:
            raise ValueError(f'month must be in 1..{miy}', month)
        return sum([self._days_in_month(i+1) for i in range(month-1)])

    def _ymd2ord(self, year, month, day):
        miy = self.__months_in_year
        if not 1 <= month <= miy:
            raise ValueError(f'month must be in 1..{miy}', month)
        dim = self._days_in_month(month)
        if not 1 <= day <= dim:
            raise ValueError(f'day must be in 1..{dim}', day)
        return (self._days_before_year(year) +
                self._days_before_month(month) +
                day)

    def _ord2ymd(self, n):
        year, n = divmod(n, self.__days_in_year)
        for month in range(self.__months_in_year):
            dim = self._days_in_month(month+1)  # 0-based loop
            if dim >= n:
                break
            n -= dim
        return year+1, month+1, n

    # Additional constructors

    @classmethod
    def from_ordinal(cls, ordinal):
        y, m, d = cls(None)._ord2ymd(ordinal)
        return cls(y, m, d)

    @classmethod
    def from_iso_format(cls, date_string):
        v = list(map(int, re.split(r'\D+', str(date_string))))
        return cls(v[0], v[1], v[2])

    @classmethod
    def today(cls):
        with open(cls._CFG_PATH) as json_file:
            json_data = json.load(json_file)
        default_year = json_data.get('year', 1)
        date_str = json_data.get('current_date', f'{default_year}-1-1')
        d = cls.from_iso_format(date_str)
        d.era = json_data.get('era')
        return d

    # String conversions

    def iso_format(self):
        return f'{self.__year:04d}-{self.__month:02d}-{self.__day:02d}'

    def donjon_format(self):
        return f'{self.__year}-{self.__month}-{self.__day}'

    __str__ = donjon_format

    def __repr__(self):
        c_name = self.__class__.__name__
        return f'{c_name}({self.__year}, {self.__month}, {self.__day})'

    def descr_format(self):
        weekday = self.__weekdays[self.weekday()-1]
        day = self.__day
        ord_ind = _ord_ind(day)
        month = self.__months[self.__month-1]
        year = self.__year
        era = str(self.__era if self.__era else '') + 'E'
        return f'{weekday}, {day}{ord_ind} of {month}, {era}{year}'

    # Properties

    @property
    def era(self):
        return self.__era

    @era.setter
    def era(self, value):
        try:
            self.__era = int(value)
        except TypeError:
            pass

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        return self.__day

    @property
    def first_day_of_week(self):
        return self.__first_day_of_week

    @first_day_of_week.setter
    def first_day_of_week(self, value):
        try:
            self.__first_day_of_week = int(value)
        except TypeError:
            pass

    # Conversions

    def to_ordinal(self):
        return self._ymd2ord(self.__year, self.__month, self.__day)

    def replace(self, year=None, month=None, day=None):
        if year is None:
            year = self.__year
        if month is None:
            month = self.__month
        if day is None:
            day = self.__day
        self._check_date_fields(year, month, day)
        return self.__class__(year, month, day)

    # Comparisons

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__cmp(other) == 0
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.__cmp(other) != 0
        else:
            return True

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.__cmp(other) <= 0
        else:
            _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.__cmp(other) < 0
        else:
            _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.__cmp(other) >= 0
        else:
            _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.__cmp(other) > 0
        else:
            _cmperror(self, other)

    def __cmp(self, other):
        assert isinstance(other, self.__class__)
        y1, m1, d1 = self.__year, self.__month, self.__day
        y2, m2, d2 = other.__year, other.__month, other.__day
        return cmp((y1, m1, d1), (y2, m2, d2))

    # Computations

    def __add__(self, other):
        if isinstance(other, int):
            return self.__class__.from_ordinal(self.to_ordinal() + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, int):  # 'timedelta' object doesn't exist (yet)
            return self.__class__.from_ordinal(self.to_ordinal() - other)
        if isinstance(other, DonjonDate):
            days1 = self.to_ordinal()
            days2 = other.to_ordinal()
            return days1 - days2
        return NotImplemented

    def weekday(self):
        return ((self.to_ordinal() + self.__first_day_of_week) % self.__days_in_week) + 1


class ElderanDate(DonjonDate):
    _CFG_PATH = Path(__file__).parents[2]/'data'/'elderan'/'calendar.json'

    def __init__(self, year, month=None, day=None, era=3, **kwargs):
        _path = kwargs.get('calendar_file', ElderanDate._CFG_PATH)
        super().__init__(_path, year, month, day, era)
        self.first_day_of_week = 1

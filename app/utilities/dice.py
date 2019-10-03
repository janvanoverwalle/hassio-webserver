""" Dice module """


class Dice(object):
    """ A class representing a (set of) dice """

    _type_map = (0, 4, 6, 8, 10, 12, 20)

    def __init__(self, dice=0, **kwargs):
        d, a, m = self._parse_dice(dice)
        self._type = d
        self._amount = a
        self.change_amount_by(kwargs.get('amount'))
        self._mod = m
        self.change_modifier_by(kwargs.get('modifier'))

    def __str__(self):
        mod = (f'{self._mod:+}' if self._mod != 0 else '') if not isinstance(self._mod, str) else self._mod
        return f'{self._amount}d{self._type}{mod}'

    def __repr__(self):
        return str(self)

    def _parse_dice(self, dice):
        segments = dice.strip().lower().split('d', 1)
        a = int(segments[0]) if len(segments) > 1 else 1
        if '+' in segments[-1]:
            d_data = segments[-1].split('+')
            d = int(d_data[0])
            try:
                m = int(d_data[-1])
            except ValueError:
                m = f'+{d_data[-1]}'
        elif '-' in segments[-1]:
            d_data = segments[-1].split('-')
            d = int(d_data[0])
            try:
                m = -int(d_data[-1])
            except ValueError:
                m = f'-{d_data[-1]}'
        elif '*' in segments[-1]:
            d_data = segments[-1].split('*')
            d = int(d_data[0])
            m = f'*{d_data[-1]}'
        elif '/' in segments[-1]:
            d_data = segments[-1].split('/')
            d = int(d_data[0])
            m = f'/{d_data[-1]}'
        else:
            d = int(segments[-1])
            m = 0
        return d, a, m

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def modifier(self):
        return self._mod

    @modifier.setter
    def modifier(self, value):
        self._mod = value

    def change_type_by(self, step):
        if step is None:
            return
        try:
            idx = self._type_map.index(self._type)
        except ValueError:
            idx = 0
        idx = max(0, min(idx + int(step), len(self._type_map)))
        self._type = self._type_map[idx]

    def change_amount_by(self, step):
        if step is None:
            return
        self._amount = max(0, self._amount + int(step))

    def change_modifier_by(self, step):
        if step is None:
            return
        try:
            self._mod += int(step)
        except (TypeError, ValueError):
            self._mod += f'{step:+}'

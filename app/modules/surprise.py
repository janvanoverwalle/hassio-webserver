from datetime import datetime
from enum import Enum


class ValidCodes(Enum):
    TEST = 'test'
    EL_BROCCO = 'elbrocco'
    LUSJIFER = 'lusjifer'
    RACCOON_BABUSHKA = 'raccoonbabushka'
    I_LOVE_YOU = 'iloveyou'

    @staticmethod
    def from_string(code: str):
        if isinstance(code, ValidCodes):
            return code
        for c in ValidCodes:
            if code == c.value:
                return c
        raise KeyError(f'{code}')


class Surprise:
    DATE_FORMAT = '%d/%m/%Y %H:%M'
    CODE_UNLOCK_DATES = {
        #ValidCodes.EL_BROCCO: datetime.strptime('10/03/2023 10:00', DATE_FORMAT),
        #ValidCodes.LUSJIFER: datetime.strptime('17/03/2023 10:00', DATE_FORMAT),
        #ValidCodes.RACCOON_BABUSHKA: datetime.strptime('24/03/2023 10:00', DATE_FORMAT),
        #ValidCodes.I_LOVE_YOU: datetime.strptime('31/03/2023 10:00', DATE_FORMAT)
    }

    CODE_TITLES = {
        ValidCodes.TEST: 'Test',
        ValidCodes.EL_BROCCO: 'El Brocco',
        ValidCodes.LUSJIFER: 'Lusjifer',
        ValidCodes.RACCOON_BABUSHKA: 'Raccoon Babushka',
        ValidCodes.I_LOVE_YOU: 'I Love You ❤️'
    }

    @classmethod
    def get_title_for_code(cls, code: str):
        return cls.CODE_TITLES.get(ValidCodes.from_string(code), 'unknown-code')

    @classmethod
    def get_unlock_date_for_code(cls, code: str):
        return cls.CODE_UNLOCK_DATES.get(ValidCodes.from_string(code))

    @classmethod
    def is_valid_code(cls, code: str):
        if not code:
            return False
        try:
            ValidCodes.from_string(code)
        except KeyError:
            return False
        return True

    @classmethod
    def is_unlocked_code(cls, code: str):
        if not cls.is_valid_code(code):
            return False
        now = datetime.now()
        unlock_date = cls.CODE_UNLOCK_DATES.get(ValidCodes.from_string(code), now)
        return unlock_date <= now

    @classmethod
    def get_unlocked_codes(cls):
        result = []
        now = datetime.now()
        for code in ValidCodes:
            date = cls.CODE_UNLOCK_DATES.get(code, now)
            if date <= now:
                result.append(code.value)
        return result

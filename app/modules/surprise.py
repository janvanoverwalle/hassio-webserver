from datetime import datetime
from enum import Enum


class ValidCodes(Enum):
    TEST = 'test'
    CODE1 = 'code1'
    CODE2 = 'code2'
    CODE3 = 'code3'

    @staticmethod
    def from_string(code: str):
        if isinstance(code, ValidCodes):
            return code
        for c in ValidCodes:
            if code == c.value:
                return c
        raise KeyError(f'{code}')


class Surprise:
    DATE_FORMAT = '%d/%m/%y %H:%M:%S'
    CODE_UNLOCK_DATES = {
        ValidCodes.TEST: datetime.strptime('24/02/22 15:00:00', DATE_FORMAT)
    }

    CODE_TITLES = {
        ValidCodes.TEST: 'Test'
    }

    @classmethod
    def get_unlocked_codes(cls):
        # TODO: Implement properly
        return [
            ValidCodes.TEST.value
        ]

    @classmethod
    def get_title_for_code(cls, code: str):
        return cls.CODE_TITLES.get(ValidCodes.from_string(code), 'unknown-code')

    @classmethod
    def validate_code(cls, code: str):
        if not code:
            return False
        try:
            ValidCodes.from_string(code)
        except KeyError:
            return False
        return True

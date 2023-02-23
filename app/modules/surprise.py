class Surprise:
    VALID_CODES = [
        'test',
        'code1',
        'code2',
        'code3'
    ]

    CODE_TITLES = {
        'test': 'Test'
    }

    @classmethod
    def get_unlocked_codes(cls):
        # TODO: Implement properly
        return [
            'test'
        ]

    @classmethod
    def get_title_for_code(cls, code: str):
        return cls.CODE_TITLES.get(code, 'Unknown code')

    @classmethod
    def validate_code(cls, code: str):
        code = code.strip().lower()
        if not code:
            return False
        return code in cls.VALID_CODES

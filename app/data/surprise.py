class Surprise:
    VALID_CODES = [
        'test',
        'code1',
        'code2',
        'code3'
    ]

    @classmethod
    def get_unlocked_codes(cls):
        # TODO: Implement properly
        return [
            'test'
        ]

    @classmethod
    def validate_code(cls, code: str):
        code = code.strip().lower()
        if not code:
            return False
        return code in cls.VALID_CODES

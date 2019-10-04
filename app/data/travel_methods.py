""" Travel Method module """


class TravelMethods(object):
    DEDICATED = 'dedicated'
    SLOW = 'slow'
    NORMAL = 'normal'
    FAST = 'fast'

    _DESCRIPTIONS = {
        DEDICATED: 'Dedicated search without traveling',
        SLOW: 'Traveling at a slow or stealthy pace',
        NORMAL: 'Traveling at a normal pace',
        FAST: 'Traveling at a fast pace'
    }

    _DCS = {
        DEDICATED: 12,
        SLOW: 15,
        NORMAL: 18,
        FAST: 21
    }

    @classmethod
    def to_list(cls):
        return [
            cls.DEDICATED.capitalize(),
            cls.SLOW.capitalize(),
            cls.NORMAL.capitalize(),
            cls.FAST.capitalize()
        ]

    @classmethod
    def description(cls, travel_method):
        return cls._DESCRIPTIONS.get(travel_method.lower())

    @classmethod
    def dc(cls, travel_method):
        return cls._DCS.get(travel_method.lower())

    @classmethod
    def gather(cls, travel_method, roll):
        return int(roll) >= cls.dc(travel_method)

""" Ingredient Properties module """


class IngredientType(object):
    """ Ingredient type enum """

    POTION = 'Potion'
    POISON = 'Poison'
    ENCHANTMENT = 'Enchantment'

    _duration_multiplier = {
        POTION: 1,
        POISON: 1.1,
        ENCHANTMENT: 1.3
    }

    @classmethod
    def duration_multiplier(cls, t):
        return cls._duration_multiplier.get(t, 1)


class IngredientRarity(object):
    """ Ingredient rarity enum """

    COMMON = 'Common'
    UNCOMMON = 'Uncommon'
    RARE = 'Rare'
    VERY_RARE = 'Very Rare'

    _duration_multiplier = {
        COMMON: .7,
        UNCOMMON: 1,
        RARE: 1.4,
        VERY_RARE: 1.9
    }

    @classmethod
    def duration_multiplier(cls, r):
        return cls._duration_multiplier.get(r, 1)


class IngredientFunction(object):
    """ Ingredient function enum """

    EFFECT = 'Effect'
    MODIFIER = 'Modifier'


class IngredientProperty(object):
    """ Ingredient property class """

    DICE = 'dice'
    RESISTANCES = 'resistances'
    DURATION = 'duration'
    DAMAGE_TYPE = 'damage_type'

    def __init__(self):
        self._properties = {}

    def _check_property_key(self, key):
        if key not in self._properties:
            self._properties[key] = {}

    def _get_absolute_dice_size(self, dice):
        if not isinstance(dice, str):
            dice = str(dice)
        segments = dice.strip().lower().split('d')
        amount = int(segments[0]) if len(segments) > 1 else 1
        size = int(segments[-1] if len(segments) > 1 else segments[0])
        return amount * size

    @property
    def properties(self):
        return self.properties

    def add_dice(self, dice_type, amount):
        self._check_property_key(self.DICE)

        if dice_type not in self._properties[self.DICE]:
            self._properties[self.DICE][dice_type] = 0

        self._properties[self.DICE][dice_type] += amount

    def add_resistance(self, resistance_type, duration):
        self._check_property_key(self.RESISTANCES)

        p_dice = self._properties[self.RESISTANCES].get(resistance_type, '0d0')
        d0 = self._get_absolute_dice_size(p_dice)
        d1 = self._get_absolute_dice_size(duration)

        if d1 > d0:
            self._properties[self.RESISTANCES][resistance_type] = str(duration)

    def add_duration(self, duration):
        p_dur = self._properties.get(self.DURATION, '0d0')
        d0 = self._get_absolute_dice_size(p_dur)
        d1 = self._get_absolute_dice_size(duration)

        if d1 > d0:
            self._properties[self.DURATION] = str(duration)

    def add_damage_type(self, damage_type):
        self._properties[self.DAMAGE_TYPE] = str(damage_type)

import random


class TerrainIngredient(object):
    def __init__(self, ingredient, **kwargs):
        self._ingredient = ingredient
        self._multiplier = kwargs.get('multiplier', (1, 1))
        if not isinstance(self._multiplier, tuple):
            self._multiplier = (self._multiplier, self._multiplier)
        self._additional = kwargs.get('additional')
        self._remarks = kwargs.get('remarks')

    @property
    def ingredient(self):
        return self._ingredient

    @property
    def remarks(self):
        return self._remarks

    @property
    def additional(self):
        return self._additional

    def apply_multiplier(self, amount):
        return amount * random.choice(self._multiplier)

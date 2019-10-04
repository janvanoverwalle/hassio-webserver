from .ingredients import Ingredients
from .terrain_types import TerrainTypes
from utilities.dice import Dice
import random


class TerrainIngredient(object):
    def __init__(self, ingredient, **kwargs):
        self._ingredient = ingredient
        self._multiplier = kwargs.get('multiplier', (1, 1))
        if not isinstance(self._multiplier, tuple):
            self._multiplier = (self._multiplier, self._multiplier)
        self._remarks = kwargs.get('remarks')

    @property
    def ingredient(self):
        return self._ingredient

    @property
    def remarks(self):
        return self._remarks

    def apply_multiplier(self, amount):
        return amount * random.choice(self._multiplier)


class TerrainTable(object):
    _type = None
    _data = None

    @classmethod
    def retrieve_ingredient(cls, amount):
        dice = Dice('2d6')
        ingredient = cls._data.get(dice.roll())

        try:
            while True:
                ingredient = ingredient._data.get(dice.roll())
        except AttributeError:
            pass

        return (
            ingredient.ingredient,
            ingredient.apply_multiplier(amount),
            ingredient.remarks
        )

    @classmethod
    def is_type(cls, terrain_type):
        return cls._type.lower() == terrain_type.lower()


class CommonTable(TerrainTable):
    _type = TerrainTypes.MOST
    _data = {
        2: TerrainIngredient(Ingredients.MANDRAKE_ROOT),
        3: TerrainIngredient(Ingredients.QUICKSILVER_LICHEN),
        4: TerrainIngredient(Ingredients.QUICKSILVER_LICHEN),
        5: TerrainIngredient(Ingredients.WILD_SAGEROOT),
        6: TerrainIngredient(Ingredients.WILD_SAGEROOT),
        7: TerrainIngredient(Ingredients.BLOODGRASS),
        8: TerrainIngredient(Ingredients.WYRMTONGUE_PETALS),
        9: TerrainIngredient(Ingredients.WYRMTONGUE_PETALS),
        10: TerrainIngredient(Ingredients.MILKWEED_SEEDS),
        11: TerrainIngredient(Ingredients.MILKWEED_SEEDS),
        12: TerrainIngredient(Ingredients.MANDRAKE_ROOT)
    }


class ArcticTable(TerrainTable):
    _type = TerrainTypes.ARCTIC
    _data = {
        2: TerrainIngredient(Ingredients.SILVER_HIBISCUS),
        3: TerrainIngredient(Ingredients.MORTFLESH_POWDER),
        4: TerrainIngredient(Ingredients.IRONWOOD_HEART),
        5: TerrainIngredient(Ingredients.FROZEN_SEEDLINGS, multiplier=2),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.ARCTIC_CREEPER, multiplier=2),
        10: TerrainIngredient(Ingredients.FENNEL_SILK),
        11: TerrainIngredient(Ingredients.FIENDS_IVY),
        12: TerrainIngredient(Ingredients.VOIDROOT)
    }


class TerrainTables(object):
    _tables = [
        CommonTable,
        ArcticTable
    ]

    @classmethod
    def retrieve_ingredient(cls, terrain, amount=None):
        if amount is None:
            amount = Dice('1d4').roll()
        terrain_table = [t for t in cls._tables if t.is_type(terrain)]
        if len(terrain_table) <= 0:
            raise ValueError(f'Invalid terrain type given: {terrain}')
        return terrain_table[0].retrieve_ingredient(amount)

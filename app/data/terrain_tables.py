from .ingredients import Ingredients
from .terrain_types import TerrainTypes
from .terrain_ingredients import TerrainIngredient
from utilities.dice import Dice
import random


class TerrainTable(object):
    _type = None
    _data = None

    @classmethod
    def retrieve_ingredient(cls):
        dice = Dice('2d6')
        roll = dice.roll()

        special = False
        if 2 <= roll <= 4 or 10 <= roll <= 12 and random.random() > .75:
            ingredient = TerrainIngredient(Ingredients.ELEMENTAL_WATER)
            special = True
        else:
            ingredient = cls._data.get(roll)

        try:
            while True:
                ingredient = ingredient._data.get(dice.roll())
        except AttributeError:
            pass

        return ingredient, special

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


class CoastalTable(TerrainTable):
    _type = TerrainTypes.COASTAL
    _data = {
        2: TerrainIngredient(Ingredients.HYDRATHISTLE, multiplier=(1, 2)),
        3: TerrainIngredient(Ingredients.AMANITA_CAP),
        4: TerrainIngredient(Ingredients.HYANCINTH_NECTAR),
        5: TerrainIngredient(Ingredients.CHROMUS_SLIME, multiplier=(1, 2)),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.LAVENDER_SPRIG),
        10: TerrainIngredient(Ingredients.BLUE_TOADSHADE),
        11: TerrainIngredient(Ingredients.WRACKWORT_BULBS),
        12: TerrainIngredient(Ingredients.COSMOS_GLOND, multiplier=(1, 2))
    }


class UnderwaterTable(TerrainTable):
    _type = TerrainTypes.UNDERWATER
    _data = {
        2: TerrainIngredient(Ingredients.HYDRATHISTLE, multiplier=(1, 2)),
        3: TerrainIngredient(Ingredients.AMANITA_CAP, multiplier=0),  # Coastal only
        4: TerrainIngredient(Ingredients.HYANCINTH_NECTAR),
        5: TerrainIngredient(Ingredients.CHROMUS_SLIME, multiplier=(1, 2)),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.LAVENDER_SPRIG, multiplier=0),  # Coastal only
        10: TerrainIngredient(Ingredients.BLUE_TOADSHADE, multiplier=0),  # Coastal only
        11: TerrainIngredient(Ingredients.WRACKWORT_BULBS),
        12: TerrainIngredient(Ingredients.COSMOS_GLOND, multiplier=(1, 2))
    }


class DesertTable(TerrainTable):
    _type = TerrainTypes.DESERT
    _data = {
        2: TerrainIngredient(Ingredients.COSMOS_GLOND),
        3: TerrainIngredient(Ingredients.ARROW_ROOT),
        4: TerrainIngredient(Ingredients.DRIED_EPHEDRA),
        5: TerrainIngredient(Ingredients.CACTUS_JUICE, multiplier=2),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.DRAKUS_FLOWER),
        10: TerrainIngredient(Ingredients.SCILLIA_BEANS),
        11: TerrainIngredient(Ingredients.SPINEFLOWER_BERRIES),
        12: TerrainIngredient(Ingredients.VOIDROOT, additional=Ingredients.ELEMENTAL_WATER)
    }


class ForestTable(TerrainTable):
    _type = TerrainTypes.FOREST
    _data = {
        2: TerrainIngredient(Ingredients.HARRADA_LEAF),
        3: TerrainIngredient(Ingredients.NIGHTSHADE_BERRIES),
        4: TerrainIngredient(Ingredients.EMETIC_WAX),
        5: TerrainIngredient(Ingredients.VERDANT_NETTLE),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.ARROW_ROOT),
        10: TerrainIngredient(Ingredients.IRONWOOD_HEART),
        11: TerrainIngredient(Ingredients.BLUE_TOADSHADE),
        12: TerrainIngredient(Ingredients.WISP_STALKS,
                              remarks='Find 2x during Night, Re-roll during Day')
    }


class GrasslandTable(TerrainTable):
    _type = TerrainTypes.GRASSLAND
    _data = {
        2: TerrainIngredient(Ingredients.HARRADA_LEAF),
        3: TerrainIngredient(Ingredients.DRAKUS_FLOWER),
        4: TerrainIngredient(Ingredients.LAVENDER_SPRIG, multiplier=2),
        5: TerrainIngredient(Ingredients.ARROW_ROOT),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.SCILLIA_BEANS, multiplier=2),
        10: TerrainIngredient(Ingredients.CACTUS_JUICE),
        11: TerrainIngredient(Ingredients.TAIL_LEAF),
        12: TerrainIngredient(Ingredients.HYANCINTH_NECTAR)
    }


class HillTable(TerrainTable):
    _type = TerrainTypes.HILL
    _data = {
        2: TerrainIngredient(Ingredients.DEVILS_BLOODLEAF),
        3: TerrainIngredient(Ingredients.NIGHTSHADE_BERRIES),
        4: TerrainIngredient(Ingredients.TAIL_LEAF, multiplier=2),
        5: TerrainIngredient(Ingredients.LAVENDER_SPRIG),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.IRONWOOD_HEART),
        10: TerrainIngredient(Ingredients.GENGKO_BRUSH),
        11: TerrainIngredient(Ingredients.ROCK_VINE, multiplier=2),
        12: TerrainIngredient(Ingredients.HARRADA_LEAF)
    }


class MountainTable(TerrainTable):
    _type = TerrainTypes.MOUNTAIN
    _data = {
        2: TerrainIngredient(Ingredients.BASILISK_BREATH),
        3: TerrainIngredient(Ingredients.FROZEN_SEEDLINGS, multiplier=2),
        4: TerrainIngredient(Ingredients.ARCTIC_CREEPER, multiplier=2),
        5: TerrainIngredient(Ingredients.DRIED_EPHEDRA),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.DRAKUS_FLOWER),
        10: TerrainIngredient(Ingredients.LUMINOUS_CAP_DUST, multiplier=2),
        11: TerrainIngredient(Ingredients.ROCK_VINE),
        12: TerrainIngredient(Ingredients.PRIMORDIAL_BALM)
    }


class SwampTable(TerrainTable):
    _type = TerrainTypes.SWAMP
    _data = {
        2: TerrainIngredient(Ingredients.DEVILS_BLOODLEAF),
        3: TerrainIngredient(Ingredients.SPINEFLOWER_BERRIES),
        4: TerrainIngredient(Ingredients.EMETIC_WAX),
        5: TerrainIngredient(Ingredients.AMANITA_CAP, multiplier=2),
        6: CommonTable,
        7: CommonTable,
        8: CommonTable,
        9: TerrainIngredient(Ingredients.BLUE_TOADSHADE, multiplier=2),
        10: TerrainIngredient(Ingredients.WRACKWORT_BULBS),
        11: TerrainIngredient(Ingredients.HYDRATHISTLE, multiplier=2),
        12: TerrainIngredient(Ingredients.PRIMORDIAL_BALM)
    }


class UnderdarkTable(TerrainTable):
    _type = TerrainTypes.UNDERDARK
    _data = {
        2: TerrainIngredient(Ingredients.PRIMORDIAL_BALM, multiplier=(1, 2)),
        3: TerrainIngredient(Ingredients.SILVER_HIBISCUS),
        4: TerrainIngredient(Ingredients.DEVILS_BLOODLEAF),
        5: TerrainIngredient(Ingredients.CHROMUS_SLIME),
        6: TerrainIngredient(Ingredients.MORTFLESH_POWDER, multiplier=2),
        7: TerrainIngredient(Ingredients.FENNEL_SILK),
        8: TerrainIngredient(Ingredients.FIENDS_IVY),
        9: TerrainIngredient(Ingredients.GENGKO_BRUSH),
        10: TerrainIngredient(Ingredients.LUMINOUS_CAP_DUST, multiplier=2),
        11: TerrainIngredient(Ingredients.RADIANT_SYNTHSEED),
        12: TerrainIngredient(Ingredients.WISP_STALKS)
    }


class TerrainTables(object):
    _tables = [
        CommonTable,
        ArcticTable,
        CoastalTable,
        UnderwaterTable,
        DesertTable,
        ForestTable,
        GrasslandTable,
        HillTable,
        MountainTable,
        SwampTable,
        UnderdarkTable
    ]

    @classmethod
    def retrieve_ingredient(cls, terrain):
        terrain_table = [t for t in cls._tables if t.is_type(terrain)]
        if len(terrain_table) <= 0:
            raise ValueError(f'Invalid terrain type given: {terrain}')
        return terrain_table[0].retrieve_ingredient()

""" Ingredients module """


from app.models.ingredient_properties import IngredientFunction, IngredientRarity,\
    IngredientTerrain, IngredientType


class Ingredient(object):
    """ Default ingredient class """

    def __init__(self, name, **kwargs):
        self._name = name
        self._id = kwargs.get('id')
        self._type = kwargs.get('type')
        self._rarity = kwargs.get('rarity')
        self._special = kwargs.get('special', False)
        self._function = kwargs.get('function')
        self._details = kwargs.get('details')
        self._dc = kwargs.get('dc')
        self._terrain = kwargs.get('terrain')
        self._property = kwargs.get('property', self._details)

        if not isinstance(self._type, list):
            self._type = [self._type]

        if not isinstance(self._terrain, list):
            self._terrain = [self._terrain]

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def rarity(self):
        return self._rarity

    @property
    def is_special(self):
        return self._special

    @property
    def function(self):
        return self._function

    @property
    def details(self):
        return self._details

    @property
    def dc(self):
        return self._dc

    @property
    def terrain(self):
        return self._terrain

    @property
    def property(self):
        return self._property


###########
# Potions #
###########

class Bloodgrass(Ingredient):
    """ Bloodgrass ingredient """

    def __init__(self):
        super().__init__(
            'Bloodgrass',
            id=0x00,
            type=IngredientType.POTION,
            rarity=IngredientRarity.COMMON,
            special=True,
            function=IngredientFunction.EFFECT,
            details=(
                'Can combine with any other Potion Effect ingredient to become '
                'a food source for 1 day. Cannot be altered by other ingredients.'
            ),
            dc=0,
            terrain=IngredientTerrain.MOST
        )


class DriedEphedra(Ingredient):
    """ Dried Ephedra ingredient """

    def __init__(self):
        super().__init__(
            'Dried Ephedra',
            id=0x01,
            type=IngredientType.POTION,
            rarity=IngredientRarity.UNCOMMON,
            function=IngredientFunction.MODIFIER,
            details='Increase the dice-type by 1 size for any healing Effect.',
            dc=2,
            terrain=[
                IngredientTerrain.DESERT,
                IngredientTerrain.MOUNTAIN
            ],
            property={'increase_dice_type': 1}
        )


class FennelSilk(Ingredient):
    """ Fennel Silk ingredient """

    def __init__(self):
        super().__init__(
            'Fennel Silk',
            id=0x02,
            type=IngredientType.POTION,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.EFFECT,
            details=(
                'Stabilizes body heat to resist cold weather or wet condition penalties for 1 hour.'
                ' Cannot be altered by other ingredients.'
            ),
            dc=2,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.UNDERDARK
            ],
            property={'resistance': ('cold', 3600)}
        )


class GengkoBrush(Ingredient):
    """ Gengko Brush ingredient """

    def __init__(self):
        super().__init__(
            'Gengko Brush',
            id=0x03,
            type=IngredientType.POTION,
            rarity=IngredientRarity.UNCOMMON,
            function=IngredientFunction.MODIFIER,
            details=(
                'Double the dice rolled of any healing Effect, but divide the total of the dice '
                'by 2 (rounding down); Then, the recipient receives that amount of healing '
                'per round for 2 rounds.'
            ),
            dc=2,
            terrain=[
                IngredientTerrain.HILL,
                IngredientTerrain.UNDERDARK
            ],
            property={'dice_amount': '*2', 'dice_total': '*.5', 'duration': 12}
        )


class HyancinthNectar(Ingredient):
    """ Hyancinth Nectar ingredient """

    def __init__(self):
        super().__init__(
            'Hyancinth Nectar',
            id=0x04,
            type=IngredientType.POTION,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.EFFECT,
            details=(
                'Removes 1d6 rounds of poison in the target’s system, but cannot remove it '
                'completely. One round of poison damage will still occur at minimum.'
            ),
            dc=1,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.GRASSLAND
            ]
        )


class MandrakeRoot(Ingredient):
    """ Mandrake Root ingredient """

    def __init__(self):
        super().__init__(
            'Mandrake Root',
            id=0x05,
            type=IngredientType.POTION,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.EFFECT,
            details=(
                'Reduce any disease or poison’s potency by half for 2d12 hours. '
                'Only hinders already existing poisons or diseases in the body. '
                'Cannot be altered by other ingredients.'
            ),
            dc=0,
            terrain=IngredientTerrain.MOST,
            property={'potency': ('*.5', '2d12*3600')}
        )


class MilkweedSeeds(Ingredient):
    """ Milkweed Seeds ingredient """

    def __init__(self):
        super().__init__(
            'Milkweed Seeds',
            id=0x06,
            type=IngredientType.POTION,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.MODIFIER,
            details=(
                'Double the dice rolled of any healing Effect, but remove all Alchemy Modifier '
                'bonuses. This modifier can stack.'
            ),
            dc=2,
            terrain=IngredientTerrain.MOST,
            property={'dice_amount': '*2', 'alchemy_modifier': 0}
        )


class WildSageroot(Ingredient):
    """ Wild Sageroot ingredient """

    def __init__(self):
        super().__init__(
            'Wild Sageroot',
            id=0x07,
            type=IngredientType.POTION,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.EFFECT,
            details='Heals for 2d4 + Alchemy Modifier.',
            dc=0,
            terrain=IngredientTerrain.MOST,
            property={'effect_dice': '2d4+mod'}
        )


###########
# Poisons #
###########

class ArcticCreeper(Ingredient):
    """ Arctic Creeper ingredient """

    def __init__(self):
        super().__init__(
            'Arctic Creeper',
            id=0x08,
            type=IngredientType.POISON,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.MODIFIER,
            details=(
                'Change poison damage to cold or necrotic damage; target is still [poisoned] for '
                '1 minute on a failed CON saving throw; this toxin is still considered '
                'poison damage when combining with other ingredients.'
            ),
            dc=2,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.MOUNTAIN
            ],
            property={'damage_type': ['cold', 'necrotic']}
        )


class AmanitaCap(Ingredient):
    """ Amanita Cap ingredient """

    def __init__(self):
        super().__init__(
            'Amanita Cap',
            id=0x09,
            type=IngredientType.POISON,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.MODIFIER,
            details='Changes any poison Effect to be non-lethal and only incapacitate the target.',
            dc=1,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.SWAMP
            ],
            property={'lethal': False}
        )


class BasiliskBreath(Ingredient):
    """ Basilisk Breath ingredient """

    def __init__(self):
        super().__init__(
            'Basilisk Breath',
            id=0x0A,
            type=IngredientType.POISON,
            rarity=IngredientRarity.VERY_RARE,
            special=True,
            function=IngredientFunction.EFFECT,
            details=(
                'Slowly paralyzes opponent. Target makes a DC 5 + Alchemy Modifier CON saving '
                'throw each turn for 4 turns. While under this affect, target is considered slowed '
                'by the slow spell. On a failed save, the target is considered [paralyzed] for '
                '4 rounds. Cannot be modified or altered by other ingredients.'
            ),
            dc=5,
            terrain=IngredientTerrain.MOUNTAIN,
            property={'con_save': '5+mod', 'save_fail': {'condition': 'paralyzed', 'duration': 24}}
        )


class CactusJuice(Ingredient):
    """ Cactus Juice ingredient """

    def __init__(self):
        super().__init__(
            'Cactus Juice',
            id=0x0B,
            type=IngredientType.POISON,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.MODIFIER,
            details=(
                'The target will not notice any poison damage Effect in their system until '
                'they take 5 rounds of damage from the toxin.'
            ),
            dc=2,
            terrain=[
                IngredientTerrain.DESERT,
                IngredientTerrain.GRASSLAND
            ],
            property={'dormant': 5}
        )


class DrakusFlower(Ingredient):
    """ Drakus Flower ingredient """

    def __init__(self):
        super().__init__(
            'Drakus Flower',
            id=0x0C,
            type=IngredientType.POISON,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.MODIFIER,
            details=(
                'Change poison damage to fire or acid damage; target is still [poisoned] for '
                '1 minute on a failed CON saving throw; this toxin is still considered '
                'poison damage when combining with other ingredients.'
            ),
            dc=2,
            terrain=[
                IngredientTerrain.DESERT,
                IngredientTerrain.GRASSLAND,
                IngredientTerrain.MOUNTAIN
            ],
            property={'damage_type': ['fire', 'acid']}
        )


class FrozenSeedlings(Ingredient):
    """ Frozen Seedlings ingredient """

    def __init__(self):
        super().__init__(
            'Frozen Seedlings',
            id=0x0D,
            type=IngredientType.POISON,
            rarity=IngredientRarity.RARE,
            function=IngredientFunction.MODIFIER,
            details=(
                'While [poisoned], target’s movement speed is reduced by 10 ft for 1 minute. '
                'Cannot be altered by other ingredients.'
            ),
            dc=4,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.MOUNTAIN
            ],
            property={'speed': (-10, 60)}
        )


class HarradaLeaf(Ingredient):
    """ Harrada Leaf ingredient """

    def __init__(self):
        super().__init__(
            'Harrada Leaf',
            id=0x0E,
            type=IngredientType.POISON,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.MODIFIER,
            details=(
                'While [poisoned], target has disadvantage on ability checks. '
                'Cannot be altered by other ingredients.'
            ),
            dc=1,
            terrain=IngredientTerrain.FOREST,
            property={'disadvantage': True}
        )


class QuicksilverLichen(Ingredient):
    """ Quicksilver Lichen ingredient """

    def __init__(self):
        super().__init__(
            'Quicksilver Lichen',
            id=0x0F,
            type=IngredientType.POISON,
            rarity=IngredientRarity.UNCOMMON,
            function=IngredientFunction.MODIFIER,
            details=(
                'Double the dice rolled of any Toxin Effect, but reduce that Effect duration '
                'by half. This modifier can stack.'
            ),
            dc=3,
            terrain=IngredientTerrain.MOST,
            property={'dice_amount': '*2', 'duration': '*.5'}
        )


class RadiantSynthseed(Ingredient):
    """ Radiant Synthseed ingredient """

    def __init__(self):
        super().__init__(
            'Radiant Synthseed',
            id=0x10,
            type=IngredientType.POISON,
            rarity=IngredientRarity.RARE,
            function=IngredientFunction.MODIFIER,
            details=(
                'Change poison damage to radiant damage; target is still [poisoned] for 1 minute '
                'on a failed CON saving throw; this toxin is still considered poison damage when '
                'combining with other ingredients.'
            ),
            dc=2,
            terrain=IngredientTerrain.UNDERDARK,
            property={'damage_type': ['radiant']}
        )


class SpineflowerBerries(Ingredient):
    """ Spineflower Berries ingredient """

    def __init__(self):
        super().__init__(
            'Spineflower Berries',
            id=0x11,
            type=IngredientType.POISON,
            rarity=IngredientRarity.UNCOMMON,
            function=IngredientFunction.MODIFIER,
            details='Increase the dice-type by 1 size for any Toxin Effect.',
            dc=3,
            terrain=[
                IngredientTerrain.DESERT,
                IngredientTerrain.SWAMP
            ],
            property={'increase_dice_type': 1}
        )


class WyrmtonguePetals(Ingredient):
    """ Wyrmtongue Petals ingredient """

    def __init__(self):
        super().__init__(
            'Wyrmtongue Petals',
            id=0x12,
            type=IngredientType.POISON,
            rarity=IngredientRarity.COMMON,
            function=IngredientFunction.EFFECT,
            details=(
                '1d4 + Alchemy Modifier poison damage per round; target is [poisoned] for '
                '1 minute on a failed CON save.'
            ),
            dc=0,
            terrain=IngredientTerrain.MOST,
            property={
                'effect_dice': '1d4+mod',
                'con_save': '8+mod',
                'save_fail': {'condition': 'poisoned', 'duration': 60}
            }
        )


###################
# Potions/Poisons #
###################

class ChromusSlime(Ingredient):
    """ Chromus Slime ingredient """

    def __init__(self):
        super().__init__(
            'Chromus Slime',
            id=0x13,
            type=[
                IngredientType.POTION,
                IngredientType.POISON
            ],
            rarity=IngredientRarity.RARE,
            special=True,
            function=IngredientFunction.MODIFIER,
            details=(
                'The final Effect after all other calculations is the exact opposite. '
                'This is up to the DM’s discretion on the specifics per potion/poison.'
            ),
            dc=4,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.UNDERDARK
            ],
            property={'reverse_effect': True}
        )


class EmeticWax(Ingredient):
    """ Emetic Wax ingredient """

    def __init__(self):
        super().__init__(
            'Emetic Wax',
            id=0x14,
            type=[
                IngredientType.POTION,
                IngredientType.POISON
            ],
            rarity=IngredientRarity.COMMON,
            special=True,
            function=IngredientFunction.MODIFIER,
            details='Delay the Effect of an ingredient this was combined with by 1d6 rounds',
            dc=1,
            terrain=[
                IngredientTerrain.FOREST,
                IngredientTerrain.SWAMP
            ],
            property={'delay_effect': '1d6*6'}
        )


class LavenderSprig(Ingredient):
    """ Lavender Sprig ingredient """

    def __init__(self):
        super().__init__(
            'Lavender Sprig',
            id=0x15,
            type=[
                IngredientType.POTION,
                IngredientType.POISON
            ],
            rarity=IngredientRarity.COMMON,
            special=True,
            function=IngredientFunction.MODIFIER,
            details='Makes the potion or toxin more stable and safer to craft.',
            dc=-2,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.GRASSLAND,
                IngredientTerrain.HILL
            ]
        )


################
# Enchantments #
################

class ArrowRoot(Ingredient):
    """ Arrow Root ingredient """

    def __init__(self):
        super().__init__(
            'Arrow Root',
            id=0x16,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.UNCOMMON,
            details='+1 to attack rolls for one minute when applied to a weapon.',
            dc=2,
            terrain=[
                IngredientTerrain.DESERT,
                IngredientTerrain.FOREST,
                IngredientTerrain.GRASSLAND
            ]
        )


class BlueToadshade(Ingredient):
    """ Blue Toadshade ingredient """

    def __init__(self):
        super().__init__(
            'Blue Toadshade',
            id=0x17,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details='User creates a potion of gaseous form (DMG 187).',
            dc=3,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.FOREST,
                IngredientTerrain.SWAMP
            ]
        )


class CosmosGlond(Ingredient):
    """ Cosmos Glond ingredient """

    def __init__(self):
        super().__init__(
            'Cosmos Glond',
            id=0x18,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details='User creates a potion of clairvoyance (DMG 187).',
            dc=3,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.DESERT
            ]
        )


class DevilsBloodleaf(Ingredient):
    """ Devils Bloodleaf ingredient """

    def __init__(self):
        super().__init__(
            'Devils Bloodleaf',
            id=0x19,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.VERY_RARE,
            details='User creates a potion of vitality (DMG 188).',
            dc=5,
            terrain=[
                IngredientTerrain.HILL,
                IngredientTerrain.SWAMP,
                IngredientTerrain.UNDERDARK
            ]
        )


class ElementalWater(Ingredient):
    """ Elemental Water ingredient """

    def __init__(self):
        super().__init__(
            'Elemental Water',
            id=0x1A,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            special=True,
            details='This is required as the base catalyst for all Enchantment ingredients.',
            dc=3,
            terrain=IngredientTerrain.SPECIAL
        )


class FiendsIvy(Ingredient):
    """ Fiends Ivy ingredient """

    def __init__(self):
        super().__init__(
            'Fiends Ivy',
            id=0x1B,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details='User creates a potion of mind reading (DMG 188).',
            dc=4,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.UNDERDARK
            ]
        )


class Hydrathistle(Ingredient):
    """ Hydrathistle ingredient """

    def __init__(self):
        super().__init__(
            'Hydrathistle',
            id=0x1C,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.UNCOMMON,
            details='User creates a potion of water breathing (DMG 188).',
            dc=2,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.SWAMP
            ]
        )


class IronwoodHeart(Ingredient):
    """ Ironwood Heart ingredient """

    def __init__(self):
        super().__init__(
            'Ironwood Heart',
            id=0x1D,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.UNCOMMON,
            details='User creates a potion of growth (DMG 187).',
            dc=3,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.FOREST,
                IngredientTerrain.HILL
            ]
        )


class LuminousCapDust(Ingredient):
    """ Luminous Cap Dust ingredient """

    def __init__(self):
        super().__init__(
            'Luminous Cap Dust',
            id=0x1E,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details='User creates a potion of heroism (DMG 188).',
            dc=4,
            terrain=[
                IngredientTerrain.MOUNTAIN,
                IngredientTerrain.UNDERDARK
            ]
        )


class MortfleshPowder(Ingredient):
    """ Mortflesh Powder ingredient """

    def __init__(self):
        super().__init__(
            'Mortflesh Powder',
            id=0x1F,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.VERY_RARE,
            details='User creates a potion of longevity (DMG 188).',
            dc=5,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.UNDERDARK
            ]
        )


class NightshadeBerries(Ingredient):
    """ Nightshade Berries ingredient """

    def __init__(self):
        super().__init__(
            'Nightshade Berries',
            id=0x20,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.UNCOMMON,
            details='The effect of this “potion” is similar to the oil of slipperiness (DMG 184).',
            dc=3,
            terrain=[
                IngredientTerrain.FOREST,
                IngredientTerrain.HILL
            ]
        )


class PrimordialBalm(Ingredient):
    """ Primordial Balm ingredient """

    def __init__(self):
        super().__init__(
            'Primordial Balm',
            id=0x21,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details='User creates a potion of frost/fire/stone giant strength (DMG 187).',
            dc=4,
            terrain=[
                IngredientTerrain.MOUNTAIN,
                IngredientTerrain.SWAMP,
                IngredientTerrain.UNDERDARK
            ]
        )


class RockVine(Ingredient):
    """ Rock Vine ingredient """

    def __init__(self):
        super().__init__(
            'Rock Vine',
            id=0x22,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details='User creates a potion of invulnerability (DMG 188).',
            dc=4,
            terrain=[
                IngredientTerrain.HILL,
                IngredientTerrain.MOUNTAIN
            ]
        )


class ScilliaBeans(Ingredient):
    """ Scilia Beans ingredient """

    def __init__(self):
        super().__init__(
            'Scilia Beans',
            id=0x23,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.COMMON,
            details='User creates a potion of climbing (DMG 187).',
            dc=1,
            terrain=[
                IngredientTerrain.DESERT,
                IngredientTerrain.GRASSLAND
            ]
        )


class SilverHibiscus(Ingredient):
    """ Silver Hibiscus ingredient """

    def __init__(self):
        super().__init__(
            'Silver Hibiscus',
            id=0x24,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details=(
                'When consumed by target, they can unleash a random elemental breathe weapon '
                '3 times (PHB 34). Cannot be altered by other ingredients.'
            ),
            dc=4,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.UNDERDARK
            ]
        )


class TailLeaf(Ingredient):
    """ Tail Leaf ingredient """

    def __init__(self):
        super().__init__(
            'Tail Leaf',
            id=0x25,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.VERY_RARE,
            details='User creates a potion of speed (DMG 188).',
            dc=5,
            terrain=[
                IngredientTerrain.GRASSLAND,
                IngredientTerrain.HILL
            ]
        )


class VerdantNettle(Ingredient):
    """ Verdant Nettle ingredient """

    def __init__(self):
        super().__init__(
            'Verdant Nettle',
            id=0x26,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.UNCOMMON,
            details='User creates a potion of animal friendship (DMG 187).',
            dc=2,
            terrain=IngredientTerrain.FOREST
        )


class Voidroot(Ingredient):
    """ Voidroot ingredient """

    def __init__(self):
        super().__init__(
            'Voidroot',
            id=0x27,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.VERY_RARE,
            details='User creates a potion of flying (DMG 187).',
            dc=5,
            terrain=[
                IngredientTerrain.ARCTIC,
                IngredientTerrain.DESERT
            ]
        )


class WispStalks(Ingredient):
    """ Wisp Stalks ingredient """

    def __init__(self):
        super().__init__(
            'Wisp Stalks',
            id=0x28,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.VERY_RARE,
            details='User creates a potion of invisibility (DMG 188).',
            dc=5,
            terrain=[
                IngredientTerrain.FOREST,
                IngredientTerrain.UNDERDARK
            ]
        )


class WrackwortBulbs(Ingredient):
    """ Wrackwort Bulbs ingredient """

    def __init__(self):
        super().__init__(
            'Wrackwort Bulbs',
            id=0x29,
            type=IngredientType.ENCHANTMENT,
            rarity=IngredientRarity.RARE,
            details='User creates a potion of diminution (DMG 187).',
            dc=4,
            terrain=[
                IngredientTerrain.COASTAL,
                IngredientTerrain.SWAMP
            ]
        )


class Ingredients(object):
    """ Class holder for all ingredients """

    BLOODGRASS = Bloodgrass()
    DRIED_EPHEDRA = DriedEphedra()
    FENNEL_SILK = FennelSilk()
    GENGKO_BRUSH = GengkoBrush()
    HYANCINTH_NECTAR = HyancinthNectar()
    MANDRAKE_ROOT = MandrakeRoot()
    MILKWEED_SEEDS = MilkweedSeeds()
    WILD_SAGEROOT = WildSageroot()
    ARCTIC_CREEPER = ArcticCreeper()
    AMANITA_CAP = AmanitaCap()
    BASILISK_BREATH = BasiliskBreath()
    CACTUS_JUICE = CactusJuice()
    DRAKUS_FLOWER = DrakusFlower()
    FROZEN_SEEDLINGS = FrozenSeedlings()
    HARRADA_LEAF = HarradaLeaf()
    QUICKSILVER_LICHEN = QuicksilverLichen()
    RADIANT_SYNTHSEED = RadiantSynthseed()
    SPINEFLOWER_BERRIES = SpineflowerBerries()
    WYRMTONGUE_PETALS = WyrmtonguePetals()
    CHROMUS_SLIME = ChromusSlime()
    EMETIC_WAX = EmeticWax()
    LAVENDER_SPRIG = LavenderSprig()
    ARROW_ROOT = ArrowRoot()
    BLUE_TOADSHADE = BlueToadshade()
    COSMOS_GLOND = CosmosGlond()
    DEVILS_BLOODLEAF = DevilsBloodleaf()
    ELEMENTAL_WATER = ElementalWater()
    FIENDS_IVY = FiendsIvy()
    HYDRATHISTLE = Hydrathistle()
    IRONWOOD_HEART = IronwoodHeart()
    LUMINOUS_CAP_DUST = LuminousCapDust()
    MORTFLESH_POWDER = MortfleshPowder()
    NIGHTSHADE_BERRIES = NightshadeBerries()
    PRIMORDIAL_BALM = PrimordialBalm()
    ROCK_VINE = RockVine()
    SCILLIA_BEANS = ScilliaBeans()
    SILVER_HIBISCUS = SilverHibiscus()
    TAIL_LEAF = TailLeaf()
    VERDANT_NETTLE = VerdantNettle()
    VOIDROOT = Voidroot()
    WISP_STALKS = WispStalks()
    WRACKWORT_BULBS = WrackwortBulbs()

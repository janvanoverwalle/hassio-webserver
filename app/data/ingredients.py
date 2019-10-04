""" Ingredients module """


from .ingredient_properties import IngredientFunction, \
    IngredientRarity, IngredientType
from .terrain_types import TerrainTypes


class Ingredient(object):
    """ Default ingredient class """

    _name = None
    _id = None
    _type = None
    _rarity = None
    _special = None
    _function = None
    _details = None
    _dc = None
    _terrain = None
    _property = None

    @classmethod
    def name(cls, new_name=None):
        if new_name is not None:
            cls._name = new_name
        return cls._name

    @classmethod
    def id(cls, new_id=None):
        if new_id is not None:
            cls._id = new_id
        return cls._id

    @classmethod
    def type(cls, new_type = None):
        if new_type is not None:
            cls._type = new_type
        if not isinstance(cls._type, list):
            cls._type = list(cls._type)
        return cls._type

    @classmethod
    def rarity(cls, new_rarity=None):
        if new_rarity is not None:
            cls._rarity = new_rarity
        return cls._rarity

    @classmethod
    def special(cls, new_special=None):
        if new_special is not None:
            cls._special = new_special
        return cls._special

    @classmethod
    def function(cls, new_function=None):
        if new_function is not None:
            cls._function = new_function
        return cls._function

    @classmethod
    def details(cls, new_details=None):
        if new_details is not None:
            cls._details = new_details
        return cls._details

    @classmethod
    def dc(cls, new_dc=None):
        if new_dc is not None:
            cls._dc = new_dc
        return cls._dc

    @classmethod
    def terrain(cls, new_terrain = None):
        if new_terrain is not None:
            cls._terrain = new_terrain
        if not isinstance(cls._terrain, list):
            cls._terrain = list(cls._terrain)
        return cls._terrain

    @classmethod
    def property(cls, new_property = None):
        if new_property is not None:
            cls._property = new_property
        return cls._property

    @classmethod
    def to_dict(cls):
        return {
            'name': cls.name(),
            'id': cls.id(),
            'type': cls.type(),
            'rarity': cls.rarity(),
            'special': cls.special(),
            'function': cls.function(),
            'details': cls.details(),
            'dc': cls.dc(),
            'terrain': cls.terrain(),
            'property': cls.property(),
        }


###########
# Potions #
###########

class Bloodgrass(Ingredient):
    """ Bloodgrass ingredient """

    _name = 'Bloodgrass'
    _id = 0x00
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _special = True
    _function = IngredientFunction.EFFECT
    _details = (
        'Can combine with any other Potion Effect ingredient to become '
        'a food source for 1 day. Cannot be altered by other ingredients.'
    )
    _dc = 0
    _terrain = TerrainTypes.MOST


class DriedEphedra(Ingredient):
    """ Dried Ephedra ingredient """

    _name = 'Dried Ephedra'
    _id = 0x01
    _type = IngredientType.POTION
    _rarity = IngredientRarity.UNCOMMON
    _function = IngredientFunction.MODIFIER
    _details = 'Increase the dice-type by 1 size for any healing Effect.'
    _dc = 2
    _terrain = [
        TerrainTypes.DESERT,
        TerrainTypes.MOUNTAIN
    ]
    _property = {'increase_dice_type': 1}


class FennelSilk(Ingredient):
    """ Fennel Silk ingredient """

    _name = 'Fennel Silk'
    _id = 0x02
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = (
        'Stabilizes body heat to resist cold weather or wet condition penalties for 1 hour.'
        ' Cannot be altered by other ingredients.'
    )
    _dc = 2
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.UNDERDARK
    ]
    _property = {'resistance': ('cold', 3600)}


class GengkoBrush(Ingredient):
    """ Gengko Brush ingredient """

    _name = 'Gengko Brush'
    _id = 0x03
    _type = IngredientType.POTION
    _rarity = IngredientRarity.UNCOMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'Double the dice rolled of any healing Effect, but divide the total of the dice '
        'by 2 (rounding down); Then, the recipient receives that amount of healing '
        'per round for 2 rounds.'
    )
    _dc = 2
    _terrain = [
        TerrainTypes.HILL,
        TerrainTypes.UNDERDARK
    ]
    _property = {'dice_amount': '*2', 'dice_total': '*.5', 'duration': 12}


class HyancinthNectar(Ingredient):
    """ Hyancinth Nectar ingredient """

    _name = 'Hyancinth Nectar'
    _id = 0x04
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = (
        'Removes 1d6 rounds of poison in the target’s system, but cannot remove it '
        'completely. One round of poison damage will still occur at minimum.'
    )
    _dc = 1
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.GRASSLAND
    ]


class MandrakeRoot(Ingredient):
    """ Mandrake Root ingredient """

    _name = 'Mandrake Root'
    _id = 0x05
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = (
        'Reduce any disease or poison’s potency by half for 2d12 hours. '
        'Only hinders already existing poisons or diseases in the body. '
        'Cannot be altered by other ingredients.'
    )
    _dc = 0
    _terrain = TerrainTypes.MOST
    _property = {'potency': ('*.5' '2d12*3600')}


class MilkweedSeeds(Ingredient):
    """ Milkweed Seeds ingredient """

    _name = 'Milkweed Seeds'
    _id = 0x06
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'Double the dice rolled of any healing Effect, but remove all Alchemy Modifier '
        'bonuses. This modifier can stack.'
    )
    _dc = 2
    _terrain = TerrainTypes.MOST
    _property = {'dice_amount': '*2', 'alchemy_modifier': 0}


class WildSageroot(Ingredient):
    """ Wild Sageroot ingredient """

    _name = 'Wild Sageroot'
    _id = 0x07
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = 'Heals for 2d4 + Alchemy Modifier.'
    _dc = 0
    _terrain = TerrainTypes.MOST
    _property = {'effect_dice': '2d4+mod'}


###########
# Poisons #
###########

class ArcticCreeper(Ingredient):
    """ Arctic Creeper ingredient """

    _name = 'Arctic Creeper'
    _id = 0x08
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'Change poison damage to cold or necrotic damage; target is still [poisoned] for '
        '1 minute on a failed CON saving throw; this toxin is still considered '
        'poison damage when combining with other ingredients.'
    )
    _dc = 2
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.MOUNTAIN
    ]
    _property = {'damage_type': ['cold' 'necrotic']}


class AmanitaCap(Ingredient):
    """ Amanita Cap ingredient """

    _name = 'Amanita Cap'
    _id = 0x09
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = 'Changes any poison Effect to be non-lethal and only incapacitate the target.'
    _dc = 1
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.SWAMP
    ]
    _property = {'lethal': False}


class BasiliskBreath(Ingredient):
    """ Basilisk Breath ingredient """

    _name = 'Basilisk Breath'
    _id = 0x0A
    _type = IngredientType.POISON
    _rarity = IngredientRarity.VERY_RARE
    _special = True
    _function = IngredientFunction.EFFECT
    _details = (
        'Slowly paralyzes opponent. Target makes a DC 5 + Alchemy Modifier CON saving '
        'throw each turn for 4 turns. While under this affect, target is considered slowed '
        'by the slow spell. On a failed save, the target is considered [paralyzed] for '
        '4 rounds. Cannot be modified or altered by other ingredients.'
    )
    _dc = 5
    _terrain = TerrainTypes.MOUNTAIN
    _property = {'con_save': '5+mod', 'save_fail': {'condition': 'paralyzed', 'duration': 24}}


class CactusJuice(Ingredient):
    """ Cactus Juice ingredient """

    _name = 'Cactus Juice'
    _id = 0x0B
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'The target will not notice any poison damage Effect in their system until '
        'they take 5 rounds of damage from the toxin.'
    )
    _dc = 2
    _terrain = [
        TerrainTypes.DESERT,
        TerrainTypes.GRASSLAND
    ]
    _property = {'dormant': 5}


class DrakusFlower(Ingredient):
    """ Drakus Flower ingredient """

    _name = 'Drakus Flower'
    _id = 0x0C
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'Change poison damage to fire or acid damage; target is still [poisoned] for '
        '1 minute on a failed CON saving throw; this toxin is still considered '
        'poison damage when combining with other ingredients.'
    )
    _dc = 2
    _terrain = [
        TerrainTypes.DESERT,
        TerrainTypes.GRASSLAND,
        TerrainTypes.MOUNTAIN
    ]
    _property = {'damage_type': ['fire' 'acid']}


class FrozenSeedlings(Ingredient):
    """ Frozen Seedlings ingredient """

    _name = 'Frozen Seedlings'
    _id = 0x0D
    _type = IngredientType.POISON
    _rarity = IngredientRarity.RARE
    _function = IngredientFunction.MODIFIER
    _details = (
        'While [poisoned] target’s movement speed is reduced by 10 ft for 1 minute. '
        'Cannot be altered by other ingredients.'
    )
    _dc = 4
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.MOUNTAIN
    ]
    _property = {'speed': (-10, 60)}


class HarradaLeaf(Ingredient):
    """ Harrada Leaf ingredient """

    _name = 'Harrada Leaf'
    _id = 0x0E
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'While [poisoned] target has disadvantage on ability checks. '
        'Cannot be altered by other ingredients.'
    )
    _dc = 1
    _terrain = TerrainTypes.FOREST
    _property = {'disadvantage': True}


class QuicksilverLichen(Ingredient):
    """ Quicksilver Lichen ingredient """

    _name = 'Quicksilver Lichen'
    _id = 0x0F
    _type = IngredientType.POISON
    _rarity = IngredientRarity.UNCOMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'Double the dice rolled of any Toxin Effect, but reduce that Effect duration '
        'by half. This modifier can stack.'
    )
    _dc = 3
    _terrain = TerrainTypes.MOST
    _property = {'dice_amount': '*2', 'duration': '*.5'}


class RadiantSynthseed(Ingredient):
    """ Radiant Synthseed ingredient """

    _name = 'Radiant Synthseed'
    _id = 0x10
    _type = IngredientType.POISON
    _rarity = IngredientRarity.RARE
    _function = IngredientFunction.MODIFIER
    _details = (
        'Change poison damage to radiant damage; target is still [poisoned] for 1 minute '
        'on a failed CON saving throw; this toxin is still considered poison damage when '
        'combining with other ingredients.'
    )
    _dc = 2
    _terrain = TerrainTypes.UNDERDARK
    _property = {'damage_type': ['radiant']}


class SpineflowerBerries(Ingredient):
    """ Spineflower Berries ingredient """

    _name = 'Spineflower Berries'
    _id = 0x11
    _type = IngredientType.POISON
    _rarity = IngredientRarity.UNCOMMON
    _function = IngredientFunction.MODIFIER
    _details = 'Increase the dice-type by 1 size for any Toxin Effect.'
    _dc = 3
    _terrain = [
        TerrainTypes.DESERT,
        TerrainTypes.SWAMP
    ]
    _property = {'increase_dice_type': 1}


class WyrmtonguePetals(Ingredient):
    """ Wyrmtongue Petals ingredient """

    _name = 'Wyrmtongue Petals'
    _id = 0x12
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = (
        '1d4 + Alchemy Modifier poison damage per round; target is [poisoned] for '
        '1 minute on a failed CON save.'
    )
    _dc = 0
    _terrain = TerrainTypes.MOST
    _property = {
        'effect_dice': '1d4+mod',
        'con_save': '8+mod',
        'save_fail': {'condition': 'poisoned', 'duration': 60}
    }


###################
# Potions/Poisons #
###################

class ChromusSlime(Ingredient):
    """ Chromus Slime ingredient """

    _name = 'Chromus Slime'
    _id = 0x13
    _type = [
        IngredientType.POTION,
        IngredientType.POISON
    ]
    _rarity = IngredientRarity.RARE
    _special = True
    _function = IngredientFunction.MODIFIER
    _details = (
        'The final Effect after all other calculations is the exact opposite. '
        'This is up to the DM’s discretion on the specifics per potion/poison.'
    )
    _dc = 4
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.UNDERDARK
    ]
    _property = {'reverse_effect': True}


class EmeticWax(Ingredient):
    """ Emetic Wax ingredient """

    _name = 'Emetic Wax'
    _id = 0x14
    _type = [
        IngredientType.POTION,
        IngredientType.POISON
    ]
    _rarity = IngredientRarity.COMMON
    _special = True
    _function = IngredientFunction.MODIFIER
    _details = 'Delay the Effect of an ingredient this was combined with by 1d6 rounds'
    _dc = 1
    _terrain = [
        TerrainTypes.FOREST,
        TerrainTypes.SWAMP
    ]
    _property = {'delay_effect': '1d6*6'}


class LavenderSprig(Ingredient):
    """ Lavender Sprig ingredient """

    _name = 'Lavender Sprig'
    _id = 0x15
    _type = [
        IngredientType.POTION,
        IngredientType.POISON
    ]
    _rarity = IngredientRarity.COMMON
    _special = True
    _function = IngredientFunction.MODIFIER
    _details = 'Makes the potion or toxin more stable and safer to craft.'
    _dc = -2
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.GRASSLAND,
        TerrainTypes.HILL
    ]


################
# Enchantments #
################

class ArrowRoot(Ingredient):
    """ Arrow Root ingredient """

    _name = 'Arrow Root'
    _id = 0x16
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.UNCOMMON
    _details = '+1 to attack rolls for one minute when applied to a weapon.'
    _dc = 2
    _terrain = [
        TerrainTypes.DESERT,
        TerrainTypes.FOREST,
        TerrainTypes.GRASSLAND
    ]


class BlueToadshade(Ingredient):
    """ Blue Toadshade ingredient """

    _name = 'Blue Toadshade'
    _id = 0x17
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = 'User creates a potion of gaseous form (DMG 187).'
    _dc = 3
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.FOREST,
        TerrainTypes.SWAMP
    ]


class CosmosGlond(Ingredient):
    """ Cosmos Glond ingredient """

    _name = 'Cosmos Glond'
    _id = 0x18
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = 'User creates a potion of clairvoyance (DMG 187).'
    _dc = 3
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.DESERT
    ]


class DevilsBloodleaf(Ingredient):
    """ Devils Bloodleaf ingredient """

    _name = 'Devils Bloodleaf'
    _id = 0x19
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.VERY_RARE
    _details = 'User creates a potion of vitality (DMG 188).'
    _dc = 5
    _terrain = [
        TerrainTypes.HILL,
        TerrainTypes.SWAMP,
        TerrainTypes.UNDERDARK
    ]


class ElementalWater(Ingredient):
    """ Elemental Water ingredient """

    _name = 'Elemental Water'
    _id = 0x1A
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _special = True
    _details = 'This is required as the base catalyst for all Enchantment ingredients.'
    _dc = 3
    _terrain = TerrainTypes.SPECIAL


class FiendsIvy(Ingredient):
    """ Fiends Ivy ingredient """

    _name = 'Fiends Ivy'
    _id = 0x1B
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = 'User creates a potion of mind reading (DMG 188).'
    _dc = 4
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.UNDERDARK
    ]


class Hydrathistle(Ingredient):
    """ Hydrathistle ingredient """

    _name = 'Hydrathistle'
    _id = 0x1C
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.UNCOMMON
    _details = 'User creates a potion of water breathing (DMG 188).'
    _dc = 2
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.SWAMP
    ]


class IronwoodHeart(Ingredient):
    """ Ironwood Heart ingredient """

    _name = 'Ironwood Heart'
    _id = 0x1D
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.UNCOMMON
    _details = 'User creates a potion of growth (DMG 187).'
    _dc = 3
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.FOREST,
        TerrainTypes.HILL
    ]


class LuminousCapDust(Ingredient):
    """ Luminous Cap Dust ingredient """

    _name = 'Luminous Cap Dust'
    _id = 0x1E
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = 'User creates a potion of heroism (DMG 188).'
    _dc = 4
    _terrain = [
        TerrainTypes.MOUNTAIN,
        TerrainTypes.UNDERDARK
    ]


class MortfleshPowder(Ingredient):
    """ Mortflesh Powder ingredient """

    _name = 'Mortflesh Powder'
    _id = 0x1F
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.VERY_RARE
    _details = 'User creates a potion of longevity (DMG 188).'
    _dc = 5
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.UNDERDARK
    ]


class NightshadeBerries(Ingredient):
    """ Nightshade Berries ingredient """

    _name = 'Nightshade Berries'
    _id = 0x20
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.UNCOMMON
    _details = 'The effect of this “potion” is similar to the oil of slipperiness (DMG 184).'
    _dc = 3
    _terrain = [
        TerrainTypes.FOREST,
        TerrainTypes.HILL
    ]


class PrimordialBalm(Ingredient):
    """ Primordial Balm ingredient """

    _name = 'Primordial Balm'
    _id = 0x21
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = 'User creates a potion of frost/fire/stone giant strength (DMG 187).'
    _dc = 4
    _terrain = [
        TerrainTypes.MOUNTAIN,
        TerrainTypes.SWAMP,
        TerrainTypes.UNDERDARK
    ]


class RockVine(Ingredient):
    """ Rock Vine ingredient """

    _name = 'Rock Vine'
    _id = 0x22
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = 'User creates a potion of invulnerability (DMG 188).'
    _dc = 4
    _terrain = [
        TerrainTypes.HILL,
        TerrainTypes.MOUNTAIN
    ]


class ScilliaBeans(Ingredient):
    """ Scilia Beans ingredient """

    _name = 'Scilia Beans'
    _id = 0x23
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.COMMON
    _details = 'User creates a potion of climbing (DMG 187).'
    _dc = 1
    _terrain = [
        TerrainTypes.DESERT,
        TerrainTypes.GRASSLAND
    ]


class SilverHibiscus(Ingredient):
    """ Silver Hibiscus ingredient """

    _name = 'Silver Hibiscus'
    _id = 0x24
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = (
        'When consumed by target, they can unleash a random elemental breathe weapon '
        '3 times (PHB 34). Cannot be altered by other ingredients.'
    )
    _dc = 4
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.UNDERDARK
    ]


class TailLeaf(Ingredient):
    """ Tail Leaf ingredient """

    _name = 'Tail Leaf'
    _id = 0x25
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.VERY_RARE
    _details = 'User creates a potion of speed (DMG 188).'
    _dc = 5
    _terrain = [
        TerrainTypes.GRASSLAND,
        TerrainTypes.HILL
    ]


class VerdantNettle(Ingredient):
    """ Verdant Nettle ingredient """

    _name = 'Verdant Nettle'
    _id = 0x26
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.UNCOMMON
    _details = 'User creates a potion of animal friendship (DMG 187).'
    _dc = 2
    _terrain = TerrainTypes.FOREST


class Voidroot(Ingredient):
    """ Voidroot ingredient """

    _name = 'Voidroot'
    _id = 0x27
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.VERY_RARE
    _details = 'User creates a potion of flying (DMG 187).'
    _dc = 5
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.DESERT
    ]


class WispStalks(Ingredient):
    """ Wisp Stalks ingredient """

    _name = 'Wisp Stalks'
    _id = 0x28
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.VERY_RARE
    _details = 'User creates a potion of invisibility (DMG 188).'
    _dc = 5
    _terrain = [
        TerrainTypes.FOREST,
        TerrainTypes.UNDERDARK
    ]


class WrackwortBulbs(Ingredient):
    """ Wrackwort Bulbs ingredient """

    _name = 'Wrackwort Bulbs'
    _id = 0x29
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.RARE
    _details = 'User creates a potion of diminution (DMG 187).'
    _dc = 4
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.SWAMP
    ]


class Ingredients(object):
    """ Class holder for all ingredients """

    AMANITA_CAP = AmanitaCap
    ARCTIC_CREEPER = ArcticCreeper
    ARROW_ROOT = ArrowRoot
    BASILISK_BREATH = BasiliskBreath
    BLOODGRASS = Bloodgrass
    BLUE_TOADSHADE = BlueToadshade
    CACTUS_JUICE = CactusJuice
    CHROMUS_SLIME = ChromusSlime
    COSMOS_GLOND = CosmosGlond
    DEVILS_BLOODLEAF = DevilsBloodleaf
    DRAKUS_FLOWER = DrakusFlower
    DRIED_EPHEDRA = DriedEphedra
    ELEMENTAL_WATER = ElementalWater
    EMETIC_WAX = EmeticWax
    FENNEL_SILK = FennelSilk
    FIENDS_IVY = FiendsIvy
    FROZEN_SEEDLINGS = FrozenSeedlings
    GENGKO_BRUSH = GengkoBrush
    HARRADA_LEAF = HarradaLeaf
    HYANCINTH_NECTAR = HyancinthNectar
    HYDRATHISTLE = Hydrathistle
    IRONWOOD_HEART = IronwoodHeart
    LAVENDER_SPRIG = LavenderSprig
    LUMINOUS_CAP_DUST = LuminousCapDust
    MANDRAKE_ROOT = MandrakeRoot
    MILKWEED_SEEDS = MilkweedSeeds
    MORTFLESH_POWDER = MortfleshPowder
    NIGHTSHADE_BERRIES = NightshadeBerries
    PRIMORDIAL_BALM = PrimordialBalm
    QUICKSILVER_LICHEN = QuicksilverLichen
    RADIANT_SYNTHSEED = RadiantSynthseed
    ROCK_VINE = RockVine
    SCILLIA_BEANS = ScilliaBeans
    SILVER_HIBISCUS = SilverHibiscus
    SPINEFLOWER_BERRIES = SpineflowerBerries
    TAIL_LEAF = TailLeaf
    VERDANT_NETTLE = VerdantNettle
    VOIDROOT = Voidroot
    WILD_SAGEROOT = WildSageroot
    WISP_STALKS = WispStalks
    WRACKWORT_BULBS = WrackwortBulbs
    WYRMTONGUE_PETALS = WyrmtonguePetals

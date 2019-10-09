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
    _description = None

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
    def type(cls, new_type=None):
        if new_type is not None:
            cls._type = new_type
        if not isinstance(cls._type, list):
            cls._type = [cls._type]
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
    def terrain(cls, new_terrain=None):
        if new_terrain is not None:
            cls._terrain = new_terrain
        if not isinstance(cls._terrain, list):
            cls._terrain = [cls._terrain]
        return cls._terrain

    @classmethod
    def property(cls, new_property=None):
        if new_property is not None:
            cls._property = new_property
        return cls._property

    @classmethod
    def description(cls, new_description=None):
        if new_description is not None:
            cls._description = new_description
        return cls._description

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
            'description': cls.description()
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
    _description = (
        'The most boring, common plant life found in the wild is this dark brown grass. '
        'It has absolutely no remarkable qualities, other than being relatively harmless, '
        'and its use as basic sustenance for a while when properly prepared. '
        'Herbalists do not find this grass very unique, but still tend to collect it '
        'as it occupies almost no space in their packs.'
    )


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
    _description = (
        'bush often found in dry environments, it is thorny and hard to harvest without scratching '
        'your skin. It has a distinct dark purple hue when viewed at a distance, but up close '
        'it looks black. Herbalists love to use this plant when making healing tonics '
        'as it has the odd ability to enhance Wild Sageroot.'
    )


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
    _description = (
        'Often mistaken for a spider\'s web, this white web like plant grows amongst frigid '
        'and dark environments. It uses sharp hooked tendrils to help secure the edges '
        'of the plant to nearby rocks or plants. Adventurers that are adept in the use of '
        'Fennel Silk will recognize the many applications it has for protecting your extremities '
        'from harsh, low temperature environments.'
    )


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
    _description = (
        'This brown, dry brush is usually found growing between rocks and outcrops. It doesn\'t '
        'seem to require much water, instead it seems to thrive off the rocks. When plucked from '
        'its rocky bed, the brush will quickly start to deteriorate unless done properly. '
        'Herbalists have nevertheless found that when you crunch these branches, '
        'they delay (smooth out) any healing effect they\'re mixed in.'
    )


class HyancinthNectar(Ingredient):
    """ Hyancinth Nectar ingredient """

    _name = 'Hyancinth Nectar'
    _id = 0x04
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = (
        'Removes 1d6 rounds of poison in the target\'s system, but cannot remove it '
        'completely. One round of poison damage will still occur at minimum.'
    )
    _dc = 1
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.GRASSLAND
    ]
    _description = (
        'This blue and white thick liquid can be extracted from the Hyancinth\'s near somewhat wet '
        'areas. This nectar is of high demand and is often used by highly trained guards to '
        'counter poisons that evil people attempt to use on them. While it does not cure the mean '
        'of poisons, it severely limits its effects.'
    )


class MandrakeRoot(Ingredient):
    """ Mandrake Root ingredient """

    _name = 'Mandrake Root'
    _id = 0x05
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = (
        'Reduce any disease or poison\'s potency by half for 2d12 hours. '
        'Only hinders already existing poisons or diseases in the body. '
        'Cannot be altered by other ingredients.'
    )
    _dc = 0
    _terrain = TerrainTypes.MOST
    _property = {'potency': ('*.5' '2d12*3600')}
    _description = (
        'This tan root has serrated edges all along its body that often cause injury to '
        'Herbalists that do not properly know how to handle it. When stripped of its outer skin, '
        'the soft tender center can be eaten with relative ease and is often used by Doctors '
        'to reduce pain from poison or disease.'
    )


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
    _description = (
        'These small, white translucent seeds can be found when opening up a Milkweed Flower. '
        'They are often eaten by children due to their friendly look, but can cause negative '
        'digestive effects this way. When crushed up and diluted with other liquid these seeds '
        'offer very powerful healing effects.'
    )


class WildSageroot(Ingredient):
    """ Wild Sageroot ingredient """

    _name = 'Wild Sageroot'
    _id = 0x07
    _type = IngredientType.POTION
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = 'Heals for 1d4 + Alchemy Modifier.'
    _dc = 1
    _terrain = TerrainTypes.MOST
    _property = {'effect_dice': '1d4+mod'}
    _description = (
        'The most common ingredient found among doctor\'s and healer\'s equipment would be these '
        'light pink roots. They measure about 3 to 5 inches in length and have a smooth, fuzzy '
        'texture to them. They are used every day by skilled Alchemists and healers to create '
        'concoctions of extraordinary healing power.'
    )


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
    _description = (
        'This noxious weed usually grows in extremely cold environments, or at higher elevations '
        'where snow tends to accumulate. The leaves of the plant are characterized by a pleasant '
        'sweet minty flavor, whereas the root is bitter and acidic. The weed is one of an '
        'assassin\'s favorite plants, due to the root\'s ability to freeze a creature\'s '
        'bloodstream, which leads to a slow and agonizing death. Arctic Creeper is toxic to many '
        'unwary travelers, as it is quite easy to consume the root\'s toxins while enjoying '
        'the sweet flavorsome leaves.'
    )


class AmanitaCap(Ingredient):
    """ Amanita Cap ingredient """

    _name = 'Amanita Cap'
    _id = 0x09
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = 'Changes any poison Effect to be non-lethal and only incapacitates the target.'
    _dc = 1
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.SWAMP
    ]
    _property = {'lethal': False}
    _description = (
        'This large mushroom is often found growing in clusters near bodies of water, or around '
        'other damp terrain. It has a bold blue stem accompanied by a large red cap, which makes '
        'this fungi extremely easy to identify. Professional herbalists often cut the head from '
        'the root, as the mushroom has the rare ability to re-grow its cap within a few short '
        'weeks.'
    )


class BasiliskBreath(Ingredient):
    """ Basilisk Breath ingredient """

    _name = 'Basilisk\'s Breath'
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
    _description = (
        'Often referred to as Grey Restraints amongst the nobles of the world, this dark grey vine '
        'is only rarely found atop the highest peaks of mountainous regions. It is fabled that '
        'this vine is a gift from the gods, as a way to test humanity. Often sold for outrageous '
        'sums of gold, Basilisk\'s Breath can attract unwanted attention to those trying to sell '
        'it for profit.'
    )


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
    _description = (
        'This usually clear liquid can be found within most cacti around the world. It\'s '
        'reasonably difficult to extract, as many cacti are dangerous to work with. Brewers love '
        'to use this juice in many recipes, as one of its effects is to delay alcohol '
        'intoxication, allowing people to purchase and consume more before it hits them.'
    )


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
    _description = (
        'This bright red and pale green flower can be found in both temperate and warm '
        'environments. It\'s a natural favorite amongst entertainers, due to the petal\'s ability '
        'to ignite with a moderate application of friction. This ignition does not cause harm, '
        'but instead creates theatrical sparks with the ability to light fires and create warmth.'
    )


class FrozenSeedlings(Ingredient):
    """ Frozen Seedlings ingredient """

    _name = 'Frozen Seedlings'
    _id = 0x0D
    _type = IngredientType.POISON
    _rarity = IngredientRarity.RARE
    _function = IngredientFunction.MODIFIER
    _details = (
        'While [poisoned] target\'s movement speed is reduced by 10 ft for 1 minute. '
        'Cannot be altered by other ingredients.'
    )
    _dc = 4
    _terrain = [
        TerrainTypes.ARCTIC,
        TerrainTypes.MOUNTAIN
    ]
    _property = {'speed': (-10, 60)}
    _description = (
        'These small, pea sized pods can be found amongst resilient flowers in very cold '
        'environments. Named for their almost frozen appearance, they can be plucked with relative '
        'ease and are often used in cold alcoholic drinks. Some assassins have found ways to crush '
        'these into a paste and hamper one\'s movements.'
    )


class HarradaLeaf(Ingredient):
    """ Harrada Leaf ingredient """

    _name = 'Harrada Leaf'
    _id = 0x0E
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.MODIFIER
    _details = (
        'While [poisoned], target has advantage on a single type of ability '
        'check followed by disadvantage on that same type of ability check '
        'for 1d4 hours. Cannot be altered by other ingredients.'
    )
    _dc = 1
    _terrain = TerrainTypes.FOREST
    _property = {'disadvantage': True}
    _description = (
        'This huge yellow leaf can often be found near tree tops in lush environments. It is often '
        'cultivated and harvested by gangs or the Thieves Guilds to be sold as a street drug. '
        'The potent nature of this addictive substance will cause a brief euphoric state coupled '
        'with an increase in a specific attribute; followed by a long recovery period in which the '
        'user is extremely weakened in that attribute.'
    )


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
    _description = (
        'This silver and grey silky moss can be found growing amongst almost any substance as it '
        'seems to ignore environmental standards. Assassins have been able to use this lichen to '
        'quickly administer their toxins into the target\'s system without any drawbacks. However, '
        'this takes some preparation and is often forgotten by common folk.'
    )


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
    _description = (
        'This long black and boat shaped seed emanates a strong yellow glow, and often exerts the '
        'smell of flowers. When the seed is cracked open, a person can find a few smaller looking '
        'seeds of the same nature. These smaller seeds can often be crushed or blended into '
        'mixtures to enhance toxins.'
    )


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
    _description = (
        'Often found hanging amongst the bone-like flowers, this white berry can be harvested and '
        'crushed to enhance toxins made by scoundrels. However, this effect only applies when '
        'introduced directly to the bloodstream. When ingested normally these berries provide '
        'little sustenance, but do not harm the person.'
    )


class WyrmtonguePetals(Ingredient):
    """ Wyrmtongue Petals ingredient """

    _name = 'Wyrmtongue Petals'
    _id = 0x12
    _type = IngredientType.POISON
    _rarity = IngredientRarity.COMMON
    _function = IngredientFunction.EFFECT
    _details = (
        '1d4 + Alchemy Modifier poison damage and target is [poisoned] for '
        '1 minute on a failed CON save.'
    )
    _dc = 1
    _terrain = TerrainTypes.MOST
    _property = {
        'effect_dice': '1d4+mod',
        'con_save': '8+mod',
        'save_fail': {'condition': 'poisoned', 'duration': 60}
    }
    _description = (
        'Assassins\', and many Drows, favorite natural ingredient. These jagged red petals can be '
        'found growing on Wyrmtongue flowers in almost every terrain. It\'s almost as if the world '
        'itself is trying to test humanity by letting these flowers grow everywhere. These petals '
        'are used as a base for toxins that can offer extremely powerful damage. For this reason, '
        'Wyrmtongue is highly illegal, and in some cases punishes owners of this flower with death.'
    )


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
        'This is up to the DM\'s discretion on the specifics per potion/poison.'
    )
    _dc = 4
    _terrain = [
        TerrainTypes.COASTAL,
        TerrainTypes.UNDERDARK
    ]
    _property = {'reverse_effect': True}
    _description = (
        'This thin, slimy substance is often observed to flow within water current as if it had a '
        'mind of its own. Often times, scientists mistake this slime with mercury, as it has the '
        'same consistency and look. When attempting to alter the slime, it reverberates and alters '
        'the other plant life it touches instead.'
    )


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
    _description = (
        'This thick, white wax is often found seeping out of trees near lush and wet areas. It is '
        'commonly used in candle making, as the wax melts and rehardens rather quickly, yet is '
        'strong enough to form delicate shapes. Herbalists use it to control how their tonics '
        'enter the body, performing miraculous feats.'
    )


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
    _description = (
        'These long stemmed purple-petal flowers can often be found swaying in the wind in huge '
        'patches. They are very common amongst green environments and have a distinct sweet smell. '
        'However, they taste extremely bitter when eaten.'
    )


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
    _description = (
        'This unusually elongated plant can stand up to four feet tall, and is very easy to spot '
        'due to its distinctive white and brown speckled pattern. The Arrow Root thrives in desert '
        'and drought environments, as the plant needs very little water to survive. When diced and '
        'boiled in water the plant creates a frothy silver liquid, which is ideal for sharpening '
        'and polishing weapons and armor without the use of magic or other means.'
    )


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
    _description = (
        'Another common mushroom is this dark blue cap with a yellow striped stem. When disturbed, '
        'this mushroom lets off a puff of blue powder. Usually this causes no permanent harm to '
        'the surrounding creatures, but it can stain their skin and equipment for a short while. '
        'The powder is commonly used to color various inks and dyes. Herbalists usually search for '
        'the fungi around small watering holes, where aquatic life often thrives.'
    )


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
    _description = (
        'This uncommon four-leafed plant is notorious for being somewhat difficult to find. This '
        'is mostly due to the plant growing about 5 feet underneath the ground, and only peeking '
        'out during its final maturity. However, it has an uncanny look of the stars in a night '
        'sky amongst its leaves.'
    )


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
    _description = (
        'Only a few recorded instances of this red and yellow flower exist. This large and bold '
        'red leaf can be found going back in history to the dawn of humankind. It was once a '
        'popular decoration around homes and gardens, but has become one of the rarest plants in '
        'the world. It is said to give immense vitality and health to one who can properly prepare '
        'the plant.'
    )


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
    _description = (
        'This unique liquid shares properties of the planar realms of the 4 elements. At times you '
        'can see rocks floating unnaturally in the middle and at other times you can swear you see '
        'fire in the water. This special water can be found in all environments as it is not bound '
        'to our physical world\'s rules.'
    )


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
    _description = (
        'These long, red thorn-encrusted vines can stretch up to 3 feet long and have sharp thorns '
        'that reach up to an inch or two long. It isn\'t rare to find blood stains amongst these '
        'vines as many animals and adventurers can easily trip or get caught in a bushel of the '
        'vines. The vines also seem to have a sentient quality to them as they relax when prey is '
        'near, and contract when captured.'
    )


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
    _description = (
        'Named for its appearance, this threepronged blue and black flower is often found in dark '
        'and dank environments. When used alone, the thistle has no real beneficial effects. '
        'However, skilled alchemists have been able to use highly powerful and natural water to '
        'concoct potions that allow them to breath in water.'
    )


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
    _description = (
        'This gnarled white seed is commonly found in the nooks of Ironwood Trees. These large '
        'seeds pulse with a slow repetitive beat when gripped tightly, often referred to as '
        '"Nature\'s Heartbeat". It is said that when cooked or properly prepared by a Herbalist '
        'these seeds can increase a beings physical size greatly.'
    )


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
    _description = (
        'This powder can be shook from the glowing yellow mushrooms often found in extremely dark '
        'environments and it keeps an ember-like glow for about a week after extracted. Many '
        'Herbalists keep the glowing mushrooms themselves in dark cellars in order to harvest this '
        'dust every chance they get.'
    )


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
    _description = (
        'This dark purple powder is often found growing on top of moss in dark, cold environments. '
        'This powder is often used as makeup for young men and women to reduce the look of age '
        'from their faces. When imbibed with a magical catalyst, the effect is said to be '
        'permanent when consumed.'
    )


class NightshadeBerries(Ingredient):
    """ Nightshade Berries ingredient """

    _name = 'Nightshade Berries'
    _id = 0x20
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.UNCOMMON
    _details = 'The effect of this "potion" is similar to the oil of slipperiness (DMG 184).'
    _dc = 3
    _terrain = [
        TerrainTypes.FOREST,
        TerrainTypes.HILL
    ]
    _description = (
        'These light blue berries can be found in small clumped packs among small bushes in lush '
        'environments. They can be safely ingested and are often eaten by wild animals for their '
        'sweet, but tangy flavor. A skilled Herbalist can enhance the berries\' natural ability to '
        'affect a persons body.'
    )


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
    _description = (
        'This thick substance has been observed changing its coloring, almost at will. The balm is '
        'unusually warm to the touch, and can seem to retain heat for weeks on end. Herbalists '
        'often find this substance growing on rocks in humid environments. The exact rarity of the '
        'substance is unknown, as its constantly changing appearance makes it difficult to '
        'identify.'
    )


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
    _description = (
        'This extremely hardened dark green vine can be found growing in the ground near very old '
        'minerals, often seeming to feed off the minerals themselves. At first glance this vine '
        'seems completely useless to mortals, but arcane studies have shown this vine to harden a '
        'person\'s skin significantly if combined with a powerful catalyst.'
    )


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
    _description = (
        'These light brown beans can occasionally be found hanging from Scillia Bushes in dry '
        'atmosphere environments. They are often used to enhance flavors in stew and other meals, '
        'but have a much stranger effect. At full potency, some of these beans can offer the user '
        'the ability to climb steep cliffs and rock faces with ease.'
    )


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
    _description = (
        'This silver-grey plant looks as though it represents madness itself. It often has random '
        'patterns and unplanned shapes, but always has a black web-like pattern on it. Although it '
        'may look deadly to touch, when prepared properly a Herbalist can unleash a torrent of '
        'elemental power representing a breath weapon.'
    )


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
    _description = (
        'This very fuzzy, dark green leaf looks like a circle with three thick strands hanging '
        'from it. When held, the leaf itself feels as though it is vibrating. It is known that a '
        'skilled Herbalist can use these leaves in concoctions to create powerful magical effects '
        'to enhance one\'s speed.'
    )


class VerdantNettle(Ingredient):
    """ Verdant Nettle ingredient """

    _name = 'Verdant Nettle'
    _id = 0x26
    _type = IngredientType.ENCHANTMENT
    _rarity = IngredientRarity.UNCOMMON
    _details = 'User creates a potion of animal friendship (DMG 187).'
    _dc = 2
    _terrain = TerrainTypes.FOREST
    _description = (
        'With its dark green and yellow speckled mesh, this plant can be easily spotted. It '
        'normally grows in forests and can catch a person\'s feet when traveling if they do not '
        'have proper footing. Alchemists like to use this plant to create tonics that enhance '
        'one\'s strength and reflexes.'
    )


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
    _description = (
        'This dark grey thick root is often found amongst the most extreme environments. It '
        'normally grows in either desert or arctic environments and seems to vary in growth rate '
        'per root. Herbalists tend to be very careful when they extract this root from the ground, '
        'as it seems to defy gravity and want to "fly" away.'
    )


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
    _description = (
        'This incredibly rare fungi has become something of a fable amongst herbalists. It is '
        'reported to have a large bulbous cap growing atop a thin stem, and to normally form in '
        'small clusters deep within damp cave environments and forests. The organism is usually a '
        'translucent blue, and is rumored to render creatures invisible once consumed.'
    )


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
    _description = (
        'These huge white bulbs can be found on small yellow mushrooms often found in swamps or '
        'wet caverns. The mushroom releases a puff of powder from these bulbs when threatened and '
        'it tends to confuse and hinder a person. When harvested successfully, these bulbs can be '
        'ground into a paste and imbibed within magical water to diminish the size of a being.'
    )


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

    @classmethod
    def to_list(cls, exclude=None):
        res_list = sorted([
            cls.AMANITA_CAP,
            cls.ARCTIC_CREEPER,
            cls.ARROW_ROOT,
            cls.BASILISK_BREATH,
            cls.BLOODGRASS,
            cls.BLUE_TOADSHADE,
            cls.CACTUS_JUICE,
            cls.CHROMUS_SLIME,
            cls.COSMOS_GLOND,
            cls.DEVILS_BLOODLEAF,
            cls.DRAKUS_FLOWER,
            cls.DRIED_EPHEDRA,
            cls.ELEMENTAL_WATER,
            cls.EMETIC_WAX,
            cls.FENNEL_SILK,
            cls.FIENDS_IVY,
            cls.FROZEN_SEEDLINGS,
            cls.GENGKO_BRUSH,
            cls.HARRADA_LEAF,
            cls.HYANCINTH_NECTAR,
            cls.HYDRATHISTLE,
            cls.IRONWOOD_HEART,
            cls.LAVENDER_SPRIG,
            cls.LUMINOUS_CAP_DUST,
            cls.MANDRAKE_ROOT,
            cls.MILKWEED_SEEDS,
            cls.MORTFLESH_POWDER,
            cls.NIGHTSHADE_BERRIES,
            cls.PRIMORDIAL_BALM,
            cls.QUICKSILVER_LICHEN,
            cls.RADIANT_SYNTHSEED,
            cls.ROCK_VINE,
            cls.SCILLIA_BEANS,
            cls.SILVER_HIBISCUS,
            cls.SPINEFLOWER_BERRIES,
            cls.TAIL_LEAF,
            cls.VERDANT_NETTLE,
            cls.VOIDROOT,
            cls.WILD_SAGEROOT,
            cls.WISP_STALKS,
            cls.WRACKWORT_BULBS,
            cls.WYRMTONGUE_PETALS
        ], key=lambda i: i.name())

        if exclude:
            if not isinstance(exclude, (list, tuple)):
                exclude = [exclude]
            for e in exclude:
                if e not in res_list:
                    continue
                res_list.remove(e)

        return res_list

    @classmethod
    def retrieve(cls, ingredient, key=None):
        if not key:
            return [i for i in cls.to_list() if i == ingredient]

        ret = []
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        for i in cls.to_list():
            k = key(i)
            if isinstance(k, str):
                s1 = ''.join([c for c in k.lower() if c in allowed_chars])
                s2 = ''.join([c for c in ingredient.lower() if c in allowed_chars])
                if s1 == s2:
                    ret.append(i)
        return ret

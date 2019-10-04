class TerrainTypes(object):
    """ Ingredient terrain enum """

    MOST = 'Most Terrain'
    ARCTIC = 'Arctic'
    COASTAL = 'Coastal'
    DESERT = 'Desert'
    FOREST = 'Forest'
    GRASSLAND = 'Grassland'
    HILL = 'Hill'
    MOUNTAIN = 'Mountain'
    SWAMP = 'Swamp'
    UNDERDARK = 'Underdark'
    UNDERWATER = 'Underwater'
    SPECIAL = 'Special'

    @classmethod
    def to_list(cls):
        return sorted([
            cls.MOST,
            cls.ARCTIC,
            cls.COASTAL,
            cls.DESERT,
            cls.FOREST,
            cls.GRASSLAND,
            cls.HILL,
            cls.MOUNTAIN,
            cls.SWAMP,
            cls.UNDERDARK,
            cls.UNDERWATER,
            cls.SPECIAL
        ])

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
    def to_list(cls, exclude=None):
        res_list = sorted([
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

        if exclude:
            if not isinstance(exclude, (list, tuple)):
                exclude = list(exclude)
            for e in exclude:
                if e not in res_list:
                    continue
                res_list.remove(e)

        return res_list

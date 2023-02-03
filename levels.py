"""
Exp calculation for a given level and exp group
"""
import bisect


class EXPGroup:

    def __init__(self, groupname):

        functions = {'erratic': self.erratic,
                     'fast': self.fast,
                     'medfast': self.medfast,
                     'medslow': self.medslow,
                     'slow': self.slow,
                     'fluctuating': self.fluctuating
                     }

        # build and cache a level table for this group
        self._table = {i: functions[groupname](i) for i in range(1, 101)}
        self._name = groupname

    @property
    def name(self):
        return self._name

    @property
    def table(self):
        return self._table

    def get_exp(self, lvl: int) -> int:
        return self.table[lvl]

    def get_lvl(self, exp: int) -> int:
        # get cached list of exp vals
        lvls = list(self.table.values())
        # insert our test exp value into this list
        bisect.insort(lvls, exp)
        # index the inserted value
        point = lvls.index(exp)

        return point

    @staticmethod
    def erratic(lvl):
        if lvl < 50:
            val = (lvl ** 3) * (100 - lvl) / 50
        elif lvl < 68:
            val = (lvl ** 3) * (150 - lvl) / 100
        elif lvl < 98:
            val = (lvl ** 3) * ((1911 - (10 * lvl)) / 3) / 500
        else:
            val = (lvl ** 3) * (160 - lvl) / 100
        return int(val)

    @staticmethod
    def fast(lvl):
        return int(4 * lvl ** 3 / 5)

    @staticmethod
    def medfast(lvl):
        return int(lvl ** 3)

    @staticmethod
    def medslow(lvl):
        return int((6 / 5) * lvl ** 3 - 15 * lvl ** 2 + 100 * lvl - 140)

    @staticmethod
    def slow(lvl):
        return int(5 * lvl ** 3 / 4)

    @staticmethod
    def fluctuating(lvl):
        if lvl < 15:
            val = ((lvl ** 3) * (((lvl + 1) / 3) + 24)) / 50
        elif lvl < 36:
            val = (lvl ** 3) * (lvl + 14) / 50
        else:
            val = ((lvl ** 3) * ((lvl / 2) + 32)) / 50
        return int(val)


if __name__ == '__main__':
    grp = EXPGroup('fast')

    print('1', grp.get_lvl(1))
    print('75', grp.get_lvl(350214))
    print('76', grp.get_lvl(352214))
    print('100', grp.get_lvl(350000214))

    print('0', grp.get_exp(1))
    print('6', grp.get_exp(2))
    print('563975', grp.get_exp(89))
    print('776239', grp.get_exp(99))
    print('800000', grp.get_exp(100))

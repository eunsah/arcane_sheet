'''
class that handles ARC object
'''
from datetime import datetime, timedelta, date
level_exp = [
    1,      11,     15,     20,     27,
    36,     47,     60,     75,     92,
    111,    132,    155,    180,    207,
    236,    267,    300,    335,    372
    ]
max_level = 20

class ARC():
    '''
    ARC object class
    _level : current level for ARC
    _exp : current exp for ARC
    _value : current net exp for ARC
    '''
    def __init__(self, name, level = 0, exp = 0, income = 0, value = 0):
        # init all values with 0
        self._income = 0
        self._level = 0
        self._exp = 0
        self._value = 0
        self._selector = 0
        self._future = (0, 0)

        if (level != 0 and exp != 0) and value != 0:
            raise ValueError('Only initialize (level, exp) or value')
        elif value != 0:
            self.value = value
        else:
            self.level = level
            self.exp = exp

        self._income = income
        self._name = name

## -- Setter/Getter --
    @property
    def name(self):
        # name getter
        return self._name

    @property
    def level(self):
        # arc level getter
        return self._level

    @level.setter
    def level(self, new_level):
        # arc level setter
        if new_level > max_level:
            new_level = max_level
        self._level = new_level
        self.convert_to_value()

    @property
    def exp(self):
        # arc exp getter
        return self._exp

    @exp.setter
    def exp(self, new_exp):
        # arc exp setter
        max_exp = sum(level_exp)
        if new_exp > max_exp:
            new_exp = max_exp
        self._exp = new_exp
        self.convert_to_value()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # private function to set net exp
        max_value = sum([xp for xp in level_exp])
        if new_value > max_value:
            new_value = max_value
        self._value = new_value
        self.convert_to_level()

    @property
    def income(self):
        # income getter
        return self._income

    @income.setter
    def income(self, gain):
        # income setter
        if gain >= 0:
            self._income = gain
        else:
            raise ValueError('Can\'t set negative income')

    @property
    def force(self):
        # arcane force getter
        if self._level <= 0:
            return 0
        else:
            return self._level*10 + 30

## -- Dates --
    def _remain_days(self, future = False):
        # calculate remaining days, returns float
        max_value = sum([xp for xp in level_exp])
        if future:
            value = self._value + self._selector
        else:
            value = self._value
        if value >= max_value:
            return 'Done'
        if self._income <= 0:
            return '-'

        remain_val = max_value - value
        remain_d = remain_val / self._income

        return str(remain_d)

    def due_days(self, future = False):
        res = self._remain_days(future)
        if res in ['Done', '-']:
            return res
        return int(float(res)+.9)

    def due_date(self, future = False):
        res = self._remain_days(future)
        if res in ['Done', '-']:
            return res
        return date.today() + timedelta(days = int(float(res)+.9))

## -- Future --
    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, count):
        self._selector = count
        self.future_convert_to_level

    @property
    def future_level(self):
        return self._future[0]

    @property
    def future_exp(self):
        return  self._future[1]

    @property
    def future_convert_to_level(self):
        value = self._value + self._selector
        self._future = self._convert_to_level(value)

## -- Others --
    def convert_to_value(self):
        # update level, exp -> value
        self._value = sum([level_exp[stage] for stage in range(self._level)])
        self._value += self._exp

    def convert_to_level(self):
        # update value -> level, exp
        self.level, self.exp = self._convert_to_level(self._value)

    def _convert_to_level(self, value):
        level, exp = 0, 0

        if value == 2679:
            return 20, 0
        elif value > 2679:
            value -= 2679
            return 20, value

        while True:
            if value < level_exp[level]:
                exp = value
                break
            else:
                value -= level_exp[level]
                level += 1

        return level, exp

    @property
    def info(self):
        print (f'{self._name} lv:{self._level} exp:{self._exp} value:{self._value}')
        print (f'Selector:{self._selector} future:{self._future}')

if __name__ == '__main__':
    print('arc test')
    a = ARC(name = 'arc', level = 2, exp = 4, value = 0)
    a.info
    a.exp = 20
    a.info
    a.level = 5
    a.info
    a.value = 324
    a.info

    print ('brc test')
    b = ARC(name = 'brc', level = 0,  exp = 0, value = 451)
    b.info
    b.exp = 45
    b.info
    b.level = 2
    b.info
    b.value = 591
    b.info

    print ('crc text')
    c = ARC(name = 'crc')
    c.info
    c.selector = 2927
    c.info


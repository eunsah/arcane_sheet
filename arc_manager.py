'''
ARC symbol manager class
'''
from arc import ARC
prefix = ['VJ', 'CC', 'LA', 'AR', 'MO', 'ES']

class ARC_Manager():
    def __init__(self):
        self.arc_prefix = ['VJ', 'CC', 'LA', 'AR', 'MO', 'ES']
        self.arc_id = ['Vanishing', 'ChuChu', 'Lachelein', 'Arcana', 'Morass', 'Esfera']
        self.symbol = dict()
        self.arc_init()

    def arc_init(self):
        for it in range(6):
            self.symbol[self.arc_prefix[it]] = ARC(self.arc_id[it])
## -- Property --
    @property
    def total_af(self):
        return  sum([arc.force for arc in self.symbol.values()])

    def get_level(self, id):
        return self.symbol[id].level

    def set_level(self, id, level):
        self.symbol[id].level = level

    def get_exp(self, id):
        return self.symbol[id].exp

    def set_exp(self, id, exp):
        self.symbol[id].exp = exp

    def get_income(self, id):
        return self.symbol[id].income

    def set_income(self, id, income):
        self.symbol[id].income = income

    def add_income(self, id, value):
        self.symbol[id].income += value

    def rem_income(self, id, value):
        self.symbol[id].income -= value

    def _remain_float(self, id, future=False):
        return self.symbol[id]._remain_days(future)

    def get_days(self, id, future=False):
        return self.symbol[id].remain_days(future)

    def get_date(self, id, future=False):
        return self.symbol[id].due_date(future)

## -- Selector --
    def add_selector(self, id, value=1):
        self.symbol[id].selector += value

    def _remain_float_fliter(self, id):
        res = self._remain_float(id, future=True)
        if res in ['Done', '-']:
            return  0
        return float(res)

    def distribute_selectors(self, select):
        while select != 0:
            remain_list = [self._remain_float_fliter(p) for p in self.arc_prefix]
            max_days = max(remain_list)
            if max_days < 0:
                break
            for p in self.arc_prefix:
                if self._remain_float_fliter(p) == max_days:
                    self.add_selector(p)
                    select -= 1
                    if select == 0:
                        break

if __name__ == '__main__':
    print ('--- start ---')

    a = ARC_Manager()

    def get_all_date():
        for p in prefix:
            print(a.get_date(p, future=True))

    # a.set_level('VJ', 20)
    # a.set_exp('CC', 375)

    a.set_income('VJ', 8)
    a.set_income('CC', 4)
    a.set_income('LA', 4)
    a.set_income('AR', 8)
    a.set_income('MO', 8)
    a.set_income('ES', 8)

    get_all_date()

    print ('Sending Selectors')
    a.distribute_selectors(4000)

    get_all_date()



    print ('--- end ---')

'''
ARC symbol manager class
'''
from arc import ARC

class ARC_Manager():
    def __init__(self):
        self.arc_prefix = ['VJ', 'CC', 'LA', 'AR', 'MO', 'ES']
        self.arc_id = ['Vanishing', 'ChuChu', 'Lachelein', 'Arcana', 'Morass', 'Esfera']
        self.symbol = dict()
        self._arc_init()

    def _arc_init(self):
        for it in range(6):
            self.symbol[self.arc_prefix[it]] = ARC(self.arc_id[it])

## -- Import --
    def setup(self, level, exp, income, add):
        for it in range(6):
            p = self.arc_prefix[it]
            self.set_level(p, level[it])
            self.set_exp(p, exp[it])
            self.set_income(p, income[it])
            self.add_income(p, add[it])

## -- Setter/Getter --
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
        return self.symbol[id].due_days(future)

    def get_date(self, id, future=False):
        return self.symbol[id].due_date(future)

    def get_name(self, id):
        return self.symbol[id].name

## -- Selector --
    def get_selector(self, id):
        return self.symbol[id].selector

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

## -- Output --
    def output(self):
        for p in self.arc_prefix:
            name = p
            level = str(self.get_level(p)).rjust(2)
            exp = str(self.get_exp(p)).rjust(3)
            current = self.get_date(p)
            future = self.get_date(p, True)
            selector = str(self.get_selector(p)).ljust(5)
            print(  name,
                    ' | ',
                    level,
                    exp,
                    ' | ',
                    current,
                    ' == ' if current == future else ' -> ',
                    future,
                    ' | ',
                    selector
                    )

if __name__ == '__main__':
    print ('--- start ---')
    arc = ARC_Manager()

    level =   [0, 0, 0, 0, 0, 0]
    exp =     [0, 0, 0, 0, 0, 0]
    income =  [8, 4, 4, 4, 8, 8]
    add =     [6, 15, (100+24)/30, 30/3, 0, 0]

    arc.setup(level, exp, income, add)

    arc.distribute_selectors(1000)

    arc.output()

    print ('--- end ---')

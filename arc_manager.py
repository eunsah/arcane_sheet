'''
ARC symbol manager class
'''
from arc import ARC
from timeit import default_timer as timer

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

    def _remain_days_float(self, id):
        res = self.symbol[id]._remain_days(future=True)
        if res in ['Done', '-']:
            return 0
        return float(res)

    def _return_top_value(self) -> str:
        # finds top value for finish date and return prefix string
        top_value = {'empty':0.0}
        for p in self.arc_prefix:
            new_value = self._remain_days_float(p)
            list_value = list(top_value.values())[0]
            if new_value < list_value:
                continue
            elif new_value > list_value:
                top_value.clear()
                top_value[p] = new_value
            elif new_value == list_value:
                top_value[p] = new_value
        return top_value.keys()

    def distribute_selectors(self, select):
        while select != 0:
            finish_list = self._return_top_value()
            if list(finish_list)[0] == 'empty':
                break
            for symbol_name in list(finish_list):
                self.add_selector(symbol_name)
                select -= 1
                if select == 0:
                    break

## -- Output --
    @property
    def output(self):
        for p in self.arc_prefix:
            name = self.get_name(p).ljust(10)
            level = str(self.get_level(p)).rjust(2)
            exp = str(self.get_exp(p)).rjust(3)
            current = self.get_date(p)
            future = self.get_date(p, future = True)
            current_d = str(self.get_days(p)).rjust(3)
            future_d = str(self.get_days(p, future = True)).rjust(3)
            selector = str(self.get_selector(p)).rjust(4)
            print(  name,
                    '|',
                    level,
                    exp,
                    '|',
                    current,
                    '==' if current == future else '->',
                    future,
                    '|',
                    current_d,
                    '==' if current_d == future_d else '->',
                    future_d,
                    '|',
                    selector,
                    )

if __name__ == '__main__':
    print ('--- start ---')
    start = timer()
    arc = ARC_Manager()

    selectors = 1000

    level =   [13, 15, 13, 13, 10, 10]
    exp =     [64, 77, 17, 48, 29, 36]
    income =  [8, 4, 4, 4, 8, 8]
    add =     [6, 15, (100+24)/30, 30/3, 0, 0]
    arc.setup(level, exp, income, add)

    arc.distribute_selectors(selectors)
    print (f'Distributing {selectors} selectors')
    arc.output

    end = timer() - start
    print ('--- end ---')
    print (f'total execution time : {round(end*1000, 2)} milliseconds')

'''
ARC symbol manager class
'''
from arc import ARC
from timeit import default_timer as timer
import os, json

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
        _income =  [8, 4, 4, 4, 8, 8]
        _add =     [6, 15]
        for it in range(6):
            p = self.arc_prefix[it]
            self.set_level(p, level[it])
            self.set_exp(p, exp[it])
            if income[it]:
                self.set_income(p, _income[it])
            if it in [0, 1] and add[it]:
                self.add_income(p, _add[it])
            if it == 2 and add[it]:
                self.add_income(p, (add[it]+24)/30)
            if it == 3 and add[it]:
                self.add_income(p, add[it]/3)

    @property
    def json_save(self):
        symbol_dict = dict()
        for pid in self.arc_prefix:
            symbol_dict[pid] = dict()
            symbol_dict[pid]['level'] = self.get_level(pid)
            symbol_dict[pid]['exp'] = self.get_exp(pid)
            symbol_dict[pid]['income'] = self.get_income(pid)
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path, 'save'), 'w') as o_file:
            json.dump(symbol_dict, o_file, indent=4)

    @property
    def json_load(self):
        symbol_dict = dict()
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path, 'save'), 'r') as o_file:
            symbol_dict = json.load(o_file)

        for pid in self.arc_prefix:
            self.set_level(pid, symbol_dict[pid]['level'])
            self.set_exp(pid, symbol_dict[pid]['exp'])
            self.set_income(pid, symbol_dict[pid]['income'])

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

    def clear_selectors(self):
        for pid in self.arc_prefix:
            self.symbol[id].selector = 0

    def top_symbols(self) -> list:
        top_value = {'empty':0.0}
        for pid in self.arc_prefix:
            remain_d = self.symbol[pid]._remain_days(future=True)
            days_float = 0 if remain_d in ['Done', '-'] else float(remain_d)
            days_float_list = list(top_value.values())[0]
            if days_float < days_float_list:
                continue
            elif days_float > days_float_list:
                top_value.clear()
                top_value[pid] = days_float
            elif days_float == days_float_list:
                top_value[pid] = days_float
        return list(top_value.keys())

    def distribute_selectors(self, select):
        while select != 0:
            finish_list = self.top_symbols()
            if finish_list[0] == 'empty':
                break
            for symbol_name in finish_list:
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

def test():
    arc = ARC_Manager()
    selectors = 1000

    level =   [13, 15, 13, 13, 10, 10]
    exp =     [64, 77, 17, 48, 29, 36]
    income =  [True, True, True, True, True, True]
    add =     [True, True, 300, 30]
    arc.setup(level, exp, income, add)

    arc.distribute_selectors(selectors)
    print (f'Distributing {selectors} selectors')
    arc.output

def get_int_max(string, max_val) -> int:
    while True:
        foo = input(string)
        if foo.isdigit():
            if int(foo) <= max_val:
                return int(foo)
            else:
                print ('Value mustn\'t exceed', max_val)
        else:
            print ('Value must be integer')

def get_bool(string) -> bool:
    while True:
        foo = input(string).lower()
        if foo in ['x', 'o']:
            return True if foo == 'o' else False
        else:
            print('Please answer the question with \'o\' or \'x\'')

def new():
    arc = ARC_Manager()
    symbol_name = arc.arc_id
    level = []
    exp = []
    income = []
    add = []

    for count in range(6):
        print (symbol_name[count])
        level.append(get_int_max(f'Enter {symbol_name[count]} level: ',20))
        exp.append(get_int_max(f'Enter {symbol_name[count]} exp: ', 2_679))
        income.append(get_bool(f'Daily quest? (o/x): '))
        if count in [0, 1]:
            add.append(get_bool('Extra daily? (o/x): '))
        if count == 2:
            add.append(get_int_max('Dream Defender coins (max 500): ', 500))
        if count == 3:
            add.append(get_int_max('Spirit Savior coins (max 30): ', 30))

    arc.setup(level, exp, income, add)

    selectors = get_int_max('Number of Selectors: ', 999_999)
    arc.distribute_selectors(selectors)
    print (f'Distributing {selectors} selectors')
    arc.output
    arc.json_save

def load():
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_path, 'save'), 'r') as o_file:
        out = json.load(o_file)
        selector = out['Selector']

    arc = ARC_Manager()
    arc.json_load
    arc.distribute_selectors(selector)
    arc.output

def main():
    print ('--- start ---')
    start = timer()

    end = timer() - start
    print ('--- end ---')
    print (f'total execution time : {round(end*1000, 2)} milliseconds')

if __name__ == '__main__':
    while True:
        foo = input('Enter (new | load | exit)\n').lower()
        if foo == 'new':
            new()
        elif foo == 'load':
            load()
        elif foo == 'exit':
            break
        else:
            print ('Unrecognized option:',foo)

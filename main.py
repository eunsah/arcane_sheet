'''
AF simulator
'''
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import shelve
from datetime import datetime, timedelta, date
import dbm
import os
import collections

WIDTH = 720
HEIGHT = 450
current_path = os.path.dirname(os.path.abspath(__file__))
default_text = ('Inconsolata', 12)
default_title = ('Inconsolata', 16)
symbol_max_level = 20
symbol_exp = [
    1,      11,     15,     20,     27,
    36,     47,     60,     75,     92,
    111,    132,    155,    180,    207,
    236,    267,    300,    335,    372
    ]
symbol_cost = [
    0,              9_500_000,      16_630_000,     23_760_000,
    30_890_000,     38_020_000,     45_150_000,     52_280_000,
    59_410_000,     66_540_000,     73_670_000,     80_800_000,
    87_930_000,     95_060_000,     102_190_000,    109_320_000,
    116_450_000,    123_580_000,    130_710_000,    137_840_000]
symbol_cost_discounted = [
    0,              19_040_000,     25_640_000,     32_240_000,
    38_840_000,     45_440_000,     52_040_000,     58_640_000,
    65_240_000,     71_840_000,     78_440_000,     85_040_000,
    91_640_000,     98_240_000,     104_840_000,    111_440_000,
    118_040_000,    124_640_000,    131_240_000,    137_840_000]
symbol_prefix = ['VJ', 'CC', 'LA', 'AR', 'MO', 'ES']
symbol_id = ['Vanishing', 'ChuChu', 'Lachelein', 'Arcana', 'Morass', 'Esfera']

class ArcaneForce(tk.Frame):
    '''
        class for tkinter
    '''
    def __init__(self, master=None):
        print ('ArcaneForce.Function.__init__()')
        super().__init__(master)
        self.master = master
        self.master.wm_protocol('WM_DELETE_WINDOW', self.exit)
        self.today = date.today()
        self.int_only = (self.register(self.validate_int_only),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.ARC_symbols = collections.defaultdict(int)
        '''self.ARC_symbols dict
        VJ_Symbol_lv_SV
        VJ_Symbol_exp_SV
        VJ_Quest_IV_SV
        VJ_Quest_IV_IV
        VJ_A_Quest_V
        '''
        self.ARC_objects = collections.defaultdict(int)

        self.root_frames()
        self.labelframe_manager()

        self.test()

### == root functions =====================
    def root_frames(self):
        print ('ArcaneForce.Function.root_frames()')
        self.header = tk.Frame(master = self.master, width=WIDTH, height=HEIGHT*.05)
        # self.header = tk.Frame(master = self.master,bg='red',width=WIDTH, height=HEIGHT*.05)
        self.header.pack()
        self.body = tk.Frame(master = self.master, width=WIDTH, height=HEIGHT*.9)
        self.body.pack()
        self.footnote = tk.Frame(master = self.master,width=WIDTH, height=HEIGHT*.05)
        # self.footnote = tk.Frame(master = self.master, bg='green',width=WIDTH, height=HEIGHT*.05)
        self.footnote.pack()

    def labelframe_manager(self):
        print ('ArcaneForce.Function.labelframe_manager()')
        ### Arcane Symbol Lable Frame
        self.current_arcane_symbol = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Symbols ',
            font = default_title,
            bd = 2, relief = 'ridge',
            width = WIDTH/3, height = HEIGHT*.42)
        self.current_arcane_symbol.place(x=35,y=0)
        self.handle_table_arcanesymbols()

        ### Arcane Force Label Frame
        self.options_labelframe = tk.LabelFrame(
            master = self.body,
            text = ' Options ',
            font = default_title,
            bd = 2, relief = 'ridge',
            width = WIDTH/5+45, height = HEIGHT*.42)
        self.options_labelframe.place(x=(WIDTH*2/3)+13, y=0)
        self.handle_options()

        ### Estimated Timeline Label Frame
        # self.master_update()
        self.current_timeline = tk.LabelFrame(
            master = self.body,
            text = ' Estimated Timeline ',
            font = default_title,
            bd = 2, relief = 'ridge',
            width = WIDTH*81/120, height = HEIGHT*.44)
        self.current_timeline.place(x=35, y=HEIGHT*.43)
        # self.current_timeline.pack_propagate(0)
        self.handle_table_timeline()

### == functions for arcane symbols =============
    def handle_table_arcanesymbols(self):
        self.table_symbol_name = ttk.Label(
            master = self.current_arcane_symbol,
            text = '',
            font = default_text,
            anchor = tk.S,
            width = 12)
        self.table_symbol_name.grid(row=0,column=0)

        self.table_symbol_level = ttk.Label(
            master = self.current_arcane_symbol,
            text = 'Lv.',
            font = default_text,
            anchor = tk.S,
            width = 4)
        self.table_symbol_level.grid(row=0,column=1)

        self.table_symbol_exp = ttk.Label(
            master = self.current_arcane_symbol,
            text = 'Exp.',
            font = default_text,
            anchor = tk.S,
            width = 4)
        self.table_symbol_exp.grid(row=0,column=2)

        self.table_symbol_daily_quest = ttk.Label(
            master = self.current_arcane_symbol,
            text = 'Daily Quest',
            font = default_text,
            anchor = tk.S,
            width = 14)
        self.table_symbol_daily_quest.grid(row=0, column=3)

        self.table_symbol_daily_quest = ttk.Label(
            master = self.current_arcane_symbol,
            text = 'Daily Additional',
            font = default_text,
            anchor = tk.S,
            width = 22)
        self.table_symbol_daily_quest.grid(row=0, column=4)

        self.table_symbol_daily_quest = ttk.Label(
            master = self.current_arcane_symbol,
            # text = 'Income  ',
            font = default_text,
            anchor = tk.S,
            width = 0)
        self.table_symbol_daily_quest.grid(row=0, column=5)

        ## --- title --------------------------------

        symbol_width = 16
        symbol_padding = 1
        symbol_entry_width = 3

        self.table_symbol_VJ = ttk.Label(
            master = self.current_arcane_symbol,
            text = '   '+symbol_id[0],
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding)
        self.table_symbol_VJ.grid(row=1,column=0)
        self.table_symbol_VJ_lv_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_VJ_lv_entry.grid(row=1, column=1)
        self.table_symbol_VJ_exp_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_VJ_exp_entry.grid(row=1, column=2)

        self.table_symbol_CC = ttk.Label(
            master = self.current_arcane_symbol,
            text = '   '+symbol_id[1],
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding)
        self.table_symbol_CC.grid(row=2,column=0)
        self.table_symbol_CC_lv_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_CC_lv_entry.grid(row=2, column=1)
        self.table_symbol_CC_exp_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_CC_exp_entry.grid(row=2, column=2)

        self.table_symbol_LA = ttk.Label(
            master = self.current_arcane_symbol,
            text = '   '+symbol_id[2],
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding)
        self.table_symbol_LA.grid(row=3,column=0)
        self.table_symbol_LA_lv_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_LA_lv_entry.grid(row=3, column=1)
        self.table_symbol_LA_exp_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_LA_exp_entry.grid(row=3, column=2)

        self.table_symbol_AR = ttk.Label(
            master = self.current_arcane_symbol,
            text = '   '+symbol_id[3],
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding)
        self.table_symbol_AR.grid(row=4,column=0)
        self.table_symbol_AR_lv_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_AR_lv_entry.grid(row=4, column=1)
        self.table_symbol_AR_exp_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_AR_exp_entry.grid(row=4, column=2)

        self.table_symbol_MO = ttk.Label(
            master = self.current_arcane_symbol,
            text = '   '+symbol_id[4],
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding)
        self.table_symbol_MO.grid(row=5,column=0)
        self.table_symbol_MO_lv_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_MO_lv_entry.grid(row=5, column=1)
        self.table_symbol_MO_exp_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_MO_exp_entry.grid(row=5, column=2)

        self.table_symbol_ES = ttk.Label(
            master = self.current_arcane_symbol,
            text = '   '+symbol_id[5],
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding)
        self.table_symbol_ES.grid(row=6,column=0)
        self.table_symbol_ES_lv_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_ES_lv_entry.grid(row=6, column=1)
        self.table_symbol_ES_exp_entry = ttk.Entry(
            master = self.current_arcane_symbol,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only)
        self.table_symbol_ES_exp_entry.grid(row=6, column=2)

        self.table_symbol_pad = ttk.Label(
            master = self.current_arcane_symbol,
            text = '')
        self.table_symbol_pad.grid(row=7,column=0)

        self.arcane_symbols_lv_exp()
        self.table_symbol_daily_income()
        self.table_symbol_daily_additional_income()

    def arcane_symbols_lv_exp(self):
        print ('ArcaneForce.Function.arcane_symbols_lv_exp()')

        def table_symbol_lv_update(*args):
            print('ArcaneForce.Function.arcane_symbols_lv_exp.table_symbol_lv_update()')
            num = args[1].get()
            if num != '':
                num = int(num)
                if num > symbol_max_level:
                    num = symbol_max_level
                args[1].set(num)
                self.ARC_symbols[args[0]] = num
            else:
                self.ARC_symbols[args[0]] = 0
            print (args[2]+' to '+args[0]+' value: '+str(num))
            self.master_update()

        def table_symbol_exp_update(*args):
            print('ArcaneForce.Function.arcane_symbols_lv_exp.table_symbol_exp_update()')
            num = args[1].get()
            if num != '':
                num = int(num)
                if num > symbol_exp[-1]:
                    num = symbol_exp[-1]
                args[1].set(num)
                self.ARC_symbols[args[0]] = num
            else:
                self.ARC_symbols[args[0]] = 0
            print (args[2]+' to '+args[0]+' value: '+str(num))
            self.master_update()

        def _arcane_symbols_init(name, func, entry, update):
            func = tk.StringVar(
                name = name,)
            entry.configure(
                textvariable = func)
            func.trace_add(
                ['write','read','unset'],
                lambda name,_,cmd: update(
                    name,
                    func,
                    cmd))
            self.ARC_symbols[func._name] = self.ARC_symbols[func._name]

        _arcane_symbols_init('VJ_Symbol_lv_SV',
                             self.ARC_symbols['VJ_Symbol_lv_SV'],
                             self.table_symbol_VJ_lv_entry,
                             table_symbol_lv_update)

        _arcane_symbols_init('VJ_Symbol_exp_SV',
                             self.ARC_symbols['VJ_Symbol_exp_SV'],
                             self.table_symbol_VJ_exp_entry,
                             table_symbol_exp_update)

        _arcane_symbols_init('CC_Symbol_lv_SV',
                             self.ARC_symbols['CC_Symbol_lv_SV'],
                             self.table_symbol_CC_lv_entry,
                             table_symbol_lv_update)

        _arcane_symbols_init('CC_Symbol_exp_SV',
                             self.ARC_symbols['CC_Symbol_exp_SV'],
                             self.table_symbol_CC_exp_entry,
                             table_symbol_exp_update)

        _arcane_symbols_init('LA_Symbol_lv_SV',
                             self.ARC_symbols['LA_Symbol_lv_SV'],
                             self.table_symbol_LA_lv_entry,
                             table_symbol_lv_update)

        _arcane_symbols_init('LA_Symbol_exp_SV',
                             self.ARC_symbols['LA_Symbol_exp_SV'],
                             self.table_symbol_LA_exp_entry,
                             table_symbol_exp_update)

        _arcane_symbols_init('AR_Symbol_lv_SV',
                             self.ARC_symbols['AR_Symbol_lv_SV'],
                             self.table_symbol_AR_lv_entry,
                             table_symbol_lv_update)

        _arcane_symbols_init('AR_Symbol_exp_SV',
                             self.ARC_symbols['AR_Symbol_exp_SV'],
                             self.table_symbol_AR_exp_entry,
                             table_symbol_exp_update)

        _arcane_symbols_init('MO_Symbol_lv_SV',
                             self.ARC_symbols['MO_Symbol_lv_SV'],
                             self.table_symbol_MO_lv_entry,
                             table_symbol_lv_update)

        _arcane_symbols_init('MO_Symbol_exp_SV',
                             self.ARC_symbols['MO_Symbol_exp_SV'],
                             self.table_symbol_MO_exp_entry,
                             table_symbol_exp_update)

        _arcane_symbols_init('ES_Symbol_lv_SV',
                             self.ARC_symbols['ES_Symbol_lv_SV'],
                             self.table_symbol_ES_lv_entry,
                             table_symbol_lv_update)

        _arcane_symbols_init('ES_Symbol_exp_SV',
                             self.ARC_symbols['ES_Symbol_exp_SV'],
                             self.table_symbol_ES_exp_entry,
                             table_symbol_exp_update)

    def table_symbol_daily_income(self):
        print('ArcaneForce.Function.table_symbol_daily_income()')

        s = ttk.Style()
        s.configure('.', font=default_text)

        def button_callback(key):
            print (self.ARC_symbols[key+'IV'].get())
            self.master_update()

        def _daily_quest_cb_bind(name, onvalue, box, IV, row, column):
            tk.Label(
                master = self.ARC_objects[name+'F'],
                font = default_text,
                text = '+'+str(onvalue)+' Symbols'
            ).grid(row=0, column=0,
                       sticky = 'w', padx=(4,0))
            box = ttk.Checkbutton(
                master = self.ARC_objects[name+'F'],
                takefocus = False,
                onvalue = onvalue,
                offvalue = '0',
                command = lambda : button_callback(name))
            box.configure(variable = IV)
            self.ARC_objects[prefix+'F'].grid(row=row, column=column)
            box.grid(row=0, column=1,
                          sticky = 'w')

        prefix = 'VJ_Quest_'
        self.ARC_objects[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        if self.ARC_symbols[prefix+'IV'] == 0:
            self.ARC_symbols[prefix+'IV'] = tk.StringVar(value = '0')
        else:
            self.ARC_symbols[prefix+'IV'] = self.ARC_symbols[prefix+'IV']

        _daily_quest_cb_bind(
            name = prefix,
            onvalue = '8',
            box = self.ARC_objects[prefix[0:-1]],
            IV = self.ARC_symbols[prefix+'IV'],
            row = 1, column = 3)

        prefix = 'CC_Quest_'
        self.ARC_objects[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        if self.ARC_symbols[prefix+'IV'] == 0:
            self.ARC_symbols[prefix+'IV'] = tk.StringVar(value = '0')
        else:
            self.ARC_symbols[prefix+'IV'] = self.ARC_symbols[prefix+'IV']

        _daily_quest_cb_bind(
            name = prefix,
            onvalue = '4',
            box = self.ARC_objects[prefix[0:-1]],
            IV = self.ARC_symbols[prefix+'IV'],
            row = 2, column = 3)

        prefix = 'LA_Quest_'
        self.ARC_objects[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        if self.ARC_symbols[prefix+'IV'] == 0:
            self.ARC_symbols[prefix+'IV'] = tk.StringVar(value = '0')
        else:
            self.ARC_symbols[prefix+'IV'] = self.ARC_symbols[prefix+'IV']

        _daily_quest_cb_bind(
            name = prefix,
            onvalue = '4',
            box = self.ARC_objects[prefix[0:-1]],
            IV = self.ARC_symbols[prefix+'IV'],
            row = 3, column = 3)

        prefix = 'AR_Quest_'
        self.ARC_objects[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        if self.ARC_symbols[prefix+'IV'] == 0:
            self.ARC_symbols[prefix+'IV'] = tk.StringVar(value = '0')
        else:
            self.ARC_symbols[prefix+'IV'] = self.ARC_symbols[prefix+'IV']

        _daily_quest_cb_bind(
            name = prefix,
            onvalue = '8',
            box = self.ARC_objects[prefix[0:-1]],
            IV = self.ARC_symbols[prefix+'IV'],
            row = 4, column = 3)

        prefix = 'MO_Quest_'
        self.ARC_objects[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        if self.ARC_symbols[prefix+'IV'] == 0:
            self.ARC_symbols[prefix+'IV'] = tk.StringVar(value = '0')
        else:
            self.ARC_symbols[prefix+'IV'] = self.ARC_symbols[prefix+'IV']

        _daily_quest_cb_bind(
            name = prefix,
            onvalue = '8',
            box = self.ARC_objects[prefix[0:-1]],
            IV = self.ARC_symbols[prefix+'IV'],
            row = 5, column = 3)

        prefix = 'ES_Quest_'
        self.ARC_objects[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        if self.ARC_symbols[prefix+'IV'] == 0:
            self.ARC_symbols[prefix+'IV'] = tk.StringVar(value = '0')
        else:
            self.ARC_symbols[prefix+'IV'] = self.ARC_symbols[prefix+'IV']

        _daily_quest_cb_bind(
            name = prefix,
            onvalue = '8',
            box = self.ARC_objects[prefix[0:-1]],
            IV = self.ARC_symbols[prefix+'IV'],
            row = 6, column = 3)

    def table_symbol_daily_additional_income(self):
        print('ArcaneForce.Function.table_symbol_daily_additional_income()')

        def AQ_checkbutton(prefix, callback, onvalue, name, row, column):
            self.ARC_objects[prefix+'F'] = tk.Frame(
                master = self.current_arcane_symbol)
            self.ARC_objects[prefix+'F'].grid(row = row, column = column, sticky='e')

            tk.Label(
                master = self.ARC_objects[prefix+'F'],
                font = default_text,
                text = name,
                width = 25,
                anchor = 'w').grid(row = 0, column = 0, sticky = 'w')
            self.ARC_objects[prefix[0:-1]] = ttk.Checkbutton(
                master = self.ARC_objects[prefix+'F'],
                takefocus = False,
                onvalue = onvalue,
                offvalue = 0,
                command = callback)
            if self.ARC_symbols[prefix+'IV']  == 0:
                self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
            else:
                self.ARC_symbols[prefix+'IV'] = self.ARC_symbols[prefix+'IV']

            self.ARC_objects[prefix[0:-1]].configure(variable = self.ARC_symbols[prefix+'IV'])
            self.ARC_objects[prefix[0:-1]].grid(row = 0, column = 1, sticky = 'e', padx=(0,7))

        def VJ_A_callback():
            self.ARC_symbols['VJ_A_Quest_V'] = self.ARC_symbols['VJ_A_Quest_IV'].get()
            self.master_update()

        prefix = 'VJ_A_Quest_'
        AQ_checkbutton(
            prefix = prefix,
            callback = VJ_A_callback,
            onvalue = 6,
            name = 'Erda Spectrum (+6)',
            row = 1, column = 4)

        def CC_A_callback():
            self.ARC_symbols['CC_A_Quest_V'] = self.ARC_symbols['CC_A_Quest_IV'].get()
            self.master_update()

        prefix = 'CC_A_Quest_'
        AQ_checkbutton(
            prefix = prefix,
            callback = CC_A_callback,
            onvalue = 15,
            name = 'Hungry Muto (+15)',
            row = 2, column = 4)

        def AQ_entry_box(prefix, callback, name, row, column):
            self.ARC_objects[prefix+'F'] = tk.Frame(
                master = self.current_arcane_symbol)
            tk.Label(
                master = self.ARC_objects[prefix+'F'],
                text = name,
                font = default_text,
                anchor = 'w',
                width = 24).grid(row = 0, column = 0, sticky= 'w')
            self.ARC_objects[prefix[0:-1]]  = ttk.Entry(
                master = self.ARC_objects[prefix+'F'],
                font = default_text,
                width = 4,
                validate='key',
                validatecommand=self.int_only)
            if self.ARC_symbols[prefix+'SV'] == 0:
                self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = '')
            else:
                self.ARC_symbols[prefix+'SV'] = self.ARC_symbols[prefix+'SV']
            self.ARC_objects[prefix[0:-1]] .configure(textvariable = self.ARC_symbols[prefix+'SV'] )
            self.ARC_symbols[prefix+'SV'].trace_add(['write','array', 'read'], callback)
            self.ARC_objects[prefix+'F'].grid(row = row, column = column, sticky='e')
            self.ARC_objects[prefix[0:-1]].grid(row=0, column = 1)

        def LA_A_callback(*args):
            ptr = self.ARC_symbols['LA_A_Quest_SV']
            if ptr.get() != '':
                num = int(ptr.get())
                if num > 300:
                    num = 300
                ptr.set(str(num))
                self.ARC_symbols['LA_A_Quest_V'] = num
            self.master_update()

        prefix = 'LA_A_Quest_'
        AQ_entry_box(
            prefix = prefix,
            callback = LA_A_callback,
            name = 'Dream Defender (300 max)',
            row = 3, column = 4)

        def AR_A_callback(*args):
            ptr = self.ARC_symbols['AR_A_Quest_SV']
            if ptr.get() != '':
                num = int(ptr.get())
                if num > 30:
                    num = 30
                ptr.set(str(num))
                self.ARC_symbols['AR_A_Quest_V'] = num
            self.master_update()

        prefix = 'AR_A_Quest_'
        AQ_entry_box(
            prefix = prefix,
            callback = AR_A_callback,
            name = 'Spirit Savior (30 max)',
            row = 4, column = 4)

### == functions for estimated timeline =========
    def handle_table_timeline(self):
        print ('ArcaneForce.Function.handle_table_timeline()')

        def symbol_id_grid(name, row):
            ttk.Label(
                master = self.current_timeline,
                text = '   '+name,
                font = default_text,
                anchor = tk.W,
                width = symbol_width,
                padding = symbol_padding).grid(row=row, column=0)

        symbol_width = 16
        symbol_padding = 3

        ttk.Label(
            master = self.current_timeline,
            text = '',
            font = default_text,
            anchor = tk.S,
            width = symbol_width,
            padding = symbol_padding).grid(row=0, column=0)

        ttk.Label(
            master = self.current_timeline,
            text = 'Raw',
            font = default_text,
            anchor = tk.S,
            width = 6).grid(row=0, column=1)

        ttk.Label(
            master = self.current_timeline,
            text = 'Days',
            font = default_text,
            anchor = tk.S,
            width = 6).grid(row=0, column=2)

        ttk.Label(
            master = self.current_timeline,
            text = 'Date',
            font = default_text,
            anchor = tk.S,
            width = 16).grid(row=0, column=3)

        ttk.Label(
            master = self.current_timeline,
            text = 'Selector',
            font = default_text,
            anchor = tk.S,
            width = 12).grid(row=0, column=4)

        ttk.Label(
            master = self.current_timeline,
            text = 'Future',
            font = default_text,
            anchor = tk.S,
            width = 8).grid(row=0, column=5)

        ttk.Label(
            master = self.current_timeline,
            text = 'Future date',
            font = default_text,
            anchor = tk.S,
            width = 16).grid(row=0, column=6)

        ttk.Label(
            master = self.current_timeline,
            text = 'F.Lv',
            font = default_text,
            anchor = tk.S,
            width = 8).grid(row=0, column=7)

        ttk.Label(
            master = self.current_timeline,
            text = 'F.Exp',
            font = default_text,
            anchor = tk.S,
            width = 8).grid(row=0, column=8)

        ttk.Label(
            master = self.current_timeline,
            text = '',
            font = default_text,
            anchor = tk.S,
            width = 4).grid(row=0, column=9)

        count = 0
        for name in symbol_id:
            count += 1
            symbol_id_grid(name, count)

        ttk.Label(
            master = self.current_timeline,
            text = '',
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding).grid(row=7, column=0)

        # raw exp
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_raw_TL'] = tk.IntVar(value = self.ARC_symbols[prefix+'_raw'])
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_raw_TL']
            ).grid(row = count, column = 1)
            count += 1

        # days
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_days'] = tk.StringVar(value='-')
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_days']
            ).grid(row = count, column = 2)
            count += 1

        # date
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_date_now'] = tk.StringVar(value='-')
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_date_now']
            ).grid(row = count, column = 3)
            count += 1

        # selector
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_selector'] = tk.StringVar(value='0')
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_selector']
            ).grid(row = count, column = 4)
            count += 1

        # future
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_future'] = tk.StringVar(value='-')
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_future']
            ).grid(row = count, column = 5)
            count += 1

        # date future
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_date_future'] = tk.StringVar(value='-')
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_date_future']
            ).grid(row = count, column = 6)
            count += 1

        # future level
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_future_lv'] = tk.StringVar(value='-')
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_future_lv']
            ).grid(row = count, column = 7)
            count += 1

        # future exp
        count = 1
        for prefix in symbol_prefix:
            self.ARC_objects[prefix+'_future_exp'] = tk.StringVar(value='-')
            ttk.Label(
                master = self.current_timeline,
                font = default_text,
                anchor = tk.S,
                textvariable = self.ARC_objects[prefix+'_future_exp']
            ).grid(row = count, column = 8)
            count += 1

### == functions for options  ==============
    def handle_options(self):
        print ('ArcaneForce.Function.handle_options()')
        ttk.Label(
            master = self.options_labelframe,
            font = default_text,
            text = '   Arcane Force :'
        ).grid(row=0, column=0)

        self.options_labelframe_symbol_value = tk.StringVar(value = 0)
        ttk.Label(
            master = self.options_labelframe,
            font = default_title,
            textvariable = self.options_labelframe_symbol_value,
            width = 10
        ).grid(row=0, column=1)




### == class functions
    def master_update(self):
        print ('ArcaneForce.Function.master_update()')
        self._income_update()
        self._arcane_update()
        self._raw_exp_update()
        self._date_now_update()
        self._date_future_update()

    def _income_update(self):
        for prefix in symbol_prefix:
            daily = int(self.ARC_symbols[prefix+'_Quest_IV'].get())
            adaily = int(self.ARC_symbols[prefix+'_A_Quest_V'])
            if adaily > 0:
                if prefix == 'LA':
                    adaily = (adaily+24) / 30
                elif prefix == 'AR':
                    adaily = adaily / 3
                else:
                    pass
            daily += adaily
            self.ARC_symbols[prefix+'_DailyIncome'] = daily

    def _arcane_update(self):
        num = 0
        self.ARC_symbols['_SymbolForce'] = 0
        for prefix in symbol_prefix:
            if self.ARC_symbols[prefix+'_Symbol_lv_SV'] != '' and self.ARC_symbols[prefix+'_Symbol_lv_SV'] > 0:
                num = 30
                num += self.ARC_symbols[prefix+'_Symbol_lv_SV']*10
                self.ARC_symbols['_SymbolForce'] += num
            else:
                pass
        self.options_labelframe_symbol_value.set(self.ARC_symbols['_SymbolForce'])

    def _raw_exp_update(self):
        for prefix in symbol_prefix:
            raw_exp = 0
            if self.ARC_symbols[prefix+'_Symbol_lv_SV'] != '' and self.ARC_symbols[prefix+'_Symbol_lv_SV'] > 0:
                level = self.ARC_symbols[prefix+'_Symbol_lv_SV']
                raw_exp += sum([count for count in symbol_exp[:level]])
            if self.ARC_symbols[prefix+'_Symbol_exp_SV'] != '' and self.ARC_symbols[prefix+'_Symbol_exp_SV'] > 0:
                raw_exp += self.ARC_symbols[prefix+'_Symbol_exp_SV']
            if raw_exp > 2679:
                raw_exp = 2679
            self.ARC_symbols[prefix+'_raw'] = raw_exp
            if self.ARC_objects[prefix+'_raw_TL'] != 0:
                self.ARC_objects[prefix+'_raw_TL'].set(value = self.ARC_symbols[prefix+'_raw'])

    def _date_now_update(self):
        max_exp = sum(symbol_exp)
        for prefix in symbol_prefix:
            req_exp = max_exp - self.ARC_symbols[prefix+'_raw']
            if req_exp == 0:
                self.ARC_objects[prefix+'_days'].set(value = 'Done')
                self.ARC_objects[prefix+'_date_now'].set(value = self.today)
            elif self.ARC_symbols[prefix+'_DailyIncome'] == 0:
                self.ARC_objects[prefix+'_days'].set(value = '-')
                self.ARC_objects[prefix+'_date_now'].set(value = 'Never')
            else:
                days = req_exp/self.ARC_symbols[prefix+'_DailyIncome']
                days = int(days + 0.9)
                self.ARC_objects[prefix+'_days'].set(value = days)
                future = self.today + timedelta(days=days)
                self.ARC_objects[prefix+'_date_now'].set(value = future)

    def _date_future_update(self):
        max_exp = sum(symbol_exp)
        for prefix in symbol_prefix:
            selector = int(self.ARC_objects[prefix+'_selector'].get())
            new_raw = self.ARC_symbols[prefix+'_raw'] + selector
            req_exp = max_exp - new_raw
            if req_exp <= 0:
                self.ARC_objects[prefix+'_future'].set(value = 'Done')
                self.ARC_objects[prefix+'_date_future'].set(value = self.today)
                self.ARC_objects[prefix+'_futured'] = -1
            elif self.ARC_symbols[prefix+'_DailyIncome'] == 0:
                self.ARC_objects[prefix+'_future'].set(value = '-')
                self.ARC_objects[prefix+'_date_future'].set(value = 'Never')
            else:
                days = req_exp/self.ARC_symbols[prefix+'_DailyIncome']
                self.ARC_objects[prefix+'_futured'] = days
                days = int(days + 0.9)
                self.ARC_objects[prefix+'_future'].set(value = days)
                future = self.today + timedelta(days=days)
                self.ARC_objects[prefix+'_date_future'].set(value = future)

            n_lv = 0
            n_exp = 0
            for level in symbol_exp:
                if new_raw > level:
                    n_lv += 1
                    new_raw -= level
                else:
                    n_exp = new_raw
                    break
            self.ARC_objects[prefix+'_future_lv'].set(value = n_lv)
            self.ARC_objects[prefix+'_future_exp'].set(value = n_exp)

    def validate_int_only(self, d, i, P, s, S, v, V, W):
        print ('ArcaneForce.Function.validate_int_only()')
        # valid percent substitutions (from the Tk entry man page)
        # note: you only have to register the ones you need; this
        # example registers them all for illustrative purposes
        #
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        if S.isdigit():
            return True
        else:
            self.bell()
            return False

    def exit(self):
        print ('ArcaneForce.Function.exit()')
        # needs to save defaultdict
        self.master.destroy()

### == test functions
    def test(self):
        print ('ArcaneForce.Function.test()')
        print (current_path)
        print (os.path.join(current_path, 'data'))

        def test_callback(*args):
            print ('test button')

            print ('Hyper:', self.ARC_symbols['Hyper'])
            print ('Guild:', self.ARC_symbols['Guild'])
            print ('Equip:', self.ARC_symbols['Equip'])

            for prefix in symbol_prefix:
                print (prefix)
                print ('lv:',self.ARC_symbols[prefix+'_Symbol_lv_SV'])
                print ('exp:', self.ARC_symbols[prefix+'_Symbol_exp_SV'])
                print ('daily:', self.ARC_symbols[prefix+'_Quest_IV'].get())
                print ('daily additional', self.ARC_symbols[prefix+'_A_Quest_V'])
                print ('raw exp', self.ARC_symbols[prefix+'_raw'])
                print ('daily income', self.ARC_symbols[prefix+'_DailyIncome'])

            for item in self.ARC_symbols:
                print (item, self.ARC_symbols[item])

        def b1(*args):
            select = 1000
            while select > 0:
                top_val = max([self.ARC_objects[prefix+'_futured']  for prefix in symbol_prefix])
                if top_val < 0:
                    break
                for prefix in symbol_prefix:
                    if self.ARC_objects[prefix+'_futured'] == top_val:
                        self.ARC_objects[prefix+'_selector'].set(int(self.ARC_objects[prefix+'_selector'].get())+1)
                        select -= 1
                        if select == 0:
                            break
                    self._date_future_update()

        def b2(*args):
            for prefix in symbol_prefix:
                self.ARC_objects[prefix+'_selector'].set(value = 0)
            self._date_future_update()

        self.test_button = tk.Button(master = self.body, text='test', command=test_callback)
        self.test_button.place(x=500,y=160)

        self.b1 = tk.Button(master = self.body, text='b1', command=b1)
        self.b1.place(x=560,y=160)

        self.b2 = tk.Button(master = self.body, text='b2', command=b2)
        self.b2.place(x=610,y=160)

def main():
    root = tk.Tk()
    root.title('AF_Spreadsheet')
    root.geometry(str(WIDTH)+'x'+str(HEIGHT))
    root.minsize(width=WIDTH, height=HEIGHT)
    root.maxsize(width=WIDTH, height=HEIGHT)
    app = ArcaneForce(master=root)
    app.mainloop()
    print ('end of main')

if __name__ == '__main__':
    main()

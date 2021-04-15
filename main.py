'''
AF
'''
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import shelve
from datetime import datetime, timedelta
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

class ArcaneForce(tk.Frame):
    '''
        class for tkinter
    '''
    def __init__(self, master=None):
        print ('ArcaneForce.Function.__init__()')
        super().__init__(master)
        self.master = master
        self.master.wm_protocol('WM_DELETE_WINDOW', self.exit)
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

        # self.test()
        self.root_frames()
        self.labelframe_manager()

### == root functions =====================
    def root_frames(self):
        print ('ArcaneForce.Function.root_frames()')
        self.header = tk.Frame(master = self.master,bg='red',width=WIDTH, height=HEIGHT*.05)
        self.header.pack()
        self.body = tk.Frame(master = self.master, width=WIDTH, height=HEIGHT*.9)
        self.body.pack()
        self.footnote = tk.Frame(master = self.master, bg='green',width=WIDTH, height=HEIGHT*.05)
        self.footnote.pack()

    def labelframe_manager(self):
        print ('ArcaneForce.Function.labelframe_manager()')
        ### Arcane Force Label Frame
        self.current_arcaneforce = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Force ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH/3, height = HEIGHT*.39)
        self.current_arcaneforce.place(x=(WIDTH*2/3)+13, y=HEIGHT*.01)
        self.handle_current_arcaneforce()

        ### Arcane Symbol Lable Frame
        self.current_arcane_symbol = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Symbols ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH/3, height = HEIGHT*.41)
        self.current_arcane_symbol.place(x=18,y=HEIGHT*.01)
        self.handle_table_arcanesymbols()

        ### Arcane Dailies Label Frame
        self.current_arcane_dailies = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Dailies ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH*75/120, height = HEIGHT*.41)
        self.current_arcane_dailies.place(x=18, y=HEIGHT*.47)
        self.current_arcane_dailies.pack_propagate(0)

### == functions for arcane force labelframe ====
    def handle_current_arcaneforce(self):
        print ('ArcaneForce.Function.handle_current_arcaneforce()')

        def combobox_selected(this):
            print ('ArcaneForce.Function.combobox_selected()')
            # print ('From :', this.widget)
            print ('selected=', this.widget.get(), sep='')

        def auto_text_space(text, totalsizeoftext):
            return '      ' + text + ' '*(totalsizeoftext-(len(text)+7))

        set_text_space = 20
        self.current_arcaneforce_symbol = tk.Label(
            master = self.current_arcaneforce,
            text = auto_text_space('Symbol:', set_text_space),
            font = default_text,
            anchor = 'w')
        self.current_arcaneforce_symbol.pack(anchor='w', pady=(5, 0))
        self.current_arcaneforce_symbol_value = tk.StringVar(value='0')
        self.current_arcaneforce_symbol_entry = ttk.Entry(
            master = self.current_arcaneforce_symbol,
            font = default_text,
            width = int(WIDTH/90),
            justify = tk.CENTER,
            state = 'disabled')
        self.current_arcaneforce_symbol_entry.configure(
            textvariable=self.current_arcaneforce_symbol_value)
        self.current_arcaneforce_symbol_entry.pack(padx=(140, 10), anchor='se')

        self.current_arcaneforce_hyper = tk.Label(
            master = self.current_arcaneforce,
            text = auto_text_space('Hyper Stats Lv.:', set_text_space),
            font = default_text,
            anchor = 'w')
        self.current_arcaneforce_hyper.pack(anchor='w')
        self.current_arcaneforce_hyper_combobox = ttk.Combobox(
            master = self.current_arcaneforce_hyper,
            font = default_text,
            width = int(WIDTH/90)-2,
            justify = tk.CENTER,
            height = 5,
            values = ['0', '1', '2', '3', '4',
                      '5', '6', '7', '8', '9',
                      '10', '11', '12', '13',
                      '14', '15'],
            state = 'readonly')

        self.current_arcaneforce_hyper_combobox.pack(padx=(140, 10), anchor='se')
        self.current_arcaneforce_hyper_combobox.bind('<<ComboboxSelected>>', combobox_selected)

        self.current_arcaneforce_guild = tk.Label(
            master = self.current_arcaneforce,
            text = auto_text_space('Guild Skill Lv.:', set_text_space),
            font = default_text,
            anchor = 'w')
        self.current_arcaneforce_guild.pack(anchor='w')
        self.current_arcaneforce_guild_combobox = ttk.Combobox(
            master = self.current_arcaneforce_guild,
            font = default_text,
            width = int(WIDTH/90)-2,
            justify = tk.CENTER,
            height = 5,
            values = ['0', '1', '2', '3', '4', '5', '6'],
            state = 'readonly')

        self.current_arcaneforce_guild_combobox.pack(padx=(140, 10), anchor='se')
        self.current_arcaneforce_guild_combobox.bind('<<ComboboxSelected>>', combobox_selected)

        self.current_arcaneforce_equip = tk.Label(
            master = self.current_arcaneforce,
            text = auto_text_space('Other AF source:', set_text_space),
            font = default_text,
            anchor = 'w')
        self.current_arcaneforce_equip.pack(anchor='w', pady=(0, 10))
        self.current_arcaneforce_equip_combobox = ttk.Combobox(
            master = self.current_arcaneforce_equip,
            font = default_text,
            width = int(WIDTH/90)-2,
            justify = tk.CENTER,
            height = 5,
            values = ['0', '30', '50', '60', '80'],
            state = 'readonly')

        self.current_arcaneforce_equip_combobox.pack(padx=(140, 10), anchor='se')
        self.current_arcaneforce_equip_combobox.bind('<<ComboboxSelected>>', combobox_selected)

        self.current_arcaneforce_init()
        # --------------------------------------------------------------

        # self.current_arcaneforce_total = tk.Label(
        #     master = self.current_arcaneforce,
        #     text = '  Total Arcane Force:',
        #     font = ('Inconsolata', 14),
        #     anchor = 'w'
        # )
        # self.current_arcaneforce_total.pack(anchor='w')
        # self.current_arcaneforce_total_value = tk.StringVar(value='1350')
        # self.current_arcaneforce_total_result = tk.Label(
        #     master = self.current_arcaneforce_total,
        #     font = ('Inconsolata', 18),
        #     width = 4,
        #     anchor = 'e'
        # )
        # self.current_arcaneforce_total_result.configure(
        #     textvariable=self.current_arcaneforce_total_value
        # )
        # self.current_arcaneforce_total_result.pack(padx=(160, 10), anchor='se')

    def current_arcaneforce_init(self):
        self.current_arcaneforce_hyper_value = tk.StringVar(value='0')
        self.current_arcaneforce_hyper_combobox.configure(
            textvariable=self.current_arcaneforce_hyper_value)
        self.current_arcaneforce_guild_value = tk.StringVar(value='0')
        self.current_arcaneforce_guild_combobox.configure(
            textvariable=self.current_arcaneforce_guild_value)
        self.current_arcaneforce_equip_value = tk.StringVar(value='0')
        self.current_arcaneforce_equip_combobox.configure(
            textvariable=self.current_arcaneforce_equip_value)

### == functions for arcane symbols =============
    def handle_table_arcanesymbols(self):
        self.table_symbol_name = ttk.Label(
            master = self.current_arcane_symbol,
            text = 'Symbol Name',
            font = default_text,
            anchor = tk.S,
            width = 16)
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
            text = 'Exp',
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
            text = 'Income  ',
            font = default_text,
            anchor = tk.S,
            width = 8)
        self.table_symbol_daily_quest.grid(row=0, column=5)

        ## --- title --------------------------------

        symbol_width = 20
        symbol_padding = 1
        symbol_entry_width = 3

        self.table_symbol_VJ = ttk.Label(
            master = self.current_arcane_symbol,
            text = ' Vanishing Journey',
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
            text = ' ChuChu Island',
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
            text = ' Lachelein',
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
            text = ' Arcana',
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
            text = ' Morass',
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
            text = ' Esfera',
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
            print('ArcaneForce.Function.table_symbol_lv_update()')
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

        def table_symbol_exp_update(*args):
            print('ArcaneForce.Function.table_symbol_exp_update()')
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
            self.ARC_symbols[func._name] = 0

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
        no_symbol = '+0 Symbols'

        def button_callback(key):
            print (self.ARC_symbols[key+'IV'].get())
            self.ARC_symbols[key+'SV'].set(
                '+'+str(self.ARC_symbols[key+'IV'].get())+' Symbols')

        def _daily_quest_cb_bind(name, onvalue, box, label, IV, SV, row, column):
            label = tk.Label(
                master = self.ARC_symbols[name+'F'],
                font = default_text
            )
            box = ttk.Checkbutton(
                master = self.ARC_symbols[name+'F'],
                takefocus = False,
                onvalue = onvalue,
                offvalue = 0,
                command = lambda : button_callback(name))
            box.configure(variable = IV)
            label.configure(textvariable = SV)
            self.ARC_symbols[prefix+'F'].grid(row=row, column=column)
            box.grid(row=0, column=1,
                          sticky = 'w')
            label.grid(row=0, column=0,
                       sticky = 'w', padx=(4,0))

        prefix = 'VJ_Quest_'
        self.ARC_symbols[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
        self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = no_symbol)
        _daily_quest_cb_bind(
            name = prefix,
            onvalue = 8,
            box = self.ARC_symbols[prefix[0:-1]],
            label = self.ARC_symbols[prefix+'L'],
            IV = self.ARC_symbols[prefix+'IV'],
            SV = self.ARC_symbols[prefix+'SV'],
            row = 1, column = 3)

        prefix = 'CC_Quest_'
        self.ARC_symbols[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
        self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = no_symbol)
        _daily_quest_cb_bind(
            name = prefix,
            onvalue = 4,
            box = self.ARC_symbols[prefix[0:-1]],
            label = self.ARC_symbols[prefix+'L'],
            IV = self.ARC_symbols[prefix+'IV'],
            SV = self.ARC_symbols[prefix+'SV'],
            row = 2, column = 3)

        prefix = 'LA_Quest_'
        self.ARC_symbols[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
        self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = no_symbol)
        _daily_quest_cb_bind(
            name = prefix,
            onvalue = 4,
            box = self.ARC_symbols[prefix[0:-1]],
            label = self.ARC_symbols[prefix+'L'],
            IV = self.ARC_symbols[prefix+'IV'],
            SV = self.ARC_symbols[prefix+'SV'],
            row = 3, column = 3)

        prefix = 'AR_Quest_'
        self.ARC_symbols[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
        self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = no_symbol)
        _daily_quest_cb_bind(
            name = prefix,
            onvalue = 8,
            box = self.ARC_symbols[prefix[0:-1]],
            label = self.ARC_symbols[prefix+'L'],
            IV = self.ARC_symbols[prefix+'IV'],
            SV = self.ARC_symbols[prefix+'SV'],
            row = 4, column = 3)

        prefix = 'MO_Quest_'
        self.ARC_symbols[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
        self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = no_symbol)
        _daily_quest_cb_bind(
            name = prefix,
            onvalue = 8,
            box = self.ARC_symbols[prefix[0:-1]],
            label = self.ARC_symbols[prefix+'L'],
            IV = self.ARC_symbols[prefix+'IV'],
            SV = self.ARC_symbols[prefix+'SV'],
            row = 5, column = 3)

        prefix = 'ES_Quest_'
        self.ARC_symbols[prefix+'F'] = tk.Frame(self.current_arcane_symbol)
        self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
        self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = no_symbol)
        _daily_quest_cb_bind(
            name = prefix,
            onvalue = 8,
            box = self.ARC_symbols[prefix[0:-1]],
            label = self.ARC_symbols[prefix+'L'],
            IV = self.ARC_symbols[prefix+'IV'],
            SV = self.ARC_symbols[prefix+'SV'],
            row = 6, column = 3)

    def table_symbol_daily_additional_income(self):
        print('ArcaneForce.Function.table_symbol_daily_additional_income()')

        def AQ_checkbutton(prefix, callback, onvalue, name, row, column):
            self.ARC_symbols[prefix+'F'] = tk.Frame(
                master = self.current_arcane_symbol)
            self.ARC_symbols[prefix+'F'].grid(row = row, column = column, sticky='e')

            self.ARC_symbols[prefix+'L'] = tk.Label(
                master = self.ARC_symbols[prefix+'F'],
                font = default_text,
                width = 25,
                anchor = 'w')
            self.ARC_symbols[prefix[0:-1]] = ttk.Checkbutton(
                master = self.ARC_symbols[prefix+'F'],
                takefocus = False,
                onvalue = onvalue,
                offvalue = 0,
                command = callback)
            self.ARC_symbols[prefix+'IV'] = tk.IntVar(value = 0)
            self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = name)
            self.ARC_symbols[prefix[0:-1]].configure(variable = self.ARC_symbols[prefix+'IV'])
            self.ARC_symbols[prefix+'L'].configure(textvariable = self.ARC_symbols[prefix+'SV'])
            self.ARC_symbols[prefix+'L'].grid(row = 0, column = 0, sticky = 'w')
            self.ARC_symbols[prefix[0:-1]].grid(row = 0, column = 1, sticky = 'e', padx=(0,6))

        def VJ_A_callback():
            if self.ARC_symbols['VJ_A_Quest_IV'].get() == 0:
                self.ARC_symbols['VJ_A_Quest_SV'] .set('Erda Spectrum (+0)')
            else:
                self.ARC_symbols['VJ_A_Quest_SV'] .set('Erda Spectrum (+6)')

        prefix = 'VJ_A_Quest_'
        AQ_checkbutton(
            prefix = prefix,
            callback = VJ_A_callback,
            onvalue = 8,
            name = 'Erda Spectrum (+0)',
            row = 1, column = 4)

        def CC_A_callback():
            if self.ARC_symbols['CC_A_Quest_IV'].get() == 0:
                self.ARC_symbols['CC_A_Quest_SV'] .set('Hungry Muto (+0)')
            else:
                self.ARC_symbols['CC_A_Quest_SV'] .set('Hungry Muto (+15)')

        prefix = 'CC_A_Quest_'
        AQ_checkbutton(
            prefix = prefix,
            callback = CC_A_callback,
            onvalue = 15,
            name = 'Hungry Muto (+0)',
            row = 2, column = 4)

        def AQ_entry_box(prefix, callback, name, row, column):
            self.ARC_symbols[prefix+'F'] = tk.Frame(master = self.current_arcane_symbol)
            self.ARC_symbols[prefix+'L']  = tk.Label(
                master = self.ARC_symbols[prefix+'F'],
                text = name,
                font = default_text,
                anchor = 'w')
            self.ARC_symbols[prefix[0:-1]]  = tk.Entry(
                master = self.ARC_symbols[prefix+'F'],
                font = default_text,
                width =4,
                validate='key',
                validatecommand=self.int_only)
            self.ARC_symbols[prefix+'SV'] = tk.StringVar(value = '')
            self.ARC_symbols[prefix[0:-1]] .configure(textvariable = self.ARC_symbols[prefix+'SV'] )
            self.ARC_symbols[prefix+'SV'].trace_add(['write','array', 'read'], callback)
            self.ARC_symbols[prefix+'L'] .grid(row = 0, column = 0)
            self.ARC_symbols[prefix+'F'].grid(row=3, column= 4)
            self.ARC_symbols[prefix[0:-1]] .grid(row=0, column =1 )

        def LA_A_callback(*args):
            pass

        prefix = 'LA_A_Quest_'
        AQ_entry_box(
            prefix = prefix,
            callback = LA_A_callback,
            name = 'Dream Defender (300 max)',
            row = 3, column = 4)

        def AR_A_callback(*args):
            pass


### == class functions
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

    def test(self):
        print ('ArcaneForce.Function.test()')
        print (current_path)
        print (os.path.join(current_path, 'data'))

    def exit(self):
        print ('ArcaneForce.Function.exit()')
        # needs to save defaultdict
        self.master.destroy()

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

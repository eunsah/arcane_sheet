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

WIDTH = 720
HEIGHT = 450
current_path = os.path.dirname(os.path.abspath(__file__))
default_text = ('Inconsolata', 12)
default_title = ('Inconsolata', 16)
symbol_max_level = 20
ARC_symbols = [(None, None)]*6
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
    116_450_000,    123_580_000,    130_710_000,    137_840_000
]
symbol_cost_discounted = [
    0,              19_040_000,     25_640_000,     32_240_000,
    38_840_000,     45_440_000,     52_040_000,     58_640_000,
    65_240_000,     71_840_000,     78_440_000,     85_040_000,
    91_640_000,     98_240_000,     104_840_000,    111_440_000,
    118_040_000,    124_640_000,    131_240_000,    137_840_000
]

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
        # self.test()
        self.root_frames()
        self.labelframe_manager()

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
        self.current_arcaneforce = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Force ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH/3, height = HEIGHT*.39
        )
        self.current_arcaneforce.place(x=(WIDTH*2/3)+13, y=HEIGHT*.01)
        # self.current_arcaneforce.place(x=18,y=HEIGHT*.01)
        self.handle_current_arcaneforce()

        self.current_symbol_level = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Symbols ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH/3, height = HEIGHT*.41
        )
        self.current_symbol_level.place(x=18,y=HEIGHT*.01)
        # self.current_symbol_level.place(x=(WIDTH/3)+13, y=HEIGHT*.01)
        # self.current_symbol_level.place(x=18, y=HEIGHT*.40)
        self.handle_table_arcanesymbols()

        self.current_arcane_dailies = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Dailies ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH*75/120, height = HEIGHT*.41
        )
        self.current_arcane_dailies.place(x=18, y=HEIGHT*.47)
        self.current_arcane_dailies.pack_propagate(0)

        # self.current_date_estimates = tk.LabelFrame(
        #     master = self.body,
        #     text = ' Dates Till Max ',
        #     font = default_title,
        #     bd = 1, relief = 'ridge',
        #     width = WIDTH*17/60, height = HEIGHT*.39
        # )
        # self.current_date_estimates.place(x=(WIDTH/3)+13, y=HEIGHT*.03)
        # self.current_date_estimates.pack_propagate(0)

    def handle_current_arcaneforce(self):
        print ('ArcaneForce.Function.handle_current_arcaneforce()')
        set_text_space = 20
        self.current_arcaneforce_symbol = tk.Label(
            master = self.current_arcaneforce,
            text = self._auto_text_space('Symbol:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
        self.current_arcaneforce_symbol.pack(anchor='w', pady=(5, 0))
        self.current_arcaneforce_symbol_value = tk.StringVar(value='0')
        self.current_arcaneforce_symbol_entry = ttk.Entry(
            master = self.current_arcaneforce_symbol,
            font = default_text,
            width = int(WIDTH/90),
            justify = tk.CENTER,
            state = 'disabled'
            )
        self.current_arcaneforce_symbol_entry.configure(
            textvariable=self.current_arcaneforce_symbol_value
            )
        self.current_arcaneforce_symbol_entry.pack(padx=(140, 10), anchor='se')

        self.current_arcaneforce_hyper = tk.Label(
            master = self.current_arcaneforce,
            text = self._auto_text_space('Hyper Stats Lv.:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
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
            state = 'readonly'
        )

        self.current_arcaneforce_hyper_combobox.pack(padx=(140, 10), anchor='se')
        self.current_arcaneforce_hyper_combobox.bind('<<ComboboxSelected>>', self.reset_combobox_selection)

        self.current_arcaneforce_guild = tk.Label(
            master = self.current_arcaneforce,
            text = self._auto_text_space('Guild Skill Lv.:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
        self.current_arcaneforce_guild.pack(anchor='w')
        self.current_arcaneforce_guild_combobox = ttk.Combobox(
            master = self.current_arcaneforce_guild,
            font = default_text,
            width = int(WIDTH/90)-2,
            justify = tk.CENTER,
            height = 5,
            values = ['0', '1', '2', '3', '4', '5', '6'],
            state = 'readonly'
        )

        self.current_arcaneforce_guild_combobox.pack(padx=(140, 10), anchor='se')
        self.current_arcaneforce_guild_combobox.bind('<<ComboboxSelected>>', self.reset_combobox_selection)

        self.current_arcaneforce_equip = tk.Label(
            master = self.current_arcaneforce,
            text = self._auto_text_space('Other AF source:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
        self.current_arcaneforce_equip.pack(anchor='w', pady=(0, 10))
        self.current_arcaneforce_equip_combobox = ttk.Combobox(
            master = self.current_arcaneforce_equip,
            font = default_text,
            width = int(WIDTH/90)-2,
            justify = tk.CENTER,
            height = 5,
            values = ['0', '30', '50', '60', '80'],
            state = 'readonly'
        )

        self.current_arcaneforce_equip_combobox.pack(padx=(140, 10), anchor='se')
        self.current_arcaneforce_equip_combobox.bind('<<ComboboxSelected>>', self.reset_combobox_selection)

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
            textvariable=self.current_arcaneforce_hyper_value
        )
        self.current_arcaneforce_guild_value = tk.StringVar(value='0')
        self.current_arcaneforce_guild_combobox.configure(
            textvariable=self.current_arcaneforce_guild_value
        )
        self.current_arcaneforce_equip_value = tk.StringVar(value='0')
        self.current_arcaneforce_equip_combobox.configure(
            textvariable=self.current_arcaneforce_equip_value
        )

    def handle_table_arcanesymbols(self):
        self.table_symbol_name = ttk.Label(
            master = self.current_symbol_level,
            text = '  ',
            font = default_text,
            anchor = tk.S,
            width = 16
            )
        self.table_symbol_name.grid(row=0,column=0)

        self.table_symbol_level = ttk.Label(
            master = self.current_symbol_level,
            text = 'Lv.',
            font = default_text,
            anchor = tk.S,
            width = 6
            )
        self.table_symbol_level.grid(row=0,column=1)

        self.table_symbol_exp = ttk.Label(
            master = self.current_symbol_level,
            text = 'Exp',
            font = default_text,
            anchor = tk.S,
            width = 6
            )
        self.table_symbol_exp.grid(row=0,column=2)

        self.table_symbol_daily_quest = ttk.Label(
            master = self.current_symbol_level,
            text = 'Daily Quest',
            font = default_text,
            anchor = tk.S,
            width = 14
        )
        self.table_symbol_daily_quest.grid(row=0, column=3)

        ## --- title --------------------------------

        symbol_width = 20
        symbol_padding = 1
        symbol_entry_width = 3

        self.table_symbol_VJ = ttk.Label(
            master = self.current_symbol_level,
            text = ' Vanishing Journey',
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding
            )
        self.table_symbol_VJ.grid(row=1,column=0)
        self.table_symbol_VJ_lv_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_VJ_lv_entry.grid(row=1, column=1)
        self.table_symbol_VJ_exp_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_VJ_exp_entry.grid(row=1, column=2)

        self.table_symbol_CC = ttk.Label(
            master = self.current_symbol_level,
            text = ' ChuChu Island',
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding
            )
        self.table_symbol_CC.grid(row=2,column=0)
        self.table_symbol_CC_lv_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_CC_lv_entry.grid(row=2, column=1)
        self.table_symbol_CC_exp_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_CC_exp_entry.grid(row=2, column=2)

        self.table_symbol_Lach = ttk.Label(
            master = self.current_symbol_level,
            text = ' Lachelein',
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding
            )
        self.table_symbol_Lach.grid(row=3,column=0)
        self.table_symbol_Lach_lv_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Lach_lv_entry.grid(row=3, column=1)
        self.table_symbol_Lach_exp_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Lach_exp_entry.grid(row=3, column=2)

        self.table_symbol_Arcana = ttk.Label(
            master = self.current_symbol_level,
            text = ' Arcana',
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding
            )
        self.table_symbol_Arcana.grid(row=4,column=0)
        self.table_symbol_Arcana_lv_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Arcana_lv_entry.grid(row=4, column=1)
        self.table_symbol_Arcana_exp_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Arcana_exp_entry.grid(row=4, column=2)

        self.table_symbol_Morass = ttk.Label(
            master = self.current_symbol_level,
            text = ' Morass',
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding
            )
        self.table_symbol_Morass.grid(row=5,column=0)
        self.table_symbol_Morass_lv_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Morass_lv_entry.grid(row=5, column=1)
        self.table_symbol_Morass_exp_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Morass_exp_entry.grid(row=5, column=2)

        self.table_symbol_Esfera = ttk.Label(
            master = self.current_symbol_level,
            text = ' Esfera',
            font = default_text,
            anchor = tk.W,
            width = symbol_width,
            padding = symbol_padding
            )
        self.table_symbol_Esfera.grid(row=6,column=0)
        self.table_symbol_Esfera_lv_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Esfera_lv_entry.grid(row=6, column=1)
        self.table_symbol_Esfera_exp_entry = ttk.Entry(
            master = self.current_symbol_level,
            font = default_text,
            justify = tk.CENTER,
            width = symbol_entry_width,
            validate = 'key',
            validatecommand = self.int_only
            )
        self.table_symbol_Esfera_exp_entry.grid(row=6, column=2)

        self.table_symbol_pad = ttk.Label(
            master = self.current_symbol_level,
            text = ''
            )
        self.table_symbol_pad.grid(row=7,column=0)

        self.arcane_symbols_init()

    def arcane_symbols_init(self):
        print ('ArcaneForce.Function.arcane_symbols_init()')
        self.table_symbol_VJ_lv_entry_value = tk.StringVar(
            name = 'VJ_Symbol_lv',
            )
        self.table_symbol_VJ_lv_entry.configure(
            textvariable = self.table_symbol_VJ_lv_entry_value
            )
        self.table_symbol_VJ_lv_entry_value.trace_add(
            ['write','read','unset'],
            self.update_VJ_lv
            )
        self.table_symbol_VJ_exp_entry_value = tk.StringVar(
            name = 'VJ_Symbol_exp'
            )
        self.table_symbol_VJ_exp_entry.configure(
            textvariable = self.table_symbol_VJ_exp_entry_value
            )
        self.table_symbol_VJ_exp_entry_value.trace_add(
            ['write','read','unset'],
            self.update_VJ_exp
            )

        self.table_symbol_CC_lv_entry_value = tk.StringVar()
        self.table_symbol_CC_lv_entry.configure(
            textvariable = self.table_symbol_CC_lv_entry_value
        )
        self.table_symbol_CC_exp_entry_value = tk.StringVar()
        self.table_symbol_CC_exp_entry.configure(
            textvariable = self.table_symbol_CC_exp_entry_value
        )

        self.table_symbol_Lach_lv_entry_value = tk.StringVar()
        self.table_symbol_Lach_lv_entry.configure(
            textvariable = self.table_symbol_Lach_lv_entry_value
        )
        self.table_symbol_Lach_exp_entry_value = tk.StringVar()
        self.table_symbol_Lach_exp_entry.configure(
            textvariable = self.table_symbol_Lach_exp_entry_value
        )

        self.table_symbol_Arcana_lv_entry_value = tk.StringVar()
        self.table_symbol_Arcana_lv_entry.configure(
            textvariable = self.table_symbol_Arcana_lv_entry_value
        )
        self.table_symbol_Arcana_exp_entry_value = tk.StringVar()
        self.table_symbol_Arcana_exp_entry.configure(
            textvariable = self.table_symbol_Arcana_exp_entry_value
        )

        self.table_symbol_Morass_lv_entry_value = tk.StringVar()
        self.table_symbol_Morass_lv_entry.configure(
            textvariable = self.table_symbol_Morass_lv_entry_value
        )
        self.table_symbol_Morass_exp_entry_value = tk.StringVar()
        self.table_symbol_Morass_exp_entry.configure(
            textvariable = self.table_symbol_Morass_exp_entry_value
        )

        self.table_symbol_Esfera_lv_entry_value = tk.StringVar()
        self.table_symbol_Esfera_lv_entry.configure(
            textvariable = self.table_symbol_Esfera_lv_entry_value
        )
        self.table_symbol_Esfera_exp_entry_value = tk.StringVar()
        self.table_symbol_Esfera_exp_entry.configure(
            textvariable = self.table_symbol_Esfera_exp_entry_value
        )

    def update_VJ_lv(self,*args):
        print('ArcaneForce.Function.update_VJ_lv()')
        num = int(self.table_symbol_VJ_lv_entry_value.get())
        if self.table_symbol_VJ_lv_entry_value.get() != '':
            if int(num) > symbol_max_level:
                num = symbol_max_level
            self.table_symbol_VJ_lv_entry_value.set(int(num))
        print (args[2]+' to '+args[0]+' value:', num)

    def update_VJ_exp(self,*args):
        print('ArcaneForce.Function.update_VJ_exp()')
        num = int(self.table_symbol_VJ_exp_entry_value.get())
        if self.table_symbol_VJ_exp_entry_value.get() != '':
            if int(num) > symbol_exp[-1]:
                num = symbol_exp[-1]
            self.table_symbol_VJ_exp_entry_value.set(int(num))
        print (args[2]+' to '+args[0]+' value:', num)

    def update_CC_lv(self,*args):
        print('ArcaneForce.Function.update_CC_lv()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update_CC_exp(self,*args):
        print('ArcaneForce.Function.update_CC_exp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)

    def update__lvexp(self,*args):
        print('ArcaneForce.Function.update__lvexp()')
        num = int(self.table_symbol__lvexp_entry_value.get())
        self.table_symbol__lvexp_entry_value.set(num)


    def reset_combobox_selection(self, this):
        print ('ArcaneForce.Function.reset_combo_selection()')
        print ('From :', this.widget)
        print ('selected=', this.widget.get(), sep='')

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

    def _auto_text_space(self, text, totalsizeoftext):
        return '      ' + text + ' '*(totalsizeoftext-(len(text)+7))

    def test(self):
        print ('ArcaneForce.Function.test()')
        print (current_path)
        print (os.path.join(current_path, 'data'))

    def exit(self):
        print ('ArcaneForce.Function.exit()')
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

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
symbol_count = [
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
        self.current_arcaneforce.place(x=10,y=HEIGHT*.03)
        # self.current_arcaneforce.pack_propagate(0)
        self.handle_current_arcaneforce()

        self.current_date_estimates = tk.LabelFrame(
            master = self.body,
            text = ' Dates Till Max ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH*17/60, height = HEIGHT*.39
        )
        self.current_date_estimates.place(x=20+(WIDTH/3), y=HEIGHT*.03)
        self.current_date_estimates.pack_propagate(0)

        self.current_symbol_level = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Symbols ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH/3, height = HEIGHT*.41
        )
        self.current_symbol_level.place(x=10, y=HEIGHT*.45)
        self.current_symbol_level.pack_propagate(0)

        self.current_arcane_dailies = tk.LabelFrame(
            master = self.body,
            text = ' Arcane Dailies ',
            font = default_title,
            bd = 1, relief = 'ridge',
            width = WIDTH*75/120, height = HEIGHT*.41
        )
        self.current_arcane_dailies.place(x=20+(WIDTH/3), y=HEIGHT*.45)
        self.current_arcane_dailies.pack_propagate(0)

    def handle_current_arcaneforce(self):
        set_text_space = 20
        self.current_arcaneforce_symbol = tk.Label(
            master = self.current_arcaneforce,
            text = self.auto_text_space('Symbol:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
        self.current_arcaneforce_symbol.pack(anchor='w', pady=(5, 0))
        self.current_arcaneforce_symbol_value = tk.StringVar(value='0')
        self.current_arcaneforce_symbol_entry = ttk.Entry(
            master = self.current_arcaneforce_symbol,
            font = default_text,
            width = int(WIDTH/90),
            justify = tk.RIGHT,
            state = 'disabled'
            )
        self.current_arcaneforce_symbol_entry.configure(
            textvariable=self.current_arcaneforce_symbol_value
            )
        self.current_arcaneforce_symbol_entry.pack(padx=(140, 10), anchor='se')

        self.current_arcaneforce_hyper = tk.Label(
            master = self.current_arcaneforce,
            text = self.auto_text_space('Hyper Stats:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
        self.current_arcaneforce_hyper.pack(anchor='w')
        self.current_arcaneforce_hyper_value = tk.StringVar(value='0')
        self.current_arcaneforce_hyper_entry = ttk.Entry(
            master = self.current_arcaneforce_hyper,
            font = default_text,
            width = int(WIDTH/90),
            justify = tk.RIGHT,
            validate = 'key',
            validatecommand = self.int_only
        )
        self.current_arcaneforce_hyper_entry.configure(
            textvariable=self.current_arcaneforce_hyper_value
        )
        self.current_arcaneforce_hyper_entry.pack(padx=(140, 10), anchor='se')

        self.current_arcaneforce_guild = tk.Label(
            master = self.current_arcaneforce,
            text = self.auto_text_space('Guild Skill:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
        self.current_arcaneforce_guild.pack(anchor='w')
        self.current_arcaneforce_guild_value = tk.StringVar(value='0')
        self.current_arcaneforce_guild_entry = ttk.Entry(
            master = self.current_arcaneforce_guild,
            font = default_text,
            width = int(WIDTH/90),
            justify = tk.RIGHT
        )
        self.current_arcaneforce_guild_entry.configure(
            textvariable=self.current_arcaneforce_guild_value
        )
        self.current_arcaneforce_guild_entry.pack(padx=(140, 10), anchor='se')

        self.current_arcaneforce_equip = tk.Label(
            master = self.current_arcaneforce,
            text = self.auto_text_space('Equipments:', set_text_space),
            font = default_text,
            anchor = 'w'
        )
        self.current_arcaneforce_equip.pack(anchor='w', pady=(0, 10))
        self.current_arcaneforce_equip_value = tk.StringVar(value='0')
        self.current_arcaneforce_equip_entry = ttk.Entry(
            master = self.current_arcaneforce_equip,
            font = default_text,
            width = int(WIDTH/90),
            justify = tk.RIGHT
        )
        self.current_arcaneforce_equip_entry.configure(
            textvariable=self.current_arcaneforce_equip_value
        )
        self.current_arcaneforce_equip_entry.pack(padx=(140, 10), anchor='se')

        # --------------------------------------------------------------

        self.current_arcaneforce_total = tk.Label(
            master = self.current_arcaneforce,
            text = '  Total Arcane Force:',
            font = ('Inconsolata', 14),
            anchor = 'w'
        )
        # self.current_arcaneforce_total.pack(anchor='w')
        self.current_arcaneforce_total_value = tk.StringVar(value='1350')
        self.current_arcaneforce_total_result = tk.Label(
            master = self.current_arcaneforce_total,
            font = ('Inconsolata', 18),
            width = 4,
            anchor = 'e'
        )
        self.current_arcaneforce_total_result.configure(
            textvariable=self.current_arcaneforce_total_value
        )
        # self.current_arcaneforce_total_result.pack(padx=(160, 10), anchor='se')

    def validate_int_only(self, d, i, P, s, S, v, V, W):
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

    def auto_text_space(self, text, totalsizeoftext):
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

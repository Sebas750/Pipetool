from tkinter import *
import ttkbootstrap as ttk
from instrument import instrument

class mainApp():
    def __init__(self, root) -> None:
        
        self.instrument = None
        self.notes = None
        self.new_tab = None
        self.previous_tab = 'Instrument'

        # Set root window
        self.root = root

        # Set main style for the window
        self.style = ttk.Style(theme='sober')
        self.style.configure('.', font=('Helvetica', 10))
        self.style.configure('TNotebook', padding=0)
        self.style.configure('Main.TNotebook', tabposition='n', padding=0)
        self.style.map('TNotebook.Tab', background=[('selected', 'white')], foreground=[('selected', 'black'), ('disabled', 'grey')])
        self.style.configure('TFrame', background='white', padding=0)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title('Pipe tool')

        # Set main notebook tabs in the middle of the window
        self.style.configure('Main.TNotebook', tabposition='n')

        # TODO: Make it work on Windows, and mac
        self.root.attributes('-zoomed', True)

        #### Main window ####
        self.main_window = ttk.Notebook(self.root, style='Main.TNotebook')
        self.main_window.grid(column=0, row=0, sticky=(N, W, E, S))

        self.instrument_frame = instrument(self.root, self.main_window, self.style)
        self.impedance_frame = Frame(self.main_window)
        self.resonance_frame = Frame(self.main_window)
        self.inharmonicity_frame = Frame(self.main_window)

        # Add frames to main notebook
        self.main_window.add(self.instrument_frame.instrument_frame, text='Instrument')
        self.main_window.add(self.impedance_frame, text='Impedance')
        self.main_window.add(self.resonance_frame, text='Resonance')
        self.main_window.add(self.inharmonicity_frame, text='Inharmonicity')

        # Set this main notebook tabs to be disabled at the beginning
        self.main_window.tab(1, state='disabled')
        self.main_window.tab(2, state='disabled')
        self.main_window.tab(3, state='disabled')

root = ttk.Window()
mainApp(root)
root.mainloop()
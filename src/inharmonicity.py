# Tkinter
from tkinter import *
from tkinter import ttk

# Matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec

# File management
from shutil import rmtree
from os import makedirs
from os.path import dirname, abspath, join, exists

# NumPy
import numpy as np

class inharmonicity():
    def __init__(self, root=None, style=None, parent=None, instrument=None,
            res_f=None, table_info=None, simulation_notes=None, notes=None,
            number_peaks=None) -> None:
        
        self.sytle = style
        self.root = root
        # Set parent
        self.parent = parent
        self.instrument = instrument
        self.res_f = res_f
        self.table_info = table_info
        self.simulation_notes = simulation_notes
        self.notes = notes
        self.number_peaks = number_peaks
        self.nat_in = self.natural_inharmonicity()
        self.octaves_cent = self.get_octave_cents()
        self.inharmo = self.inharmo_plot()
        self.tuning = True
        self.enable_octave = [True] * 3
        self.enable_inharmo = [True] * 2
        self.view_frame_middle = None
        self.view_frame_top_inhar = None
        
        
        self.colors = ['#F44346', '#9C27B0', '#3F51B5', '#03A9F4', '#009688', 
            '#8BC34A', '#FFEB3B', '#FF9800', '#795548', '#607D8B', 
            '#37474F', '#9E9E9E', '#FF5722', '#FFC107', '#CDDC39', 
            '#4CAF50', '#00BCD4', '#2196F3', '#673AB7', '#E91E63', 
            '#F44346', '#9C27B0', '#3F51B5', '#03A9F4', '#009688', 
            '#8BC34A', '#FFEB3B', '#FF9800', '#795548', '#607D8B', 
            '#37474F', '#9E9E9E', '#FF5722', '#FFC107', '#CDDC39', 
            '#4CAF50', '#00BCD4', '#2196F3', '#673AB7', '#E91E63']
        
        self.message = StringVar()
        self.message.set('INHARMONICITY')
        
        self.create_widgets(parent)
        self.table_widgets()
        self.view_widgets()
        
    def create_widgets(self, parent):
        # Instrument main frame
        self.inharmo_frame = ttk.Frame(parent)
        self.inharmo_frame.columnconfigure(0, weight=1)
        self.inharmo_frame.columnconfigure(1, weight=1)
        self.inharmo_frame.rowconfigure(0, weight=1)
        self.inharmo_frame.grid_propagate(0)
        
        # Instrumenr left frame
        self.inharmo_left_frame = ttk.Frame(self.inharmo_frame)
        self.inharmo_left_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.inharmo_left_frame.columnconfigure(0, weight=1)
        self.inharmo_left_frame.rowconfigure(0, weight=1)
        self.inharmo_left_frame.grid_propagate(0)
        
        # Instrument right frame
        self.inharmo_right_frame = ttk.Frame(self.inharmo_frame)
        self.inharmo_right_frame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.inharmo_right_frame.columnconfigure(0, weight=1)
        self.inharmo_right_frame.rowconfigure(0, weight=1)
        self.inharmo_right_frame.grid_propagate(0)
        
        # Instrument left notebook
        self.inharmo_left_notebook = ttk.Notebook(self.inharmo_left_frame)
        self.inharmo_left_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.inharmo_left_notebook.columnconfigure(0, weight=1)
        self.inharmo_left_notebook.rowconfigure(0, weight=1)
        self.inharmo_left_notebook.grid_propagate(0)
        
        # Instrument right notebook
        self.inharmo_right_notebook = ttk.Notebook(self.inharmo_right_frame)
        self.inharmo_right_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.inharmo_right_notebook.columnconfigure(0, weight=1)
        self.inharmo_right_notebook.rowconfigure(0, weight=1)
        self.inharmo_right_notebook.grid_propagate(0)  
        
    def table_widgets(self):
        self.table_frame = ttk.Frame(self.inharmo_left_notebook)
        self.inharmo_left_notebook.add(self.table_frame, text='Inharmonicity table')
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=2)
        self.table_frame.rowconfigure(1, weight=36)
        self.table_frame.rowconfigure(3, weight=2)
        self.table_frame.grid_propagate(0)
        
        # Table top subframe
        self.table_frame_top = ttk.Frame(self.table_frame)
        self.table_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.table_frame_top.columnconfigure(0, weight=1)
        self.table_frame_top.columnconfigure(1, weight=1)
        self.table_frame_top.rowconfigure(0, weight=1)
        self.table_frame_top.grid_propagate(0)
        
        self.table_frame_top_label = ttk.Label(self.table_frame_top, text='Number partials:')
        self.table_frame_top_label.grid(column=0, row=0, sticky=(N, E, W, S), padx=2, pady=2)
        self.table_frame_top_number_peaks = ttk.Combobox(self.table_frame_top, values=[1, 2, 3], state='readonly')
        self.table_frame_top_number_peaks.current(2)
        self.table_frame_top_number_peaks.bind('<<ComboboxSelected>>', lambda event, x='': self.update_table(x))
        self.table_frame_top_number_peaks.grid(column=1, row=0, sticky=(N, E, W, S), padx=2, pady=2)
        
        # Table middle subframe
        self.update_table()     

        # Table bottom subframe
        self.table_frame_bottom = ttk.Frame(self.table_frame) 
        self.table_frame_bottom.grid(column=0, row=3, sticky=(N, W, E, S), padx=2, pady=2)
        self.table_frame_bottom.columnconfigure(0, weight=1)
        self.table_frame_bottom.rowconfigure(0, weight=1)
        self.table_frame_bottom.grid_propagate(0)
        
        self.table_frame_bottom_label = ttk.Label(self.table_frame_bottom, textvariable=self.message, anchor='center', justify='center')
        self.table_frame_bottom_label.grid(column=0, row=0, sticky=(W, E, S, N))
        
    def view_widgets(self):
        self.view_frame = ttk.Frame(self.inharmo_right_notebook)
        self.inharmo_right_notebook.add(self.view_frame, text='Inharmoniciy view')
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.rowconfigure(0, weight=2)
        self.view_frame.rowconfigure(1, weight=36)
        self.view_frame.rowconfigure(3, weight=2)
        self.view_frame.grid_propagate(0)
        
        # Table top subframe
        self.view_frame_top = ttk.Frame(self.view_frame)
        self.view_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top.rowconfigure(0, weight=1)
        self.view_frame_top.columnconfigure(0, weight=1)
        self.view_frame_top.columnconfigure(1, weight=1)
        self.view_frame_top.columnconfigure(2, weight=1)
        self.view_frame_top.columnconfigure(3, weight=1)
        self.view_frame_top.columnconfigure(4, weight=1)
        self.view_frame_top.grid_propagate(0)
        
        self.view_frame_top_name_label = ttk.Label(self.view_frame_top, text='Name:', anchor='center', justify='center')
        self.view_frame_top_name_label.grid(column=0, row=0, sticky=(N, S, W, E), pady=2)
        self.view_frame_top_name_label.grid_propagate(0)
        self.view_frame_top_name = ttk.Entry(self.view_frame_top, width=10)
        self.view_frame_top_name.grid(column=1, row=0, sticky=(N, S, W, E), padx=2, pady=2)
        self.view_frame_top_name.grid_propagate(0)
        self.view_frame_top_export = ttk.Button(self.view_frame_top, text='Export to files', command=self.export, style='primary.Outline.TButton')
        self.view_frame_top_export.grid(column=2, row=0, sticky=(N, W, S), padx=2, pady=2)
        self.view_frame_top_export.grid_propagate(0)
        self.view_frame_top_pitch = ttk.Button(self.view_frame_top, text='Instrument pitch', style='primary.Outline.TButton')
        self.view_frame_top_pitch.grid(column=3, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top_pitch.bind('<Button-1>', lambda event, x=True: self.change_inharmo(x))
        self.view_frame_top_inhar = ttk.Button(self.view_frame_top, text='Instrument inharmonicity', style='primary.Outline.TButton')
        self.view_frame_top_inhar.grid(column=4, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top_inhar.bind('<Button-1>', lambda event, x=False: self.change_inharmo(x))
        
        # Table middle subframe
        self.view_frame_middle = ttk.Frame(self.view_frame)
        self.view_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_middle.columnconfigure(0, weight=1)
        self.view_frame_middle.rowconfigure(0, weight=1)
        self.view_frame_middle.grid_propagate(0)
        
        self.plot()
            
        # Table bottom subframe
        self.view_frame_bottom = ttk.Frame(self.view_frame)
        self.view_frame_bottom.grid(column=0, row=3, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_bottom.columnconfigure(0, weight=1)
        self.view_frame_bottom.rowconfigure(0, weight=1)
        self.view_frame_bottom.grid_propagate(0)
        
        self.display_enable_buttons()

    def update_table(self, x=None):
        self.number_peaks = int(self.table_frame_top_number_peaks.get())
        self.number_peaks += 1
        
        if self.view_frame_top_inhar:
            if self.number_peaks == 2:
                self.tuning = True
                self.view_frame_top_inhar.state(['disabled'])
            else:
                self.view_frame_top_inhar.state(['!disabled'])
        
        self.entries = []
        for j, elem in enumerate(self.simulation_notes):
            element = []
            element.append(elem)
            clo_f = self.table_info[elem][0]
            cent_diff = self.table_info[elem][1]
            names = self.table_info[elem][2]
            for i in range(self.number_peaks):
                data = f'{names[i]}: {clo_f[i]:.2f} Hz {cent_diff[i]:.2f} cents'
                element.append(data)
            self.entries.append(element)

        # Natural table
        self.table_frame_middle = ttk.Frame(self.table_frame, borderwidth=2, relief='sunken')
        self.table_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.table_frame_middle.columnconfigure(0, weight=1)
        self.table_frame_middle.rowconfigure(0, weight=1)
        for i in range(self.number_peaks):
            self.table_frame_middle.columnconfigure(i + 1, weight=1)
        for i in range(len(self.simulation_notes)):
            self.table_frame_middle.rowconfigure(i + 1, weight=1)
        self.table_frame_middle.grid_propagate(0)

        ttk.Label(self.table_frame_middle, text='Note').grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        ttk.Label(self.table_frame_middle, text='Fundamental (Hz)').grid(column=1, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        for i in range(self.number_peaks - 1):
            ttk.Label(self.table_frame_middle, text=f'{i + 1}° partial (Hz)').grid(column=i + 2, row=0, sticky=(N, W, E, S), padx=2, pady=2)

        self.entries = []
        for j, elem in enumerate(self.simulation_notes):
            element = []
            element.append(elem)
            name = self.table_info[elem][2][0]
            fundamental = f'{round(self.res_f[elem][0], 2)} Hz'
            element.append(fundamental)
            for i in range(self.number_peaks - 1):
                data = f'{self.res_f[elem][i + 1]:.2f} Hz'
                element.append(data)
            self.entries.append(element)
        
        k = 0
        for i, elem in enumerate(self.entries):
            k = i
            for j in range(self.number_peaks + 1):
                ttk.Label(self.table_frame_middle, text=elem[j]).grid(column=j, row=i + 1, sticky=(N, W, E, S), padx=2, pady=2)    
                    
        if self.view_frame_middle:
            self.nat_in = self.natural_inharmonicity()
            self.octaves_cent = self.get_octave_cents()
            self.inharmo = self.inharmo_plot()
            self.display_enable_buttons()
            self.plot()
            
        
    def display_enable_buttons(self):
        self.enable_octave = [True] * (self.number_peaks - 1)
        self.enable_inharmo = [True] * (self.number_peaks - 2)
        
        for widget in self.view_frame_bottom.winfo_children():
            widget.destroy()
            
        if self.tuning:  
            for i in range(self.number_peaks):
                self.view_frame_bottom.columnconfigure(2 * i, weight=1)
                self.view_frame_bottom.columnconfigure(2 * i + 1, weight=1)
            self.view_frame_bottom.rowconfigure(0, weight=1)
            self.view_frame_bottom.grid_propagate(0)
            
            self.view_frame_bottom_frames = list()
            for i in range((self.number_peaks) - 1):
                self.view_frame_bottom_label = ttk.Label(self.view_frame_bottom, text=f'{i + 1}° partial:', anchor='center', justify='center')
                self.view_frame_bottom_label.grid(column=2 * i + 1, row=0, sticky=(E, S, N), padx=2, pady=2)
                self.view_frame_bottom_frame = Frame(self.view_frame_bottom, width=24)
                self.view_frame_bottom_frame.configure(background=self.colors[i], highlightbackground=self.colors[i], highlightthickness=1)
                self.view_frame_bottom_frame.grid(column=2 * i + 2, row=0, sticky=(W, E, S, N), pady=5)
                self.view_frame_bottom_frame.rowconfigure(0, weight=1)
                self.view_frame_bottom_frame.grid_propagate(0)
                self.view_frame_bottom_frame.bind('<Button-1>', lambda event, x=i: self.change_plot(x))
                self.view_frame_bottom_frames.append(self.view_frame_bottom_frame)
        else:
            for i in range(self.number_peaks - 1):
                self.view_frame_bottom.columnconfigure(2 * i, weight=1)
                self.view_frame_bottom.columnconfigure(2 * i + 1, weight=1)
            self.view_frame_bottom.rowconfigure(0, weight=1)
            self.view_frame_bottom.grid_propagate(0)
            
            self.view_frame_bottom_frames = list()
            for i in range((self.number_peaks) - 2):
                self.view_frame_bottom_label = ttk.Label(self.view_frame_bottom, text=f'{i + 2}° partial vs {i + 1}° partial:', anchor='center', justify='center')
                self.view_frame_bottom_label.grid(column=2 * i + 1, row=0, sticky=(E, S, N), padx=2, pady=2)
                self.view_frame_bottom_frame = Frame(self.view_frame_bottom, width=24)
                self.view_frame_bottom_frame.configure(background=self.colors[i + 3], highlightbackground=self.colors[i + 3], highlightthickness=1)
                self.view_frame_bottom_frame.grid(column=2 * i + 2, row=0, sticky=(W, E, S, N), pady=5)
                self.view_frame_bottom_frame.rowconfigure(0, weight=1)
                self.view_frame_bottom_frame.grid_propagate(0)
                self.view_frame_bottom_frame.bind('<Button-1>', lambda event, x=i: self.change_plot(x))
                self.view_frame_bottom_frames.append(self.view_frame_bottom_frame)
            
    
    def plot(self):
        plt.close()
        self.view_figure = plt.figure(figsize=(1, 1), dpi=100)
        position = [0, 0, 0.5, 1]
        gs = gridspec.GridSpec(1, 1)
        gs.tight_layout(self.view_figure, rect=position)
        plt.grid()
        if self.tuning:
            plt.title('Instrument tuning')
            plt.ylabel('Difference between theoric and real partials (cents)')
            for i, element in enumerate(self.octaves_cent):
                if self.enable_octave[i]:
                    plt.plot(element, 'o--', color=self.colors[i])
                    plt.xticks(np.arange(0, len(self.simulation_notes)), self.simulation_notes)
        else:
            plt.title('Instrument inharmonicity')
            plt.ylabel('Difference between partials (cents)')
            for i, element in enumerate(self.inharmo):
                if self.enable_inharmo[i]:
                    plt.plot(element, 'o--', color=self.colors[i + 3])
                    plt.xticks(np.arange(0, len(self.simulation_notes)), self.simulation_notes)

        
        # Create canvas with figure
        canvas = FigureCanvasTkAgg(self.view_figure, self.view_frame_middle)
        canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, W, E, S), pady=10)
        
    def change_inharmo(self, x):
        if self.tuning != x:
            self.tuning = x
            self.plot()
            self.display_enable_buttons()
        
    def change_plot(self, x):
        if self.tuning:
            if self.enable_octave[x] == True:
                self.enable_octave[x] = False
                self.view_frame_bottom_frames[x].configure(background='#FFFFFF')
            else:
                self.enable_octave[x] = True
                self.view_frame_bottom_frames[x].configure(background=self.colors[x])
            self.plot()

        else:
            if self.enable_inharmo[x] == True:
                self.enable_inharmo[x] = False
                self.view_frame_bottom_frames[x].configure(background='#FFFFFF')
            else:
                self.enable_inharmo[x] = True
                self.view_frame_bottom_frames[x].configure(background=self.colors[x + 3])
            self.plot()

    def inharmo_plot(self):
        inharmo = []
        for i in range(len(self.octaves_cent) - 1):
            inhar_elem = []
            for j in range(len(self.octaves_cent[i])):
                inhar_elem.append(self.octaves_cent[i + 1][j] - self.octaves_cent[i][j])
            inharmo.append(inhar_elem)
        
        for i in range(len(inharmo)):
            print(inharmo[i])
        print('\n')
        return inharmo
            
            

    def natural_inharmonicity(self):
        nat_in = {}
        for note in self.simulation_notes:
            nat_note = list()
            natural_fundamental = self.res_f[note][0]
            for i, elem in enumerate(self.res_f[note][1:]):
                frecuency_diff = elem / (natural_fundamental * (i + 2))
                cent_diff = 1200 * np.log2(frecuency_diff)
                print(f'{note} {i + 1}° partial: {cent_diff:.2f} cents')
                nat_note.append(cent_diff)
            nat_in.update({note: nat_note})
        
        return nat_in

    def get_octave_cents(self):
        octaves_cents = []
        for i in range(self.number_peaks - 1):
            octave_overtone = []
            for j in range(len(self.simulation_notes)):
                octave_overtone.append(self.nat_in[self.simulation_notes[j]][i])
            octaves_cents.append(octave_overtone)
        
        for i in range(len(octaves_cents)):
            print(octaves_cents[i])
        print('\n')
        return octaves_cents
    
    def export(self):
        name = self.view_frame_top_name.get()
        if name != '':
            # Create files with instrument data
            path = dirname(abspath(__file__))
            folder_path = join(path, f'{name}_inharmonicity')
            if exists(folder_path):
                try:
                    rmtree(folder_path)
                except Exception as e:
                    print(f"Error deleting '{folder_path}': {e}")
            makedirs(folder_path)
                
            for i, note in enumerate(self.simulation_notes):
                with open(join(folder_path, f'{name}_{note}_inhermonicity.txt'), 'w') as file:
                    string = '# Inharmonicity between partials (cents) \n'
                    file.write(string + '\n')
                    for j in range(len(self.inharmo)):
                        string += f' {j + 2}° partial vs {j + 1}° partial \n'
                        file.write(string)
                        file.write(f' {self.inharmo[j][i]} \n')
                        string = ''
                    

            self.message.set('Files exported successfully')
        else:
            self.message.set('Please enter a name for the folder')
        
def is_float(s):
    try:
        float_value = float(s)
        return True
    except ValueError:
        return False
    
def is_int(s):
    try:
        int_value = int(s)
        return True
    except ValueError:
        return False

def normalize_color(color):
    return tuple([i/255 for i in color])
    
def traverse(list):
    traverse = [[0] * len(list) for _ in range(len(list[0]))]

    for j in range(len(list[0])):
        for i in range(len(list)):
            traverse[j][i] = list[i][j]
    
    return traverse


            
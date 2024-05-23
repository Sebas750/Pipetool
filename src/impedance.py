# Tkinter
from tkinter import *
from tkinter import ttk

# File management
from shutil import rmtree
from os import makedirs
from os.path import dirname, abspath, join, exists

# Matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec

# NumPy
import numpy as np

# Openwind
from openwind import InstrumentGeometry, InstrumentPhysics, FrequentialSolver, Player, ImpedanceComputation
from openwind.continuous import radiation_model
from openwind.impedance_tools import resonance_peaks_from_phase, match_freqs_with_notes, antiresonance_peaks_from_phase

# Resonance class
from resonance import resonance


class impedance():
    def __init__(self, root=None, parent=None, style=None, instrument=None, 
        bore=None, holes=None, fingers=None, notes=None,
        unit=None, diameter=None) -> None:
        
        self.root = root
        # Set parent
        self.style = style
        self.parent = parent
        self.instrument = instrument
        self.notes = notes
        self.to_plot_notes = [True] * len(self.notes)
        self.enable_notes = [True] * len(self.notes)
        self.bore_sections = bore
        self.holes = holes
        self.finger_chart = fingers
        self.diameter = diameter
        self.unit = unit
        
        self.colors = ['#F44346', '#9C27B0', '#3F51B5', '#03A9F4', '#009688', 
            '#8BC34A', '#FFEB3B', '#FF9800', '#795548', '#607D8B', 
            '#37474F', '#9E9E9E', '#FF5722', '#FFC107', '#CDDC39', 
            '#4CAF50', '#00BCD4', '#2196F3', '#673AB7', '#E91E63']
        
        # variables
        self.mesagge = StringVar()
        self.mesagge.set('Impedance section')
        
        # Instrument main frame
        self.simulation_notes = None
        self.temperature = None
        self.from_frecuency = None
        self.to_frecuency = None
        self.frecuency_step = None
        self.embrouchure = None
        self.concert_pitch = None
        self.transposition = None
        self.linear_scale = False
        self.freq = None
        
        self.create_widgets(parent)
        self.parameters_widgets()
        self.simulation_widgets()
    
    def create_widgets(self, parent):
        # Instrument main frame
        self.impedance_frame = ttk.Frame(parent)
        self.impedance_frame.columnconfigure(0, weight=1)
        self.impedance_frame.columnconfigure(1, weight=1)
        self.impedance_frame.rowconfigure(0, weight=1)
        self.impedance_frame.grid_propagate(0)
        
        # Instrumenr left frame
        self.impedance_left_frame = ttk.Frame(self.impedance_frame)
        self.impedance_left_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.impedance_left_frame.columnconfigure(0, weight=1)
        self.impedance_left_frame.rowconfigure(0, weight=1)
        self.impedance_left_frame.grid_propagate(0)
        
        # Instrument right frame
        self.impedance_right_frame = ttk.Frame(self.impedance_frame)
        self.impedance_right_frame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.impedance_right_frame.columnconfigure(0, weight=1)
        self.impedance_right_frame.rowconfigure(0, weight=1)
        self.impedance_right_frame.grid_propagate(0)
        
        # Instrument left notebook
        self.impedance_left_notebook = ttk.Notebook(self.impedance_left_frame)
        self.impedance_left_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.impedance_left_notebook.columnconfigure(0, weight=1)
        self.impedance_left_notebook.rowconfigure(0, weight=1)
        self.impedance_left_notebook.grid_propagate(0)
        
        # Instrument right notebook
        self.impedance_right_notebook = ttk.Notebook(self.impedance_right_frame)
        self.impedance_right_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.impedance_right_notebook.columnconfigure(0, weight=1)
        self.impedance_right_notebook.rowconfigure(0, weight=1)
        self.impedance_right_notebook.grid_propagate(0)  
    
    def parameters_widgets(self):
        self.parameter_frame = ttk.Frame(self.impedance_left_notebook)
        self.impedance_left_notebook.add(self.parameter_frame, text='Parameters')
        self.parameter_frame.columnconfigure(0, weight=1)
        self.parameter_frame.rowconfigure(0, weight=2)
        self.parameter_frame.rowconfigure(1, weight=36)
        self.parameter_frame.rowconfigure(2, weight=2)
        self.parameter_frame.grid_propagate(0)
        
        # Parameter top subframe
        self.parameter_frame_top = ttk.Frame(self.parameter_frame)
        self.parameter_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.parameter_frame_top.columnconfigure(0, weight=1)
        self.parameter_frame_top.columnconfigure(1, weight=1)
        self.parameter_frame_top.rowconfigure(0, weight=1)
        self.parameter_frame_top.grid_propagate(0)
        
        self.parameter_frame_top_clear = ttk.Button(self.parameter_frame_top, text='Clear parameters', command=self.clear_parameters, style='primary.Outline.TButton')
        self.parameter_frame_top_clear.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.parameter_frame_top_compute = ttk.Button(self.parameter_frame_top, text='Compute', command=self.print_computing, style='primary.Outline.TButton')
        self.parameter_frame_top_compute.grid(column=1, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.parameter_frame_top_clear.state(['disabled'])

        # Parameter middle subframe
        self.parameter_frame_middle = ttk.Frame(self.parameter_frame)
        self.parameter_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.parameter_frame_middle.columnconfigure(0, weight=1)
        self.parameter_frame_middle.rowconfigure(0, weight=1)
        self.parameter_frame_middle.rowconfigure(1, weight=1)
        self.parameter_frame_middle.rowconfigure(2, weight=1)
        self.parameter_frame_middle.grid_propagate(0)
        
        # main parameters subframe
        self.parameter_frame_middle_main = ttk.Frame(self.parameter_frame_middle)
        self.parameter_frame_middle_main.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.parameter_frame_middle_main.columnconfigure(0, weight=8)
        self.parameter_frame_middle_main.columnconfigure(1, weight=1)
        self.parameter_frame_middle_main.columnconfigure(2, weight=1)
        self.parameter_frame_middle_main.columnconfigure(3, weight=1)
        self.parameter_frame_middle_main.columnconfigure(4, weight=1)
        self.parameter_frame_middle_main.columnconfigure(5, weight=1)
        self.parameter_frame_middle_main.rowconfigure(0, weight=1)
        self.parameter_frame_middle_main.rowconfigure(1, weight=1)
        self.parameter_frame_middle_main.rowconfigure(2, weight=1)
        self.parameter_frame_middle_main.rowconfigure(3, weight=1)
        self.parameter_frame_middle_main.grid_propagate(0)
        
        self.parameter_frame_middle_main_notes_label = ttk.Label(self.parameter_frame_middle_main, text='Notes to simulate', anchor='center', justify='center')
        self.parameter_frame_middle_main_notes_label.grid(column=0, row=0, sticky=(E, S, N), padx=2, pady=2)
        notes = ['all'] + self.notes
        self.parameter_frame_middle_main_notes = ttk.Combobox(self.parameter_frame_middle_main, values=notes, state='readonly', width=5)
        self.parameter_frame_middle_main_notes.grid(column=1, row=0, columnspan=5, sticky=(W), padx=5, pady=5)
        self.parameter_frame_middle_main_notes.current(0)
        self.parameter_frame_middle_main_temperate_label = ttk.Label(self.parameter_frame_middle_main, text='Temperature [°C]', anchor='center', justify='center')
        self.parameter_frame_middle_main_temperate_label.grid(column=0, row=1, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_main_temperate = ttk.Entry(self.parameter_frame_middle_main, width=5)
        self.parameter_frame_middle_main_temperate.grid(column=1, row=1, pady=5)
        self.parameter_frame_middle_main_temperate.insert(0, '25')
        self.parameter_frame_middle_main_frecuency_label = ttk.Label(self.parameter_frame_middle_main, text='Frecuency range [Hz]', anchor='center', justify='center')
        self.parameter_frame_middle_main_frecuency_label.grid(column=0, row=2, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_main_frecuency_from_entry = ttk.Entry(self.parameter_frame_middle_main, width=5)
        self.parameter_frame_middle_main_frecuency_from_entry.grid(column=1, row=2, pady=5)
        self.parameter_frame_middle_main_frecuency_from_entry.insert(0, '20')
        self.parameter_frame_middle_main_frecuency_to = ttk.Label(self.parameter_frame_middle_main, text='To', anchor='center', justify='center')
        self.parameter_frame_middle_main_frecuency_to.grid(column=2, row=2, sticky=(W, S, N, E), padx=2, pady=2)
        self.parameter_frame_middle_main_frecuency_to_entry = ttk.Entry(self.parameter_frame_middle_main, width=5)
        self.parameter_frame_middle_main_frecuency_to_entry.grid(column=3, row=2, pady=5)
        self.parameter_frame_middle_main_frecuency_to_entry.insert(0, '5000')
        self.parameter_frame_middle_main_frecuency_step = ttk.Label(self.parameter_frame_middle_main, text='Step:', anchor='center', justify='center')
        self.parameter_frame_middle_main_frecuency_step.grid(column=4, row=2, sticky=(W, S, N, E), padx=[2, 5], pady=2)
        self.parameter_frame_middle_main_frecuency_step_entry = ttk.Entry(self.parameter_frame_middle_main, width=5)
        self.parameter_frame_middle_main_frecuency_step_entry.grid(column=5, row=2, pady=5)
        self.parameter_frame_middle_main_frecuency_step_entry.insert(0, '1')
        self.parameter_frame_middle_main_embouchure_label = ttk.Label(self.parameter_frame_middle_main, text='Embouchure type', anchor='center', justify='center')
        self.parameter_frame_middle_main_embouchure_label.grid(column=0, row=3, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_main_embouchure = ttk.Checkbutton(self.parameter_frame_middle_main, style='primary.Roundtoggle.Toolbutton')
        self.parameter_frame_middle_main_embouchure.grid(column=1, row=3, columnspan=5, sticky=(E, W), padx=2, pady=2)
        
        if float(self.bore_sections[0][0]) < 0 and float(self.bore_sections[0][1]) == 0 and \
           float(self.bore_sections[0][2]) == float(self.bore_sections[0][3]) and \
           float(self.bore_sections[0][3]) <= float(self.bore_sections[1][2]):
            if self.holes[1][0] == 'HJ' and float(self.holes[1][1]) == 1:
                for element in self.finger_chart:
                    if element[0] == 'HJ':
                        all_closed = True
                        for i in range(1, len(element)):
                            if element[i] == 'o':
                                all_closed = False
                                break
                        if all_closed:
                            self.parameter_frame_middle_main_embouchure.state(['!disabled'])
        else:
            self.parameter_frame_middle_main_embouchure.state(['disabled'])
                        
        

        # pitch parameters subframe
        self.parameter_frame_middle_pitch = ttk.Frame(self.parameter_frame_middle)
        self.parameter_frame_middle_pitch.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.parameter_frame_middle_pitch.columnconfigure(0, weight=1)
        self.parameter_frame_middle_pitch.columnconfigure(1, weight=1)
        self.parameter_frame_middle_pitch.rowconfigure(0, weight=1)
        self.parameter_frame_middle_pitch.rowconfigure(1, weight=1)
        self.parameter_frame_middle_pitch.grid_propagate(0)
        
        self.parameter_frame_middle_concert_pitch_label = ttk.Label(self.parameter_frame_middle_pitch, text='Concert pitch:', anchor='center', justify='center')
        self.parameter_frame_middle_concert_pitch_label.grid(column=0, row=0, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_concert_pitch = ttk.Entry(self.parameter_frame_middle_pitch, width=5)
        self.parameter_frame_middle_concert_pitch.grid(column=1, row=0, sticky=(W), pady=5)
        self.parameter_frame_middle_concert_pitch.insert(0, '440')
        self.parameter_frame_middle_pitch_transposition_label = ttk.Label(self.parameter_frame_middle_pitch, text='Transposition:', anchor='center', justify='center')
        self.parameter_frame_middle_pitch_transposition_label.grid(column=0, row=1, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_pitch_transposition = ttk.Combobox(self.parameter_frame_middle_pitch, values=['Eb','F' ,'A' ,'Bb' ,'C', 'F+' ,'A+'], state='readonly', width=5)
        self.parameter_frame_middle_pitch_transposition.grid(column=1, row=1, sticky=(W), pady=5)
        self.parameter_frame_middle_pitch_transposition.current(4)
        # advanced parameters subframe
        self.parameter_frame_middle_advanced = ttk.Frame(self.parameter_frame_middle)
        self.parameter_frame_middle_advanced.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        self.parameter_frame_middle_advanced.columnconfigure(0, weight=1)
        self.parameter_frame_middle_advanced.columnconfigure(1, weight=1)
        self.parameter_frame_middle_advanced.rowconfigure(0, weight=1)
        self.parameter_frame_middle_advanced.rowconfigure(1, weight=1)
        self.parameter_frame_middle_advanced.rowconfigure(2, weight=1)
        self.parameter_frame_middle_advanced.grid_propagate(0)
        
        self.parameter_frame_middle_advanced_opcion_1_label = ttk.Label(self.parameter_frame_middle_advanced, text='Not implemented:', anchor='center', justify='center')
        self.parameter_frame_middle_advanced_opcion_1_label.grid(column=0, row=0, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_advanced_opcion_1 = ttk.Combobox(self.parameter_frame_middle_advanced, values=['1', '2'], state='readonly', width=5)
        self.parameter_frame_middle_advanced_opcion_1.grid(column=1, row=0, sticky=(W), pady=5)
        self.parameter_frame_middle_advanced_opcion_1.current(0)
        self.parameter_frame_middle_advanced_opcion_2_label = ttk.Label(self.parameter_frame_middle_advanced, text='Not implemented:', anchor='center', justify='center')
        self.parameter_frame_middle_advanced_opcion_2_label.grid(column=0, row=1, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_advanced_opcion_2 = ttk.Combobox(self.parameter_frame_middle_advanced, values=['1', '2'], state='readonly', width=5)
        self.parameter_frame_middle_advanced_opcion_2.grid(column=1, row=1, sticky=(W), pady=5)
        self.parameter_frame_middle_advanced_opcion_2.current(0)
        self.parameter_frame_middle_advanced_opcion_3_label = ttk.Label(self.parameter_frame_middle_advanced, text='Not implemented:', anchor='center', justify='center')
        self.parameter_frame_middle_advanced_opcion_3_label.grid(column=0, row=2, sticky=(E, S, N), padx=2, pady=2)
        self.parameter_frame_middle_advanced_opcion_3 = ttk.Checkbutton(self.parameter_frame_middle_advanced, style='primary.Roundtoggle.Toolbutton')
        self.parameter_frame_middle_advanced_opcion_3.grid(column=1, row=2, sticky=(W), pady=5)

        # Parameter bottom subframe
        self.parameter_frame_bottom = ttk.Frame(self.parameter_frame) 
        self.parameter_frame_bottom.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        self.parameter_frame_bottom.columnconfigure(0, weight=1)
        self.parameter_frame_bottom.rowconfigure(0, weight=1)
        self.parameter_frame_bottom.grid_propagate(0)
        
        self.parameter_frame_bottom_label = ttk.Label(self.parameter_frame_bottom, textvariable=self.mesagge, anchor='center', justify='center')
        self.parameter_frame_bottom_label.grid(column=0, row=0, sticky=(W, E, S, N))
        
    def simulation_widgets(self):
        # Simulation frame
        self.simulation_frame = ttk.Frame(self.impedance_right_notebook)
        self.impedance_right_notebook.add(self.simulation_frame, text='Instrument')
        self.impedance_right_notebook.tab(0, state='disabled')
        self.simulation_frame.columnconfigure(0, weight=1)
        self.simulation_frame.rowconfigure(0, weight=2)
        self.simulation_frame.rowconfigure(1, weight=36)
        self.simulation_frame.rowconfigure(2, weight=2)
        self.simulation_frame.grid_propagate(0)
        
        # Simulation top subframe
        self.simulation_frame_top = ttk.Frame(self.simulation_frame)
        self.simulation_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.simulation_frame_top.columnconfigure(0, weight=1)
        self.simulation_frame_top.columnconfigure(1, weight=1)
        self.simulation_frame_top.columnconfigure(2, weight=5)
        self.simulation_frame_top.columnconfigure(3, weight=1)
        self.simulation_frame_top.columnconfigure(4, weight=1)
        self.simulation_frame_top.rowconfigure(0, weight=1)
        self.simulation_frame_top.grid_propagate(0)
        
        self.simulation_frame_top_name_label = ttk.Label(self.simulation_frame_top, text='Name:', anchor='center', justify='center')
        self.simulation_frame_top_name_label.grid(column=0, row=0, sticky=(N, S, W, E), pady=2)
        self.simulation_frame_top_name_label.grid_propagate(0)
        self.simulation_frame_top_name = ttk.Entry(self.simulation_frame_top, width=10)
        self.simulation_frame_top_name.grid(column=1, row=0, sticky=(N, S, W, E), padx=2, pady=2)
        self.simulation_frame_top_name.grid_propagate(0)
        self.simulation_frame_top_export = ttk.Button(self.simulation_frame_top, text='Export to files', command=self.export, style='primary.Outline.TButton')
        self.simulation_frame_top_export.grid(column=2, row=0, sticky=(N, W, S), padx=2, pady=2)
        self.simulation_frame_top_export.grid_propagate(0)
        self.simulation_frame_top_linear = ttk.Button(self.simulation_frame_top, text='Linear scale', style='primary.Outline.TButton')
        self.simulation_frame_top_linear.grid(column=3, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.simulation_frame_top_linear.bind('<Button-1>', lambda event, x=True: self.change_scale(x))
        self.simulation_frame_top_linear.grid_propagate(0)
        self.simulation_frame_top_dB = ttk.Button(self.simulation_frame_top, text='dB scale', style='primary.Outline.TButton')
        self.simulation_frame_top_dB.grid(column=4, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.simulation_frame_top_dB.bind('<Button-1>', lambda event, x=False: self.change_scale(x))
        self.simulation_frame_top_dB.grid_propagate(0)

        self.simulation_frame_middle = ttk.Frame(self.simulation_frame)
        self.simulation_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.simulation_frame_middle.columnconfigure(0, weight=1)
        self.simulation_frame_middle.rowconfigure(0, weight=1)
        self.simulation_frame_middle.grid_propagate(0)
        
        self.simulation_frame_bottom = ttk.Frame(self.simulation_frame) 
        self.simulation_frame_bottom.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        
        for i in range(len(self.notes) + 1):
            self.simulation_frame_bottom.columnconfigure(2 * i, weight=1)
            if i == len(self.notes):
                self.simulation_frame_bottom.columnconfigure(2 * i + 1, weight=2)
            else:
                self.simulation_frame_bottom.columnconfigure(2 * i + 1, weight=1)
        self.simulation_frame_bottom.rowconfigure(0, weight=1)
        self.simulation_frame_bottom.grid_propagate(0)
        
        self.simulation_frame_bottom_frames = list()
        for i in range(len(self.notes)):
            self.simulation_frame_bottom_label = ttk.Label(self.simulation_frame_bottom, text=f'{self.notes[i]}:', anchor='center', justify='center')
            self.simulation_frame_bottom_label.grid(column=2 * i + 1, row=0, sticky=(E, S, N), padx=2, pady=2)
            self.simulation_frame_bottom_frame= Frame(self.simulation_frame_bottom, width=24)
            self.simulation_frame_bottom_frame.grid(column=2 * i + 2, row=0, sticky=(W, E, S, N), pady=7)
            self.simulation_frame_bottom_frame.configure(bg='white', highlightbackground=self.colors[i], highlightthickness=1)
            self.simulation_frame_bottom_frame.bind('<Button-1>', lambda event, x=i: self.change_plot(x))
            self.simulation_frame_bottom_frame.bind('<Button-3>', lambda event, x=i: self.change_plot_single(x))
            self.simulation_frame_bottom_frames.append(self.simulation_frame_bottom_frame)
    
    def compute_impedance(self):
        error = False
        if self.parameter_frame_middle_main_notes.get() == 'all':
            self.simulation_notes = self.notes
            self.to_plot_notes = [True] * len(self.notes)
            self.enable_notes = [True] * len(self.notes)
        else:
            self.simulation_notes = [self.parameter_frame_middle_main_notes.get()]
            self.to_plot_notes = [False] * len(self.notes)
            self.enable_notes = [False] * len(self.notes)
            for i in range(len(self.notes)):
                if self.notes[i] == self.parameter_frame_middle_main_notes.get():
                    self.to_plot_notes[i] = True
                    self.enable_notes[i] = True
                    self.simulation_frame_bottom_frames[i].configure(background=self.colors[i])
                else:
                    self.simulation_frame_bottom_frames[i].configure(background='#FFFFFF')
        
        # Get simulation temperature
        if self.parameter_frame_middle_main_temperate.get() == '':
            self.mesagge.set('Temperature is empty')
            error = True
        else:
            if is_float(self.parameter_frame_middle_main_temperate.get()):
                self.temperature = float(self.parameter_frame_middle_main_temperate.get())
                if self.temperature < 0:
                    self.mesagge.set('Temperature is negative')
                    error = True
                elif self.temperature > 60:
                    self.mesagge.set('Temperature is higher than 60°C')
                    error = True
            else:
                self.mesagge.set('Temperature is not a number')
                error = True
        
        # Get simulation frecuency range
        if self.parameter_frame_middle_main_frecuency_from_entry.get() == '':
            self.mesagge.set('Start frecuency is empty')
            error = True
        else:
            if is_int(self.parameter_frame_middle_main_frecuency_from_entry.get()):
                self.from_frecuency = int(self.parameter_frame_middle_main_frecuency_from_entry.get())
                if self.from_frecuency < 0:
                    self.mesagge.set('Start frecuency is negative')
                    error = True
            else:
                self.mesagge.set('Start frecuency is not an integer')
                error = True
    
        if self.parameter_frame_middle_main_frecuency_to_entry.get() == '':
            self.mesagge.set('End frecuency is empty')
            error = True
        else:
            if is_int(self.parameter_frame_middle_main_frecuency_to_entry.get()):
                self.to_frecuency = int(self.parameter_frame_middle_main_frecuency_to_entry.get())
                if self.to_frecuency < 0:
                    self.mesagge.set('End frecuency is negative')
                    error = True
                elif self.to_frecuency <= self.from_frecuency:
                    self.mesagge.set('End frecuency is lower than start frecuency')
                    error = True
            else:
                self.mesagge.set('End frecuency is not an integer')
                error = True
        
        if self.parameter_frame_middle_main_frecuency_step_entry.get() == '':
            self.mesagge.set('Step frecuency is empty')
            error = True
        else:
            if is_int(self.parameter_frame_middle_main_frecuency_step_entry.get()):
                self.frecuency_step = int(self.parameter_frame_middle_main_frecuency_step_entry.get())
                if self.frecuency_step < 0:
                    self.mesagge.set('Step frecuency is negative')
                    error = True
                elif self.frecuency_step > self.to_frecuency - self.from_frecuency:
                    self.mesagge.set('Step frecuency is higher than the frecuency range')
                    error = True
            else:
                self.mesagge.set('Step frecuency is not an integer')
                error = True
        
        # Get embrouchure
        if self.parameter_frame_middle_main_embouchure.instate(['selected']):
            self.embrouchure = True
        else:
            self.embrouchure = False
            
        # Get concert pitch
        if self.parameter_frame_middle_concert_pitch.get() == '':
            self.mesagge.set('Concert pitch is empty')
            error = True
        else:
            if is_float(self.parameter_frame_middle_concert_pitch.get()):
                self.concert_pitch = float(self.parameter_frame_middle_concert_pitch.get())
                if self.concert_pitch < 0:
                    self.mesagge.set('Concert pitch is negative')
                    error = True
                if self.concert_pitch < 400 or self.concert_pitch > 500:
                    self.mesagge.set('Concert pitch is out of range (400-500 Hz)')
                    error = True
            else:
                self.mesagge.set('Concert pitch is not a number')
                error = True
                
        # Get transposition
        self.transposition = self.parameter_frame_middle_pitch_transposition.get()

        if not error:
            self.impedance_right_notebook.tab(0, state='normal')
            self.impedance_right_notebook.select(0)
            self.parameter_frame_top_clear.state(['!disabled'])
            self.compute()
            self.mesagge.set('Impedance computed!!!')
        
        for i in range(len(self.notes)):
            if self.to_plot_notes[i] == True:
                self.simulation_frame_bottom_frames[i].configure(background=self.colors[i])
            else:
                self.simulation_frame_bottom_frames[i].configure(background='#FFFFFF')
                
        self.parent.forget(3)
        self.parent.forget(2)

        self.new_resonance_frame = resonance(root=self.root, parent=self.parent, style=self.style, instrument=self.instrument, 
            res_f=self.res_f_all_fing, res_Q=self.res_Q_all_fing, res_Y=self.res_Y_all_fing,
            res_flow=self.flow_all_fing, res_pressure=self.pressure_all_fing, table_info=self.table_info, 
            simulation_notes=self.simulation_notes, notes=self.notes, position=self.position_info)

    def clear_parameters(self):
        self.parent.tab(2, state='disabled')
        self.parent.tab(3, state='disabled')
        self.impedance_right_notebook.tab(0, state='disabled')
        self.parameter_frame_middle_main_notes.current(0)
        self.parameter_frame_middle_main_temperate.delete(0, 'end')
        self.parameter_frame_middle_main_temperate.insert(0, '25')
        self.parameter_frame_middle_main_frecuency_from_entry.delete(0, 'end')
        self.parameter_frame_middle_main_frecuency_from_entry.insert(0, '20')
        self.parameter_frame_middle_main_frecuency_to_entry.delete(0, 'end')
        self.parameter_frame_middle_main_frecuency_to_entry.insert(0, '5000')
        self.parameter_frame_middle_main_frecuency_step_entry.delete(0, 'end')
        self.parameter_frame_middle_main_frecuency_step_entry.insert(0, '1')
        self.parameter_frame_middle_main_embouchure.state(['!selected'])
        self.parameter_frame_middle_concert_pitch.delete(0, 'end')
        self.parameter_frame_middle_concert_pitch.insert(0, '440')
        self.parameter_frame_middle_pitch_transposition.current(0)
        self.parameter_frame_middle_advanced_opcion_1.current(0)
        self.parameter_frame_middle_advanced_opcion_2.current(0)
        self.parameter_frame_middle_advanced_opcion_3.state(['!selected'])
        
    def dummy(self):
        pass

    def compute(self):
        """
        Currently it is necessary to compute the impedance of the "body" and the "window"/"embouchure"
        impedance separately then sum them to have the global admittance.
        """
        recompute = False
        self.instrument = InstrumentGeometry(self.bore_sections, self.holes, self.finger_chart, unit=self.unit, diameter=self.diameter)
        freq = np.arange(self.from_frecuency, self.to_frecuency, self.frecuency_step)

        # for the body the impedance is classic, here I used detailed implementation because I need
        # some elements for the window impedance
        body_physics = InstrumentPhysics(self.instrument, temperature=self.temperature, player=Player(), losses=True) # Player is unused but it is necessary
        body_imp = FrequentialSolver(body_physics, freq)

        # for the window impedance it is necessary to compute the impedance separatly with his
        # own expression or one already implemented, here for infinite flanged pipe
        window_rad = radiation_model('infinite_flanged', 'window_radiation', body_physics.scaling, body_physics.convention) # the two last options are not really used, but they are needed...

        rho, celerity = body_physics.get_entry_coefs('rho', 'c')
        radius = 0
        if self.unit == 'mm':
            if self.diameter:
                radius = 1e-3 * float(self.bore_sections[0][2])/2
            else:
                radius = 1e-3 * float(self.bore_sections[0][2])
        else:
            if self.diameter:
                radius = float(self.bore_sections[0][2])/2
            else:
                radius = float(self.bore_sections[0][2])

        omega = 2*np.pi*freq
        Zw = window_rad.get_impedance(omega, radius, rho, celerity, opening_factor=1) # opening_factor=1 => hole fully open
        Zc_w = rho*celerity/(np.pi*radius**2) # the caracteristic impedance of the window/embouchure

        # now a loop for all fingerings
        self.Y_all_fing = {} # to store everything
        self.res_f_all_fing = {}
        self.res_Q_all_fing = {}
        self.res_Y_all_fing = {}
        self.flow_all_fing = {}
        self.pressure_all_fing = {}
        self.table_info = {}
        self.position_info = {}
        simu_reverse = self.simulation_notes[::-1]
        for note in simu_reverse:
            body_imp.set_note(note)
            body_imp.solve(interp=True, interp_grad=True)
            self.position_info.update({note: body_imp.x_interp})
            Zp = body_imp.impedance
            if self.embrouchure:
                Yt = Zc_w /(Zp + Zw)
            else:
                Yt = Zc_w / Zp
            f_res, Q_res, Y_res = resonance_peaks_from_phase(freq, Yt, display_warning=False, k=5)
            if len(f_res) < 5:
                recompute = True
                break
            else:
                self.res_f_all_fing.update({note: f_res})
                self.res_Q_all_fing.update({note: Q_res})
                self.res_Y_all_fing.update({note: Y_res})
                self.Y_all_fing.update({note: Yt})
                self.table_info.update({note: match_freqs_with_notes(f_=f_res, concert_pitch_A=self.concert_pitch, transposition=self.transposition)})

        if not recompute:
            for note in self.simulation_notes:
                flow, pressure = body_imp.get_flow_pressure_several_notes(notes=[note], f_interest=[self.res_f_all_fing[note]])
                normalized_flow = []
                normalized_pressure = []
                for fl in flow:
                    fl_new = []
                    for f in fl:
                        f = np.abs(np.real(f))
                        f_max = np.max(f)
                        f = (f/f_max) * 100
                        fl_new.append(f)
                    normalized_flow.append(np.array(fl_new))
                for pr in pressure:
                    pr_new = []
                    for p in pr:
                        p = np.abs(np.real(p))
                        p_max = np.max(p)
                        p = (p/p_max) * 100
                        pr_new.append(p)
                    normalized_pressure.append(np.array(pr_new))
                self.flow_all_fing.update({note: np.array(normalized_flow)})
                self.pressure_all_fing.update({note: np.array(normalized_pressure)})
            
            self.plot()
        else:
            self.mesagge.set('Not enough resonance peaks found, recomputing with higher frequency range...')
            self.to_frecuency += 1000
            self.compute()
    
    def plot(self):
        plt.close()
        self.geometry_figure = plt.figure(figsize=(1, 1), dpi=100)
        position = [0, 0, 0.5, 1]
        gs = gridspec.GridSpec(1, 1)
        gs.tight_layout(self.geometry_figure, rect=position)
        freq = np.arange(self.from_frecuency, self.to_frecuency, self.frecuency_step)
        if self.parameter_frame_middle_main_notes.get() == 'all':
            for i, note in enumerate(self.simulation_notes):
                if self.to_plot_notes[i] == True:
                    if self.linear_scale:
                        plt.plot(freq, np.abs(self.Y_all_fing[note]), label='Fingering: ' + note, color=self.colors[i])
                        plt.plot(self.res_f_all_fing[note], np.abs(self.res_Y_all_fing[note]), 'o', color=self.colors[i])
                    else:
                        plt.plot(freq, 20*np.log10(np.abs(self.Y_all_fing[note])), label='Fingering: ' + note, color=self.colors[i])
                        plt.plot(self.res_f_all_fing[note], 20*np.log10(np.abs(self.res_Y_all_fing[note])), 'o', color=self.colors[i])
        else:
            for i in range(len(self.notes)):
                if self.notes[i] == self.simulation_notes[0]:
                    color = self.colors[i]
                    if self.linear_scale:
                        if self.to_plot_notes[i] == True:
                            plt.plot(freq, np.abs(self.Y_all_fing[self.simulation_notes[0]]), label='Fingering: ' + self.simulation_notes[0], color=color)
                            plt.plot(self.res_f_all_fing[self.simulation_notes[0]], np.abs(self.res_Y_all_fing[self.simulation_notes[0]]), 'o', color=color)
                    else:
                        if self.to_plot_notes[i] == True:
                            plt.plot(freq, 20*np.log10(np.abs(self.Y_all_fing[self.simulation_notes[0]])), label='Fingering: ' + self.simulation_notes[0], color=color)
                            plt.plot(self.res_f_all_fing[self.simulation_notes[0]], 20*np.log10(np.abs(self.res_Y_all_fing[self.simulation_notes[0]])), 'o', color=color)
                    break
        
        # ax = self.geometry_figure.get_axes()
        # for i, lines in enumerate(ax[0].lines):
        #     lines.set_color(self.colors[i])
            
        if self.linear_scale:
            plt.title('Linear scale instrument admittance')
            plt.ylabel('|Y|/Yc [Linear]')
        else:
            plt.title('dB scale instrument admittance')
            plt.ylabel('|Y|/Yc [dB]')
        plt.xlabel('Frequency [Hz]')
        
        plt.grid()
        
        # Create canvas with figure
        canvas = FigureCanvasTkAgg(self.geometry_figure, self.simulation_frame_middle)
        canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, W, E, S), pady=10)
        
    def change_scale(self, x):
        if self.linear_scale != x:
            self.linear_scale = x
            self.plot()
            
    def change_plot(self, x):
        if self.enable_notes[x] == True:
            if self.to_plot_notes[x] == True:
                self.to_plot_notes[x] = False
                self.simulation_frame_bottom_frames[x].configure(background='#FFFFFF')
            else:
                self.to_plot_notes[x] = True
                self.simulation_frame_bottom_frames[x].configure(background=self.colors[x])
            self.plot()
        
    def change_plot_single(self, x):
        if self.enable_notes[x] == True:
            self.to_plot_notes = [False] * len(self.notes)
            self.to_plot_notes[x] = True
            
            for i in range(len(self.notes)):
                if self.to_plot_notes[i] == True:
                    self.simulation_frame_bottom_frames[i].configure(background=self.colors[i])
                else:
                    self.simulation_frame_bottom_frames[i].configure(background='#FFFFFF')
                    
            self.plot()

    def export(self):
        name = self.simulation_frame_top_name.get()
        if name != '':
            freq = np.arange(self.from_frecuency, self.to_frecuency, self.frecuency_step)
            # Create files with instrument data
            path = dirname(abspath(__file__))
            folder_path = join(path, f'{name}_impedances')
            if exists(folder_path):
                try:
                    rmtree(folder_path)
                except Exception as e:
                    print(f"Error deleting '{folder_path}': {e}")
            makedirs(folder_path)
            # print(f"Folder '{name}_impedances' created successfully at '{folder_path}'")
            
            if self.parameter_frame_middle_main_notes.get() == 'all':
                for i, note in enumerate(self.simulation_notes):
                    if self.to_plot_notes[i] == True:
                        with open(join(folder_path, f'{name}_{note}_linear_impedance.txt'), 'w') as file:
                            for j in range(len(freq)):
                                file.write(f'{freq[j]} {np.real(self.Y_all_fing[note][j])} {np.imag(self.Y_all_fing[note][j])}\n')
            else:
                with open(join(folder_path, f'{name}_{self.simulation_notes[0]}_linear_impedance.txt'), 'w') as file:
                            for j in range(len(freq)):
                                file.write(f'{freq[j]} {np.real(self.Y_all_fing[self.simulation_notes[0]][j])} {np.imag(self.Y_all_fing[self.simulation_notes[0]][j])}\n')
            
            self.mesagge.set('Files exported successfully')
        else:
            self.mesagge.set('Please enter a name for the folder')
    
    def print_computing(self):
        self.mesagge.set('Computing...')
        self.compute_impedance()
            
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
# Tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ttkbootstrap.scrolled import ScrolledFrame

# File management
from shutil import rmtree
from os import makedirs
from os.path import basename, abspath, exists, join, dirname

# Matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import get_backend
import matplotlib.gridspec as gridspec

# NumPy
import numpy as np

# Openwind
from openwind import InstrumentGeometry

# Parameters
from parameters import *

# Impedance class
from impedance import impedance

import random

class instrument():
    def __init__(self, root, parent, style):
        ################################ Variables ################################
        
        self.root = root

        self.style = style
        self.style.configure('primary.Outline.TButton', borderwidth=1)
        self.style.map('primary.Outline.TButton', focuscolor=[('pressed', 'white'), ('active !disabled', 'black'), ('!pressed', 'white')])
        self.style.configure('TCombobox', borderwidth=1, borderwith=0)
        
        # To modify main notebook
        self.instrument_parent = parent
        
        # Variables for labels
        self.instruction = StringVar()
        self.instruction.set('Please load geometry')
        self.mesagge = StringVar()
        self.mesagge.set('Welcome to Pipe Tool')
        
        # Pallette with 60 colors for plot lines
        self.colors = [
            '#4B0082', '#DDA0DD', '#D8BFD8', '#9370DB', '#7FFF00', '#808000',
            '#00FF7F', '#FF1493', '#6495ED', '#C71585', '#9400D3', '#FFA07A',
            '#FF00FF', '#FF0000', '#FF4500', '#00FFFF', '#800080', '#FFD700',
            '#EE82EE', '#4682B4', '#FFB6C1', '#008000', '#FF4500', '#000080',
            '#FF69B4', '#008080', '#8B008B', '#B0E0E6', '#FFFF00', '#FF7F50',
            '#FF0000', '#00CED1', '#D8BFD8', '#FF4500', '#FFA500', '#BA55D3',
            '#800000', '#8A2BE2', '#FF6347', '#9932CC', '#FFC0CB', '#FF6347',
            '#0000FF', '#DC143C', '#FF00FF', '#FFC0CB', '#800080', '#E6E6FA',
            '#DB7093', '#ADFF2F', '#808080', '#FA8072', '#87CEEB', '#DC143C', 
            '#FF69B4', '#FF0000', '#FFA07A', '#C0C0C0', '#00FF00', '#FF7F50']
        
        # Variables to store files
        self.bore_sections = None
        self.holes = None
        self.finger_chart = None
        self.holes_label = ['label', 'position', 'length', 'radius', 'radius_out']
        self.top_view = True
        self.notes_available = False
        self.ready = False
        
        # Variables to store instrumentGeometry object
        self.instrument = None
        
        # Intrument parameters
        self.unit = 'mm'
        self.diameter = False
        
        ################################ Widgets ################################
        
        self.create_widgets(parent)
        self.geometry_widget()
        
        # self.holes_widget()
        # self.finger_chart_widget()
        # self.view_widget()
        
    def create_widgets(self, parent):
        # Instrument main frame
        self.instrument_frame = ttk.Frame(parent)
        self.instrument_frame.columnconfigure(0, weight=1)
        self.instrument_frame.columnconfigure(1, weight=1)
        self.instrument_frame.rowconfigure(0, weight=1)
        self.instrument_frame.grid_propagate(0)
        
        # Instrumenr left frame
        self.instrument_left_frame = ttk.Frame(self.instrument_frame)
        self.instrument_left_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.instrument_left_frame.columnconfigure(0, weight=1)
        self.instrument_left_frame.rowconfigure(0, weight=1)
        self.instrument_left_frame.grid_propagate(0)
        
        # Instrument right frame
        self.instrument_right_frame = ttk.Frame(self.instrument_frame)
        self.instrument_right_frame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.instrument_right_frame.columnconfigure(0, weight=1)
        self.instrument_right_frame.rowconfigure(0, weight=1)
        self.instrument_right_frame.grid_propagate(0)
        
        # Instrument left notebook
        self.instrument_left_notebook = ttk.Notebook(self.instrument_left_frame)
        self.instrument_left_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.instrument_left_notebook.columnconfigure(0, weight=1)
        self.instrument_left_notebook.rowconfigure(0, weight=1)
        self.instrument_left_notebook.grid_propagate(0)
        
        # Instrument right notebook
        self.instrument_right_notebook = ttk.Notebook(self.instrument_right_frame)
        self.instrument_right_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.instrument_right_notebook.columnconfigure(0, weight=1)
        self.instrument_right_notebook.rowconfigure(0, weight=1)
        self.instrument_right_notebook.grid_propagate(0)
        
        # Geometry frame
        self.geometry_frame = ttk.Frame(self.instrument_left_notebook)
        self.instrument_left_notebook.add(self.geometry_frame, text='Geometry')
        self.geometry_frame.columnconfigure(0, weight=1)
        self.geometry_frame.rowconfigure(0, weight=3)
        self.geometry_frame.rowconfigure(1, weight=36)
        self.geometry_frame.rowconfigure(2, weight=2)
        self.geometry_frame.grid_propagate(0)
        
        # Holes frame
        self.holes_frame = ttk.Frame(self.instrument_left_notebook)
        self.instrument_left_notebook.add(self.holes_frame, text='Holes')
        self.instrument_left_notebook.tab(1, state='disabled')
        self.holes_frame.columnconfigure(0, weight=1)
        self.holes_frame.rowconfigure(0, weight=2)
        self.holes_frame.rowconfigure(1, weight=36)
        self.holes_frame.rowconfigure(2, weight=2)
        self.holes_frame.grid_propagate(0)
        
        # Finger chart frame
        self.finger_chart_frame = ttk.Frame(self.instrument_left_notebook)
        self.instrument_left_notebook.add(self.finger_chart_frame, text='Finger Chart')
        self.instrument_left_notebook.tab(2, state='disabled')
        self.finger_chart_frame.columnconfigure(0, weight=1)
        self.finger_chart_frame.rowconfigure(0, weight=2)
        self.finger_chart_frame.rowconfigure(1, weight=36)
        self.finger_chart_frame.rowconfigure(2, weight=2)
        self.finger_chart_frame.grid_propagate(0)
        
        # View frame
        self.view_frame = ttk.Frame(self.instrument_right_notebook)
        self.instrument_right_notebook.add(self.view_frame, text='Instrument')
        self.instrument_right_notebook.tab(0, state='disabled')
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.rowconfigure(0, weight=2)
        self.view_frame.rowconfigure(1, weight=38)
        self.view_frame.grid_propagate(0)

    def geometry_widget(self):
        # Geometry top subframe
        self.geometry_frame_top = ttk.Frame(self.geometry_frame)
        self.geometry_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.geometry_frame_top.columnconfigure(0, weight=1)
        self.geometry_frame_top.columnconfigure(1, weight=1)
        self.geometry_frame_top.columnconfigure(2, weight=1)
        self.geometry_frame_top.columnconfigure(3, weight=1)
        self.geometry_frame_top.columnconfigure(4, weight=1)
        self.geometry_frame_top.columnconfigure(5, weight=1)
        self.geometry_frame_top.columnconfigure(6, weight=1)
        self.geometry_frame_top.rowconfigure(0, weight=1)
        self.geometry_frame_top.grid_propagate(0)
        
        self.geometry_frame_top_unit_label = ttk.Label(self.geometry_frame_top, text='Unit:', anchor='center', justify='center')
        self.geometry_frame_top_unit_label.grid(column=0, row=0, sticky=(N, S, E, W), padx=2, pady=2)
        self.geometry_frame_top_unit = ttk.Combobox(self.geometry_frame_top, values=['m', 'mm'], width=4)
        self.geometry_frame_top_unit.grid(column=1, row=0, sticky=(N, S, W), padx=2, pady=2)
        self.geometry_frame_top_unit.bind('<<ComboboxSelected>>', lambda event, x='': self.change_unit(x))
        self.geometry_frame_top_radius_label = ttk.Label(self.geometry_frame_top, text='Reference:', anchor='center', justify='center')
        self.geometry_frame_top_radius_label.grid(column=2, row=0, sticky=(N, S, E, W), padx=2, pady=2)
        self.geometry_frame_top_radius = ttk.Combobox(self.geometry_frame_top, values=['radius', 'diamater'], width=8)
        self.geometry_frame_top_radius.grid(column=3, row=0, sticky=(N, S, W), padx=2, pady=2) 
        self.geometry_frame_top_radius.bind('<<ComboboxSelected>>', lambda event, x='': self.change_radius(x))
        self.geometry_frame_top_save = ttk.Button(self.geometry_frame_top, text='Save Geometry', command=self.save_geometry, style='primary.Outline.TButton')
        self.geometry_frame_top_save.grid(column=4, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.geometry_frame_top_clear = ttk.Button(self.geometry_frame_top, text='Clear Geometry', command=self.clear_geometry, style='primary.Outline.TButton')
        self.geometry_frame_top_clear.grid(column=5, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.geometry_frame_top_load = ttk.Button(self.geometry_frame_top, text='Load Geometry', command=self.load_geometry, style='primary.Outline.TButton')
        self.geometry_frame_top_load.grid(column=6, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.geometry_frame_top_clear.state(['disabled'])
        self.geometry_frame_top_unit.insert(0, 'mm')
        self.geometry_frame_top_unit.config(state='readonly')
        self.geometry_frame_top_radius.insert(0, 'radius')
        self.geometry_frame_top_radius.config(state='readonly')
        
        # Geometry middle subframe
        self.geometry_frame_middle = ScrolledFrame(self.geometry_frame)
        self.geometry_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        for i in range(7):
            self.geometry_frame_middle.columnconfigure(i, weight=1)
        for i in range(MAX_INSTRUMENT_SECTIONS + 1): # plus 1 for the labels
            if i == 0:
                self.geometry_frame_middle.rowconfigure(i, weight=1)
            else:
                self.geometry_frame_middle.rowconfigure(i, weight=5)
        self.geometry_frame_middle.grid_propagate(0)
        
        self.radius_start = StringVar()
        self.radius_start.set('Start\nRadius')
        self.radius_end = StringVar()
        self.radius_end.set('End\n_adius')
        
        self.geometry_frame_middle_labels = list()
        for i in range(len(GEOMETRY_LABELS)):
            label = ttk.Label(self.geometry_frame_middle, text=GEOMETRY_LABELS[i], anchor='center', justify='center')
            label.grid(column=i, row=0, sticky=(N, W, E, S), padx=2, pady=5)
            self.geometry_frame_middle_labels.append(label)
        
        self.geometry_frame_middle_entries = list()
        self.geometry_frame_middle_disabled = list()
        for i in range(1, MAX_INSTRUMENT_SECTIONS + 1): # from 1 because of the labels
            self.geometry_frame_middle_disabled.append(False)
            entries_row = list()
            for j in range(len(GEOMETRY_LABELS)):
                if j == 4:
                    entry = ttk.Combobox(self.geometry_frame_middle, width=2,
                        values=SECTION_TYPES)
                    entry.grid(column=j, row=i, sticky=(W, E), padx=10)
                    entry.grid_propagate(0)
                    entry.config(state='readonly')
                    entry.config(state='disabled')
                    entry.bind('<<ComboboxSelected>>', lambda event, x=(i, j): self.enable_geometry_parameter(x))
                    entries_row.append(entry)
                elif GEOMETRY_LABELS[j] == 'Enable\nSection':
                    entry = Frame(self.geometry_frame_middle)
                    entry.grid(column=j, row=i, sticky=(N, S, W, E), padx=10, pady=5)
                    entry.columnconfigure(0, weight=1)
                    entry.rowconfigure(0, weight=1)
                    entry.config(bg='#ffffff', highlightbackground=self.colors[i - 1], highlightthickness=1)
                    entry.bind('<Button-1>', lambda event, x=i: self.enable_geometry_row(x))
                    entries_row.append(entry)
                else:
                    entry = ttk.Entry(self.geometry_frame_middle, width=3)
                    entry.grid(column=j, row=i, sticky=(W, E), padx=10)
                    entry.config(state='disabled')
                    entries_row.append(entry)
            self.geometry_frame_middle_entries.append(entries_row)
        
        # Geometry bottom subframe
        self.geometry_frame_bottom = ttk.Frame(self.geometry_frame) 
        self.geometry_frame_bottom.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        self.geometry_frame_bottom.columnconfigure(0, weight=1)
        self.geometry_frame_bottom.rowconfigure(0, weight=1)
        self.geometry_frame_bottom.grid_propagate(0)
        
        self.geometry_frame_bottom_label = ttk.Label(self.geometry_frame_bottom, textvariable=self.mesagge, anchor='center', justify='center')
        self.geometry_frame_bottom_label.grid(column=0, row=0, sticky=(W, E, S, N)) 
        
    def holes_widget(self):
        # Holes top subframe
        self.holes_frame_top = ttk.Frame(self.holes_frame)
        self.holes_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.holes_frame_top.columnconfigure(0, weight=1)
        self.holes_frame_top.columnconfigure(1, weight=1)
        self.holes_frame_top.columnconfigure(2, weight=1)
        self.holes_frame_top.columnconfigure(3, weight=1)
        self.holes_frame_top.columnconfigure(4, weight=1)
        self.holes_frame_top.columnconfigure(5, weight=1)
        self.holes_frame_top.columnconfigure(6, weight=1)
        self.holes_frame_top.rowconfigure(0, weight=1)
        self.holes_frame_top.grid_propagate(0)
        
        self.holes_frame_top_unit_label = ttk.Label(self.holes_frame_top, text='Unit:', anchor='center', justify='center')
        self.holes_frame_top_unit_label.grid(column=0, row=0, sticky=(N, S, E, W), padx=2, pady=2)
        self.holes_frame_top_unit = ttk.Label(self.holes_frame_top, text=f'{self.unit}', width=10)
        self.holes_frame_top_unit.grid(column=1, row=0, sticky=(N, S, W), padx=2, pady=2)
        self.holes_frame_top_radius_label = ttk.Label(self.holes_frame_top, text='Reference:', anchor='center', justify='center')
        self.holes_frame_top_radius_label.grid(column=2, row=0, sticky=(N, S, E, W), padx=2, pady=2)
        self.holes_frame_top_radius = ttk.Label(self.holes_frame_top, text='Radius', width=10)
        self.holes_frame_top_radius.grid(column=3, row=0, sticky=(N, S, W), padx=2, pady=2) 
        self.holes_frame_top_save = ttk.Button(self.holes_frame_top, text='Save Holes', command=self.save_holes, style='primary.Outline.TButton')
        self.holes_frame_top_save.grid(column=4, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.holes_frame_top_clear = ttk.Button(self.holes_frame_top, text='Clear Holes', command=self.clear_holes, style='primary.Outline.TButton')
        self.holes_frame_top_clear.grid(column=5, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.holes_frame_top_load = ttk.Button(self.holes_frame_top, text='Load Holes', command=self.load_holes, style='primary.Outline.TButton')
        self.holes_frame_top_load.grid(column=6, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.holes_frame_top_clear.state(['disabled'])

        # Holes middle subframe
        self.holes_frame_middle = ttk.Frame(self.holes_frame)
        self.holes_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        for i in range(6):
            self.holes_frame_middle.columnconfigure(i, weight=1)
        for i in range(MAX_INSTRUMENT_HOLES + 1): # plus 1 for the labels
            if i == 0:
                self.holes_frame_middle.rowconfigure(i, weight=1)
            else:
                self.holes_frame_middle.rowconfigure(i, weight=5)
        self.holes_frame_middle.grid_propagate(0)
        
        self.holes_frame_middle_labels = list()
        for i in range(len(HOLES_LABELS_RADIUS)):
            if self.diameter:
                label = ttk.Label(self.holes_frame_middle, text=HOLES_LABELS_DIAMETER[i], anchor='center', justify='center')
            else:
                label = ttk.Label(self.holes_frame_middle, text=HOLES_LABELS_RADIUS[i], anchor='center', justify='center')
            label.grid(column=i, row=0, sticky=(N, W, E, S), padx=2, pady=5)
            self.holes_frame_middle_labels.append(label)
        
        self.holes_frame_middle_entries = list()
        self.holes_frame_middle_disabled = list()
        for i in range(1, MAX_INSTRUMENT_HOLES + 1): # from 1 because of the labels
            self.holes_frame_middle_disabled.append(False)
            entries_row = list()
            for j in range(len(HOLES_LABELS_RADIUS)):
                if HOLES_LABELS_RADIUS[j] == 'Enable\nHole':
                    entry = Frame(self.holes_frame_middle)
                    entry.grid(column=j, row=i, sticky=(N, S, W, E), padx=10, pady=15)
                    entry.columnconfigure(0, weight=1)
                    entry.rowconfigure(0, weight=1)
                    entry.config(bg='#ffffff', highlightbackground=self.colors[i - 1], highlightthickness=1)
                    entry.bind('<Button-1>', lambda event, x=i: self.enable_holes_row(x))
                    entries_row.append(entry)
                else:
                    entry = ttk.Entry(self.holes_frame_middle, width=3)
                    entry.grid(column=j, row=i, sticky=(W, E), padx=10)
                    entry.config(state='disabled')
                    entries_row.append(entry)
            self.holes_frame_middle_entries.append(entries_row)
        
        if self.diameter:
            self.holes_frame_top_radius.config(text='Diameter')
            self.holes_frame_middle_labels[3].config(text='Diameter\nin')
            self.holes_frame_middle_labels[4].config(text='Diameter\nout')
        else:
            self.holes_frame_top_radius.config(text='Radius')
            self.holes_frame_middle_labels[3].config(text='Radius\nin')
            self.holes_frame_middle_labels[4].config(text='Radius\nout')
        
        if self.unit == "mm":
            self.holes_frame_top_unit.config(text='mm')
        else:
            self.holes_frame_top_unit.config(text='m')
        
        # Holes bottom subframe
        self.holes_frame_bottom = ttk.Frame(self.holes_frame) 
        self.holes_frame_bottom.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        self.holes_frame_bottom.columnconfigure(0, weight=1)
        self.holes_frame_bottom.rowconfigure(0, weight=1)
        self.holes_frame_bottom.grid_propagate(0)
        
        self.holes_frame_bottom_label = ttk.Label(self.holes_frame_bottom, textvariable=self.mesagge, anchor='center', justify='center')
        self.holes_frame_bottom_label.grid(column=0, row=0, sticky=(W, E, S, N)) 

    def finger_chart_widget(self):
        # Finger chart top subframe
        self.finger_chart_frame_top = ttk.Frame(self.finger_chart_frame)
        self.finger_chart_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.finger_chart_frame_top.columnconfigure(0, weight=1)
        self.finger_chart_frame_top.columnconfigure(1, weight=1)
        self.finger_chart_frame_top.columnconfigure(2, weight=1)
        self.finger_chart_frame_top.columnconfigure(3, weight=1)
        self.finger_chart_frame_top.columnconfigure(4, weight=1)
        self.finger_chart_frame_top.columnconfigure(5, weight=1)
        self.finger_chart_frame_top.columnconfigure(6, weight=1)
        self.finger_chart_frame_top.rowconfigure(0, weight=1)
        self.finger_chart_frame_top.grid_propagate(0)
        
        # Finger chart top subframe
        self.finger_chart_frame_top_unit_label = ttk.Label(self.finger_chart_frame_top, text='Unit:', anchor='center', justify='center')
        self.finger_chart_frame_top_unit_label.grid(column=0, row=0, sticky=(N, S, E, W), padx=2, pady=2)
        self.finger_chart_frame_top_unit = ttk.Label(self.finger_chart_frame_top, text=f'{self.unit}', width=10, anchor='center', justify='center')
        self.finger_chart_frame_top_unit.grid(column=1, row=0, sticky=(N, S, W), padx=2, pady=2)
        self.finger_chart_frame_top_radius_label = ttk.Label(self.finger_chart_frame_top, text='Reference:', anchor='center', justify='center')
        self.finger_chart_frame_top_radius_label.grid(column=2, row=0, sticky=(N, S, E, W), padx=2, pady=2)
        self.finger_chart_frame_top_radius = ttk.Label(self.finger_chart_frame_top, text='Radius', width=10, anchor='center', justify='center')
        self.finger_chart_frame_top_radius.grid(column=3, row=0, sticky=(N, S, W), padx=2, pady=2) 
        self.finger_chart_frame_top_save = ttk.Button(self.finger_chart_frame_top, text='Save Chart', command=self.save_finger_chart, style='primary.Outline.TButton')
        self.finger_chart_frame_top_save.grid(column=4, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.finger_chart_frame_top_clear = ttk.Button(self.finger_chart_frame_top, text='Clear Chart', command=self.clear_finger_chart, style='primary.Outline.TButton')
        self.finger_chart_frame_top_clear.grid(column=5, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.finger_chart_frame_top_load = ttk.Button(self.finger_chart_frame_top, text='Load Chart', command=self.load_finger_chart, style='primary.Outline.TButton')
        self.finger_chart_frame_top_load.grid(column=6, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.finger_chart_frame_top_clear.state(['disabled'])
        
        # Finger chart middle subframe
        self.finger_chart_frame_middle = ttk.Frame(self.finger_chart_frame)
        self.finger_chart_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.finger_chart_frame_middle.grid_propagate(0)
        for i in range(MAX_INSTRUMENT_NOTES + 2):
            if i == 0:
                self.finger_chart_frame_middle.rowconfigure(i, weight=1)
            else:
                self.finger_chart_frame_middle.rowconfigure(i, weight=2)
                    
        self.finger_chart_frame_middle_entries = list()
        self.finger_chart_frame_middle_disabled = [False] * (MAX_INSTRUMENT_NOTES + 1)
        for i in range(MAX_INSTRUMENT_NOTES + 1): #  + label 
            entries_row = list()
            for j in range(MAX_INSTRUMENT_HOLES + 2): #  + label and enabled
                if i == 0:
                    if j == 0:
                        entry = ttk.Label(self.finger_chart_frame_middle, text='N \ H', anchor='center', justify='center')
                        entry.grid(column=j, row=i, sticky=(N, S, W, E), padx=2, pady=2)
                        entries_row.append(entry)
                    elif j == MAX_INSTRUMENT_HOLES + 1:
                        entry = ttk.Label(self.finger_chart_frame_middle, text='Enabled', anchor='center', justify='center')
                        entry.grid(column=j, row=i, sticky=(N, S, W, E), padx=2, pady=2)
                        entries_row.append(entry)
                    else:
                        entry = ttk.Label(self.finger_chart_frame_middle, text='', anchor='center', justify='center')
                        entry.grid(column=j, row=i, sticky=(N, S, W, E), padx=2, pady=2)
                        entries_row.append(entry)
                else:
                    if j == 0:
                        entry = ttk.Entry(self.finger_chart_frame_middle, width=3)
                        entry.grid(column=j, row=i, sticky=(W, E), padx=2, pady=2)
                        entries_row.append(entry)
                    elif j == MAX_INSTRUMENT_HOLES + 1:
                        entry = Frame(self.finger_chart_frame_middle)
                        entry.grid(column=j, row=i, sticky=(N, S, W, E), padx=10, pady=15)
                        entry.columnconfigure(0, weight=1)
                        entry.rowconfigure(0, weight=1)
                        entry.config(bg='white', highlightbackground=self.colors[i - 1], highlightthickness=1)
                        entry.bind('<Button-1>', lambda event, x=i: self.enable_finger_chart_row(x))
                        entries_row.append(entry)  
                    else:
                        entry = ttk.Combobox(self.finger_chart_frame_middle, width=1,
                            values=['○', '●']) # TODO: implement ◐??
                        entry.grid(row=i, column=j, sticky=(W, E), padx=5)
                        entry.insert(0, '○')
                        entry.config(state='readonly')
                        entries_row.append(entry)
            self.finger_chart_frame_middle_entries.append(entries_row)
            
        # Finger chart bottom subframe
        self.finger_chart_frame_bottom = ttk.Frame(self.finger_chart_frame) 
        self.finger_chart_frame_bottom.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        self.finger_chart_frame_bottom.columnconfigure(0, weight=1)
        self.finger_chart_frame_bottom.rowconfigure(0, weight=1)
        self.finger_chart_frame_bottom.grid_propagate(0)
        
        self.finger_chart_frame_bottom_label = ttk.Label(self.finger_chart_frame_bottom, textvariable=self.mesagge, anchor='center', justify='center')
        self.finger_chart_frame_bottom_label.grid(column=0, row=0, sticky=(W, E, S, N)) 
        
    def view_widget(self):        
        # View top subframe
        self.view_frame_top = ttk.Frame(self.view_frame)
        self.view_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.view_frame_top.columnconfigure(0, weight=1)
        self.view_frame_top.columnconfigure(1, weight=1)
        self.view_frame_top.columnconfigure(2, weight=5)
        self.view_frame_top.columnconfigure(3, weight=1)
        self.view_frame_top.columnconfigure(4, weight=1)
        self.view_frame_top.columnconfigure(5, weight=1)
        self.view_frame_top.columnconfigure(6, weight=1)
        self.view_frame_top.columnconfigure(7, weight=1)
        self.view_frame_top.rowconfigure(0, weight=1)
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
        self.view_frame_top_notes_label = ttk.Label(self.view_frame_top, text='Notes:', anchor='center', justify='center')
        self.view_frame_top_notes_label.grid(column=3, row=0, sticky=(N, S, W, E), pady=2)
        self.view_frame_top_notes_label.grid_propagate(0)
        self.view_frame_top_notes = ttk.Combobox(self.view_frame_top, width=10, values=[''])
        self.view_frame_top_notes.grid(column=4, row=0, sticky=(N, S, W, E), padx=2, pady=2)
        self.view_frame_top_notes.grid_propagate(0)
        self.view_frame_top_topview = ttk.Button(self.view_frame_top, text='Top view', style='primary.Outline.TButton')
        self.view_frame_top_topview.grid(column=5, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top_topview.bind('<Button-1>', lambda event, x=True: self.change_view(x))
        self.view_frame_top_topview.grid_propagate(0)
        self.view_frame_top_sideview = ttk.Button(self.view_frame_top, text='Side view', style='primary.Outline.TButton')
        self.view_frame_top_sideview.grid(column=6, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top_sideview.bind('<Button-1>', lambda event, x=False: self.change_view(x))
        self.view_frame_top_sideview.grid_propagate(0)
        self.view_frame_top_pop = ttk.Button(self.view_frame_top, text='Pop', style='primary.Outline.TButton')
        self.view_frame_top_pop.grid(column=7, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top_pop.bind('<Button-1>', lambda event, x=False: self.pop(x))
        self.view_frame_top_pop.grid_propagate(0)
        self.view_frame_top_notes.state(['disabled'])
        self.view_frame_top_topview.state(['disabled'])
        self.view_frame_top_sideview.state(['disabled'])
        self.view_frame_top_pop.state(['disabled'])
        
        # View middle subframe
        self.view_frame_middle = ttk.Frame(self.view_frame)
        self.view_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_middle.columnconfigure(0, weight=1)
        self.view_frame_middle.rowconfigure(0, weight=1)
        self.view_frame_middle.grid_propagate(0)
    
    def load_geometry(self):
        # Select file by user
        file = filedialog.askopenfilename(title='Select a file for the main Bore')
        
        # Check if selected file is a valid .txt or .csv file
        if file:
            if file.split('.')[-1] != 'txt' and file.split('.')[-1] != 'csv':
                self.instruction.set('Please load valid file')
            else:
                try:
                    with open(file, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if 'spline' in line.lower():
                                raise Exception('Spline sections are not supported')
                        
                    self.instrument = InstrumentGeometry(main_bore=file, unit=self.unit, diameter=self.diameter)
                    bore = self.instrument.get_bore_list(unit=self.unit, diameter=self.diameter, all_fields=True)[0]
                    bore = [[float(i) if is_float(i) else i for i in j] for j in bore]
                    for line in bore:
                        if len(line) == 5:
                            line.append('')
                    
                    for line in bore:
                        if line[4] == 'Spline':
                            raise Exception('Spline sections are not supported')

                    # Show loaded geometry
                    self.create_geometry_table(bore)
                    
                    # Enable tabs and give instructions
                    
                    if len(bore) > MAX_INSTRUMENT_SECTIONS:
                        bore = bore[:MAX_INSTRUMENT_SECTIONS]
                        self.mesagge.set(F'Loaded geometry has more than {MAX_INSTRUMENT_SECTIONS} sections, only the first {MAX_INSTRUMENT_SECTIONS} will be loaded')
                    else:
                        self.mesagge.set(f'{basename(file)} loaded correctly!')
                    self.geometry_frame_top_clear.state(['!disabled'])
                except Exception as e:
                    if str(e).startswith('bore'):
                        e = str(e).split(':')[-1]
                    self.mesagge.set(f'{e}')

    def clear_geometry(self):
        # clears bore sections
        self.bore_sections = None
        self.holes = None
        self.finger_chart = None
        
        # Resets geometry parameters
        self.geometry_frame_top_unit.config(state='normal')
        self.geometry_frame_top_unit.config(state='readonly')
        self.geometry_frame_top_radius.config(state='normal')
        self.geometry_frame_top_radius.config(state='readonly')
        self.geometry_frame_top_clear.state(['disabled'])
        
        # Disable tabs
        self.instrument_right_notebook.tab(0, state='disabled')
        self.instrument_left_notebook.tab(1, state='disabled')
        self.instrument_left_notebook.tab(2, state='disabled')
        
        # Reset geometry table
        self.create_geometry_table([])

        # Message
        self.mesagge.set('Geometry cleared correctly!')
        
        # Clear holes
        for widget in self.holes_frame.winfo_children():
            widget.destroy()
        
        # Clear finger chart
        for widget in self.finger_chart_frame.winfo_children():
            widget.destroy()
            
        # Clear view
        for widget in self.view_frame.winfo_children():
            widget.destroy()
    
    def save_geometry(self):
        self.get_values_geometry_table()
    
    def create_geometry_table(self, bore):
        for i, element in enumerate(bore):
            self.geometry_frame_middle_disabled[i] = True
            self.geometry_frame_middle_entries[i][-1].config(bg=self.colors[i])
            
            for j, entry in enumerate(element):
                if isinstance(self.geometry_frame_middle_entries[i][j], ttk.Combobox):
                    self.geometry_frame_middle_entries[i][j].config(state='normal')
                    self.geometry_frame_middle_entries[i][j].delete(0, 'end')
                    self.geometry_frame_middle_entries[i][j].insert(0, entry)
                    self.geometry_frame_middle_entries[i][j].config(state='readonly')
                elif isinstance(self.geometry_frame_middle_entries[i][j], ttk.Entry):
                    self.geometry_frame_middle_entries[i][j].config(state='normal')
                    self.geometry_frame_middle_entries[i][j].delete(0, 'end')
                    self.geometry_frame_middle_entries[i][j].insert(0, entry)
                        
            if self.geometry_frame_middle_entries[i][4].get() == 'Bessel':
                self.geometry_frame_middle_entries[i][5].config(state='normal')
            elif self.geometry_frame_middle_entries[i][4].get() == 'Circle':
                self.geometry_frame_middle_entries[i][5].config(state='normal')
            else:
                self.geometry_frame_middle_entries[i][5].delete(0, 'end')
                self.geometry_frame_middle_entries[i][5].config(state='disabled') 

        
        for i in range(len(bore), MAX_INSTRUMENT_SECTIONS):
            self.geometry_frame_middle_disabled[i] = False
            self.geometry_frame_middle_entries[i][-1].config(bg='#ffffff')
            for k, entry in enumerate(self.geometry_frame_middle_entries[i]):
                if isinstance(entry, ttk.Combobox):
                    entry.config(state='normal')
                    entry.delete(0, 'end')
                    entry.config(state='readonly')
                    entry.config(state='disabled')
                elif isinstance(entry, ttk.Entry):
                    entry.config(state='normal')
                    entry.delete(0, 'end')
                    entry.config(state='disabled')
    
    def enable_geometry_parameter(self, x):
        i = x[0] - 1; j = x[1]
        if self.geometry_frame_middle_entries[i][j].get() == 'Bessel':
            self.geometry_frame_middle_entries[i][j + 1].config(state='normal')
        elif self.geometry_frame_middle_entries[i][j].get() == 'Circle':
            self.geometry_frame_middle_entries[i][j + 1].config(state='normal')
        else:
            self.geometry_frame_middle_entries[i][j + 1].delete(0, 'end')
            self.geometry_frame_middle_entries[i][j + 1].config(state='disabled')
    
    def enable_geometry_row(self, i):
        i -= 1
        if self.geometry_frame_middle_disabled[i]:
            self.geometry_frame_middle_entries[i][-1].config(bg='#ffffff')
            for k, entry in enumerate(self.geometry_frame_middle_entries[i]):
                if isinstance(entry, ttk.Combobox):
                    entry.config(state='disabled')
                elif isinstance(entry, ttk.Entry):
                    entry.config(state='disabled')
        else:
            self.geometry_frame_middle_entries[i][-1].config(bg=self.colors[i])
            for k, entry in enumerate(self.geometry_frame_middle_entries[i]):
                if isinstance(entry, ttk.Combobox):
                    entry.config(state='normal')
                    entry.config(state='readonly')
                elif isinstance(entry, ttk.Entry):
                    entry.config(state='normal')
                    
            if self.geometry_frame_middle_entries[i][4].get() == 'Bessel':
                self.geometry_frame_middle_entries[i][5].config(state='normal')
            elif self.geometry_frame_middle_entries[i][4].get() == 'Circle':
                self.geometry_frame_middle_entries[i][5].config(state='normal')
            else:
                self.geometry_frame_middle_entries[i][5].delete(0, 'end')
                self.geometry_frame_middle_entries[i][5].config(state='disabled')
        
        self.geometry_frame_middle_disabled[i] = not self.geometry_frame_middle_disabled[i]
    
    def get_values_geometry_table(self):
        new_list = []
        
        # Get values from table, if empty row is found it is not added to the list
        for i, row in enumerate(self.geometry_frame_middle_entries):
            if self.geometry_frame_middle_disabled[i]:
                new_row = []
                empty = True
                for j, entry in enumerate(row):
                    if not isinstance(entry, Frame):
                        if isinstance(entry, Entry):
                            test = entry.cget('state')
                            if test.string == 'normal':
                                if entry.get() != '':
                                    empty = False
                        else:
                            if entry.get() != '':
                                empty = False           
                        new_row.append(entry.get()) 
                
                if not empty:
                    new_list.append(new_row)

        # Update geomtry table
        self.create_geometry_table(new_list)
        
        # Check for errors
        self.check_errors_geometry_table(new_list)
    
    def check_errors_geometry_table(self, bore):
        # All possible errors
        empty_segment_error = False
        empty_radius_error = False
        empty_parameter_error = False
        empty_type_error = False
        empty_error = False
        not_float_segment_error = False
        not_float_radius_error = False
        not_float_parameter_error = False
        not_float_error = False
        geometry_error = False
        circle_error = False
        extra_error = False
        
        # Check for empty or non float values on the table segments
        for i in range(len(bore)):
            for j in range(2):
                if bore[i][j] == '':
                    empty_segment_error = True
                if bore[i][j] != '':
                    if not is_float(bore[i][j]):
                        not_float_segment_error = True

        # Check for empty values on the table types
        for i in range(len(bore)):
            if bore[i][4] == '':
                empty_type_error = True
                
        # Check for empty or non float values on the rest of the table
        for i in range(len(bore)):
            if bore[i][4] == 'Bessel' or bore[i][4] == 'Circle':
                if bore[i][5] == '':
                    empty_parameter_error = True
                if bore[i][5] != '':
                    if not is_float(bore[i][5]):
                        not_float_parameter_error = True
        
        # Check for empty errors and non float errors
        empty_error = empty_segment_error or empty_parameter_error or empty_radius_error or empty_type_error
        not_float_error = not_float_segment_error or not_float_parameter_error or not_float_radius_error
        
        # Only when the data es valid, check for geometry errors
        if not empty_segment_error and not not_float_segment_error:
            for i in range(len(bore)):
                if i == 0:
                    if float(bore[0][1]) < float(bore[0][0]):
                        geometry_error = True
                else:
                    if float(bore[i][0]) < float(bore[i - 1][0]):
                        geometry_error = True
                    if float(bore[i][0]) < float(bore[i - 1][1]):
                        geometry_error = True
                    if float(bore[i][1]) < float(bore[i][0]):
                        geometry_error = True
                    if float(bore[i][1]) < float(bore[i - 1][0]):
                        geometry_error = True
                    if float(bore[i][1]) < float(bore[i - 1][1]):
                        geometry_error = True
        
        # Only when the data es valid, check for circle errors          
        if not empty_parameter_error and not empty_segment_error and not not_float_segment_error and not not_float_parameter_error:
            for i in range(len(bore)):            
                if self.geometry_frame_middle_entries[i][4].get() == 'Circle': 
                    if abs(float(bore[i][5])) <= 0.5 * abs(float(bore[i][0]) - float(bore[i][1])):
                        circle_error_text = f'Circle parameter must be greater than {0.5 * abs(float(bore[i][0]) - float(bore[i][1]))}'
                        circle_error = True

        # Print errors with some priority, if there are is any error al holes and possibly finger chart delelted and disabled
        if empty_error:
            self.clear_holes()
            self.mesagge.set('There are empty fields, please fill them')
            self.instrument_left_notebook.tab(1, state='disabled')
            self.instrument_left_notebook.tab(2, state='disabled')
        elif not_float_error:
            self.clear_holes()
            self.mesagge.set('There are non float values, please correct them')
            self.instrument_left_notebook.tab(1, state='disabled')
            self.instrument_left_notebook.tab(2, state='disabled')
        elif geometry_error:
            self.clear_holes()
            self.mesagge.set('There are geometry errors, please correct them')
            self.instrument_left_notebook.tab(1, state='disabled')
            self.instrument_left_notebook.tab(2, state='disabled')
        elif circle_error:
            self.clear_holes()
            self.mesagge.set(circle_error_text)
            self.instrument_left_notebook.tab(1, state='disabled')
            self.instrument_left_notebook.tab(2, state='disabled')
        else:
            # If there are no errors, checks for empty bore
            if bore == []:
                self.mesagge.set('Please load geometry or add a valid row to the table')
                self.bore_sections = None
            else:
                try:
                    self.instrument = InstrumentGeometry(main_bore=bore, unit=self.unit, diameter=self.diameter)
                except Exception as e:
                    if str(e).startswith('bore'):
                        e = str(e).split(':')[-1]
                    self.mesagge.set(f'{e}')
                    extra_error = True
                
                if not extra_error:
                    # If bore is nor empty, saves it
                    self.bore_sections = bore
                    
                    # Create new wigets
                    self.holes_widget()
                    self.view_widget()
                    
                    # Enable tabs
                    self.instrument_left_notebook.tab(1, state='normal')
                    self.instrument_right_notebook.tab(0, state='normal')
                    self.instrument_right_notebook.select(0)
                    
                    # Locks geometry parameters
                    self.geometry_frame_top_unit.config(state='readonly')
                    self.geometry_frame_top_unit.config(state='disabled')
                    self.geometry_frame_top_radius.config(state='readonly')
                    self.geometry_frame_top_radius.config(state='disabled')
                    self.view_frame_top_pop.state(['!disabled'])
                
                    # Plot geometry
                    self.plot()
                    
                    # Message
                    self.mesagge.set('Geometry saved correctly!')

    def change_unit(self, x):
        if self.geometry_frame_top_unit.get() == 'mm':
            self.unit = 'mm'
        else:
            self.unit = 'm'
    
    def change_radius(self, x):
        if self.geometry_frame_top_radius.get() == 'radius':
            self.diameter = False
            for element in self.geometry_frame_middle_labels:
                if element.cget('text') == 'Start\nDiameter':
                    element.config(text='Start\nRadius')
                if element.cget('text') == 'End\nDiameter':
                    element.config(text='End\nRadius') 

        else:
            self.diameter = True
            for element in self.geometry_frame_middle_labels:
                if element.cget('text') == 'Start\nRadius':
                    element.config(text='Start\nDiameter')
                if element.cget('text') == 'End\nRadius':
                    element.config(text='End\nDiameter')
    
    def load_holes(self):
        # Select file by user
        file = filedialog.askopenfilename(title='Select a file for the holes')
        
        # Check if selected file is a valid .txt or .csv file
        if file:
            if file.split('.')[-1] != 'txt' and file.split('.')[-1] != 'csv':
                self.instruction.set('Please load valid file')
            else:
                self.instrument = InstrumentGeometry(main_bore=self.bore_sections, holes_valves=file)       
                holes = self.instrument.get_bore_list(unit=self.unit, diameter=self.diameter, all_fields=False)[1]
                holes = [[float(i) if is_float(i) else i for i in j] for j in holes]
                for line in holes:
                    if len(line) == 4:
                        line.append(line[-1])
                
        
                self.holes_label = holes[0]
                if self.holes_label[-1] == '':
                    if self.holes_label[-2] == 'radius':
                        self.holes_label[-1] = 'radius_out'
                    if self.holes_label[-2] == 'diameter':
                        self.holes_label[-1] = 'diameter_out'
                # impedance_(self.holes_label)
                holes = holes[1:]
                
                # Show loaded holes
                self.create_holes_table(holes)
                
                # Enable tabs and give instructions
                if len(holes) > MAX_INSTRUMENT_HOLES + 1:
                    holes = holes[:MAX_INSTRUMENT_HOLES + 1]
                    self.mesagge.set(F'Loaded holes have more than {MAX_INSTRUMENT_HOLES} holes, only the first {MAX_INSTRUMENT_HOLES} will be loaded')
                else:
                    self.mesagge.set(f'{basename(file)} loaded correctly!')
                self.holes_frame_top_clear.state(['!disabled'])
    
    def clear_holes(self):
        # Clears holes
        self.holes = None
        self.finger_chart = None
        
        # Resets holes parameters
        self.holes_frame_top_clear.state(['disabled'])
        self.view_frame_top_sideview.state(['disabled'])
        self.view_frame_top_topview.state(['disabled'])
        self.view_frame_top_notes.config(state='normal')
        self.view_frame_top_notes.delete(0, 'end')
        self.view_frame_top_notes.insert(0, 'None')
        self.view_frame_top_notes.config(state='readonly')
        self.view_frame_top_notes.config(state='disabled')
        self.instrument_left_notebook.tab(2, state='disabled')
        
        # Reset holes table
        self.create_holes_table([])
        
        # Message
        self.mesagge.set('holes cleared correctly!')
        
        # Clear finger chart
        for widget in self.finger_chart_frame.winfo_children():
            widget.destroy()

        # Clear view for holes
        self.plot()

    def save_holes(self):
        self.get_values_holes_table()
    
    def create_holes_table(self, holes):
        for i, element in enumerate(holes):
            self.holes_frame_middle_disabled[i] = True
            self.holes_frame_middle_entries[i][-1].config(bg=self.colors[i])
            
            for j, entry in enumerate(element):
                if isinstance(self.holes_frame_middle_entries[i][j], ttk.Entry):
                    self.holes_frame_middle_entries[i][j].config(state='normal')
                    self.holes_frame_middle_entries[i][j].delete(0, 'end')
                    self.holes_frame_middle_entries[i][j].insert(0, entry)
                    
        for i in range(len(holes), MAX_INSTRUMENT_HOLES):
            self.holes_frame_middle_disabled[i] = False
            self.holes_frame_middle_entries[i][-1].config(bg='#ffffff')
            for k, entry in enumerate(self.holes_frame_middle_entries[i]):
                if isinstance(entry, ttk.Combobox):
                    entry.config(state='normal')
                    entry.delete(0, 'end')
                    entry.config(state='readonly')
                    entry.config(state='disabled')
                elif isinstance(entry, ttk.Entry):
                    entry.config(state='normal')
                    entry.delete(0, 'end')
                    entry.config(state='disabled')
    
    def enable_holes_row(self, i):
        i -= 1
        if self.holes_frame_middle_disabled[i]:
            self.holes_frame_middle_entries[i][-1].config(bg='#ffffff')
            for k, entry in enumerate(self.holes_frame_middle_entries[i]):
                if isinstance(entry, ttk.Entry):
                    entry.config(state='disabled')
        else:
            self.holes_frame_middle_entries[i][-1].config(bg=self.colors[i])
            for k, entry in enumerate(self.holes_frame_middle_entries[i]):
                if isinstance(entry, ttk.Entry):
                    entry.config(state='normal')
                    
        
        self.holes_frame_middle_disabled[i] = not self.holes_frame_middle_disabled[i]
    
    def get_values_holes_table(self):
        new_list = []
        
        # Get values from table, if empty row is found it is not added to the list
        for i, row in enumerate(self.holes_frame_middle_entries):
            if self.holes_frame_middle_disabled[i]:
                new_row = []
                empty = True
                for j, entry in enumerate(row):
                    if not isinstance(entry, Frame):
                        test = entry.cget('state')
                        if test.string == 'normal':
                            if entry.get() != '':
                                empty = False         
                        new_row.append(entry.get()) 
                
                if not empty:
                    new_list.append(new_row)

        # Update holes table
        self.create_holes_table(new_list)
        
        # Check for errors
        self.check_errors_holes_table(new_list)
    
    def check_errors_holes_table(self, holes):
        # If holes is empty, print error
        if holes == []:
                self.mesagge.set('Please load holes or add a valid row to the table')
                self.holes = None
                self.plot()
        else:
            # All possible errors
            empty_error = False
            empty_label_error = False
            empty_position_error = False
            empty_radius_in_error = False
            empty_parameter_error = False
            not_float_error = False
            not_float_position_error = False
            not_float_radius_in_error = False
            not_float_parameter_error = False
            repeated_label_error = False
            
            outside_geometry_error = False
            bigger_radius_error = False
            extra_error = False
            
            labels = []
            positions = []
            radius = []
            for i in range(len(holes)):
                for j in range(len(holes[i])):
                    if j == 0:
                        if holes[i][0] == '':
                            empty_label_error = True
                        else:
                            labels.append(holes[i][0])
                    elif j == 1:
                        if holes[i][1] == '':
                            empty_position_error = True
                        elif not is_float(holes[i][1]):
                            not_float_position_error = True
                        else:
                            positions.append(float(holes[i][1]))
                    elif j == 3:
                        if holes[i][3] == '':
                            empty_radius_in_error = True
                        elif not is_float(holes[i][3]):
                            not_float_radius_in_error = True
                        else:
                            radius.append(float(holes[i][3]))
                    else:
                        if holes[i][j] == '':
                            empty_parameter_error = True
                        if not is_float(holes[i][j]):
                            not_float_parameter_error = True
                            
            labels_set = set(labels)
            if len(labels) != len(labels_set):
                repeated_label_error = True
                
            empty_error = empty_label_error or empty_position_error or empty_parameter_error or empty_radius_in_error
            not_float_error = not_float_position_error or not_float_radius_in_error or not_float_parameter_error
            
            if not empty_position_error:
                position_out = [True] * len(positions)
                for i, p in enumerate(positions):
                    for j in range(len(self.bore_sections)):
                        if float(p) >= float(self.bore_sections[j][0]) and float(p) <= float(self.bore_sections[j][1]):
                            position_out[i] = False
                if any(position_out):
                    outside_geometry_error = True
                    
            if not empty_position_error and not empty_radius_in_error and not not_float_position_error and not not_float_radius_in_error and not outside_geometry_error and not repeated_label_error:       
                test_holes = [self.holes_label] + holes
                try:
                    instrument_test = InstrumentGeometry(main_bore=self.bore_sections, holes_valves=test_holes, unit=self.unit, diameter=self.diameter)
                except Exception as e:
                    if str(e).startswith('bore'):
                        e = str(e).split(':')[-1]
                    self.mesagge.set(f'{e}')
                    extra_error = True
                if self.unit == 'mm':
                    positions = [i / 1000 for i in positions]
                    radius = [i / 1000 for i in radius]
                    
                radius_at_hole = []
                for i, p in enumerate(positions):
                    radius_at_hole.append(instrument_test.get_main_bore_radius_at(p).item())
                # print(radius_at_hole)
                
                if self.diameter:
                    radius_at_hole = [i * 2 for i in radius_at_hole]
                
                for i, r in enumerate(radius_at_hole):
                    if r < radius[i]:
                        bigger_radius_error = True
            
            # Print errors with some priority, if there are is any error al holes and possibly finger chart delelted and disabled
            if empty_error:
                self.clear_finger_chart()
                self.mesagge.set('There are empty fields, please fill them')
                self.instrument_left_notebook.tab(2, state='disabled')
                self.view_frame_top_topview.state(['disabled'])
                self.view_frame_top_pop.state(['disabled'])
                self.view_frame_top_sideview.state(['disabled'])
            elif repeated_label_error:
                self.clear_finger_chart()
                self.mesagge.set('There are repeated labels, please correct them')
                self.instrument_left_notebook.tab(2, state='disabled')
                self.view_frame_top_topview.state(['disabled'])
                self.view_frame_top_pop.state(['disabled'])
                self.view_frame_top_sideview.state(['disabled'])
            elif not_float_error:
                self.clear_finger_chart()
                self.mesagge.set('There are non float values, please correct them')
                self.instrument_left_notebook.tab(2, state='disabled')
                self.view_frame_top_topview.state(['disabled'])
                self.view_frame_top_pop.state(['disabled'])
                self.view_frame_top_sideview.state(['disabled'])
            elif outside_geometry_error:
                self.clear_finger_chart()
                self.mesagge.set('There are holes outside the geometry, please correct them')
                self.instrument_left_notebook.tab(2, state='disabled')
                self.view_frame_top_topview.state(['disabled'])
                self.view_frame_top_pop.state(['disabled'])
                self.view_frame_top_sideview.state(['disabled'])
            elif bigger_radius_error:
                self.clear_finger_chart()
                self.mesagge.set('There are holes with bigger radius than the section on its position, please correct them')
                self.instrument_left_notebook.tab(2, state='disabled')
                self.view_frame_top_topview.state(['disabled'])
                self.view_frame_top_pop.state(['disabled'])
                self.view_frame_top_sideview.state(['disabled'])
            else:
                if not extra_error:
                    # If there are no errors, saves holes and holes names
                    self.holes = holes
                    self.holes_names = ['label'] + [i[0] for i in holes]
                    
                    # Enable tabs and parameters
                    self.instrument_left_notebook.tab(2, state='normal')
                    self.view_frame_top_topview.state(['!disabled'])
                    self.view_frame_top_pop.state(['!disabled'])
                    self.view_frame_top_sideview.state(['!disabled'])
                    
                    # Message
                    self.mesagge.set('Holes saved correctly!')
                    
                    # Create finger chart
                    self.finger_chart_widget()
                    self.create_finger_chart_table()
                    
                    # Add holes names to holes for ploting
                    self.holes = [self.holes_label] + self.holes
                    
                    # Update plot
                    self.plot()

    def load_finger_chart(self):
        # Select file by user
        file = filedialog.askopenfilename(title='Select a file for the finger chart')
        
        # Check if selected file is a valid .txt or .csv file
        if file:
            if file.split('.')[-1] != 'txt' and file.split('.')[-1] != 'csv':
                self.mesagge.set('Please load valid file')
            else:
                with open(file, 'r') as f:
                    lines = f.readlines()
                    
                lines = [line.strip('\n') for line in lines]
                lines = [line.split(' ') for line in lines]
                fingers = []
                for line in lines:
                    line = [i for i in line if i != '']
                    fingers.append(line)
                
                fingers = traverse(fingers)
                
                # Check if finger chart matches the holes names
                if fingers[0] != self.holes_names:
                    self.mesagge.set('The exported finger chart does not match the hole names of the instrument, please correct them')
                else:
                    if len(fingers[0]) > MAX_INSTRUMENT_NOTES + 1:
                        for i in range(len(fingers)):
                            fingers[i] = fingers[i][:MAX_INSTRUMENT_NOTES + 1]
                        self.mesagge.set(F'Loaded finger chart has more than {MAX_INSTRUMENT_NOTES} notes, only the first {MAX_INSTRUMENT_NOTES} will be loaded')
                    else:
                        self.mesagge.set(f'{basename(file)} loaded correctly!')
                    self.set_finger_chart_values(fingers[1:])

    def clear_finger_chart(self):
        # Clears finger chart
        self.finger_chart = None
        
        # Resets finger chart parameters
        self.instrument_parent.tab(1, state='disabled')
        self.instrument_parent.tab(2, state='disabled')
        self.instrument_parent.tab(3, state='disabled')
        self.view_frame_top_notes.config(state='normal')
        self.view_frame_top_notes.delete(0, 'end')
        self.view_frame_top_notes.insert(0, 'None')
        self.view_frame_top_notes.config(state='readonly')
        self.view_frame_top_notes.config(state='disabled')
        self.finger_chart_frame_top_clear.state(['disabled'])
        
        # Clear finger chart table
        self.set_finger_chart_values([])
        
        # Message
        self.mesagge.set('Finger chart cleared correctly!')

        # Update plot
        self.plot()
    
    def save_finger_chart(self):
        new_list = []
        
        # Get values from table
        for i in range(1, len(self.finger_chart_frame_middle_entries) + 1):
            if self.finger_chart_frame_middle_disabled[i - 1]:
                new_row = []
                empty = True
                for j, entry in enumerate(self.finger_chart_frame_middle_entries[i]):
                    if not isinstance(entry, Frame):
                        test = entry.cget('state')
                        to_append = ''
                        if test.string == 'normal' or test.string == 'readonly':
                            if entry.get() != '':
                                empty = False
                                to_append = entry.get()
                                if to_append == '○':
                                    to_append = 'o'   
                                elif to_append == '●':
                                    to_append = 'x' 
                        new_row.append(to_append) 
                
                if not empty:
                    new_list.append(new_row)
        
        if new_list == []:
            self.mesagge.set('Please load finger chart or add a valid row to the table')
            self.finger_chart = None
        else:
            self.set_finger_chart_values(new_list)
            self.check_errors_finger_chart_table(new_list)
    
    def create_finger_chart_table(self):
        self.finger_chart_frame_middle_entries = list()
        self.finger_chart_frame_middle_disabled = [False] * (MAX_INSTRUMENT_NOTES + 1)
        for widget in self.finger_chart_frame_middle.winfo_children():
            widget.destroy()
        
        entry_row = list()
        self.finger_chart_frame_middle.rowconfigure(0, weight=1)
        for j in range(len(self.holes) + 2):
            self.finger_chart_frame_middle.columnconfigure(j, weight=1)
            if j == 0:
                entry = ttk.Label(self.finger_chart_frame_middle, text='N \ H', anchor='center', justify='center')
                entry.grid(column=j, row=0, sticky=(N, S, W, E), padx=2, pady=2)
                entry_row.append(entry)
            elif j == len(self.holes) + 1:
                entry = ttk.Label(self.finger_chart_frame_middle, text='Enabled', anchor='center', justify='center')
                entry.grid(column=j, row=0, sticky=(N, S, W, E), padx=2, pady=2)
                entry_row.append(entry)
            else:
                entry = ttk.Label(self.finger_chart_frame_middle, text=self.holes_names[j], anchor='center', justify='center')
                entry.grid(column=j, row=0, sticky=(N, S, W, E), padx=2, pady=2)
                entry_row.append(entry)
        self.finger_chart_frame_middle_entries.append(entry_row)
        
        for i in range(MAX_INSTRUMENT_NOTES):
            entries_row = list()
            self.finger_chart_frame_middle.rowconfigure(i + 1, weight=2)
            for j in range(len(self.holes) + 2):
                if j == 0:
                    entry = ttk.Entry(self.finger_chart_frame_middle, width=3)
                    entry.grid(column=j, row=i + 1, sticky=(W, E), padx=2, pady=2)
                    entries_row.append(entry)
                elif j == len(self.holes) + 1:
                    entry = Frame(self.finger_chart_frame_middle)
                    entry.grid(column=j, row=i + 1, sticky=(N, S, W, E), padx=10, pady=15)
                    entry.columnconfigure(0, weight=1)
                    entry.rowconfigure(0, weight=1)
                    entry.config(bg='#ffffff', highlightbackground=self.colors[i], highlightthickness=1)
                    entry.bind('<Button-1>', lambda event, x=i: self.enable_finger_chart_row(x))
                    entries_row.append(entry)  
                else:
                    entry = ttk.Combobox(self.finger_chart_frame_middle, width=1,
                        values=['○', '●'])
                    entry.grid(row=i + 1, column=j, sticky=(W, E), padx=5)
                    entry.insert(0, '○')
                    entry.config(state='readonly')
                    entry.config(state='disabled')
                    entries_row.append(entry)
            self.finger_chart_frame_middle_entries.append(entries_row)
    
    def enable_finger_chart_row(self, i):
        if self.finger_chart_frame_middle_disabled[i]:
            self.finger_chart_frame_middle_entries[i + 1][-1].config(bg='#ffffff')
            for k, entry in enumerate(self.finger_chart_frame_middle_entries[i + 1]):
                if isinstance(entry, ttk.Entry):
                    entry.config(state='disabled')
                elif isinstance(entry, ttk.Combobox):
                    entry.config(state='disabled')
                    
        else:
            self.finger_chart_frame_middle_entries[i + 1][-1].config(bg=self.colors[i])
            for k, entry in enumerate(self.finger_chart_frame_middle_entries[i + 1]):
                if k == 0:
                    entry.config(state='normal')
                else:
                    if not isinstance(entry, Frame):
                        entry.config(state='normal')
                        entry.config(state='readonly')
        
        self.finger_chart_frame_middle_disabled[i] = not self.finger_chart_frame_middle_disabled[i]
    
    def set_finger_chart_values(self, fingers):
        for i, element in enumerate(fingers):
            self.finger_chart_frame_middle_disabled[i] = True
            self.finger_chart_frame_middle_entries[i + 1][-1].config(bg=self.colors[i])
            
            for j, entry in enumerate(element):
                if j == 0:
                    self.finger_chart_frame_middle_entries[i + 1][j].config(state='normal')
                    self.finger_chart_frame_middle_entries[i + 1][j].delete(0, 'end')
                    self.finger_chart_frame_middle_entries[i + 1][j].insert(0, entry)
                else:
                    if not isinstance(self.finger_chart_frame_middle_entries[i + 1][j], Frame):
                        self.finger_chart_frame_middle_entries[i + 1][j].config(state='normal')
                        self.finger_chart_frame_middle_entries[i + 1][j].delete(0, 'end')
                        if entry == 'o':
                            entry = '○'
                        elif entry == 'x':
                            entry = '●'
                        self.finger_chart_frame_middle_entries[i + 1][j].insert(0, entry)
                        self.finger_chart_frame_middle_entries[i + 1][j].config(state='readonly')

        for i in range(len(fingers), MAX_INSTRUMENT_NOTES):
            self.finger_chart_frame_middle_disabled[i] = False
            self.finger_chart_frame_middle_entries[i + 1][-1].config(bg='#ffffff')
            for j, entry in enumerate(self.finger_chart_frame_middle_entries[0]):
                if j == 0:
                    self.finger_chart_frame_middle_entries[i + 1][j].config(state='normal')
                    self.finger_chart_frame_middle_entries[i + 1][j].delete(0, 'end')
                    self.finger_chart_frame_middle_entries[i + 1][j].config(state='disabled')
                else:
                    if not isinstance(self.finger_chart_frame_middle_entries[i + 1][j], Frame):
                        self.finger_chart_frame_middle_entries[i + 1][j].config(state='normal')
                        self.finger_chart_frame_middle_entries[i + 1][j].delete(0, 'end')
                        self.finger_chart_frame_middle_entries[i + 1][j].insert(0, '○')
                        self.finger_chart_frame_middle_entries[i + 1][j].config(state='readonly')
                        self.finger_chart_frame_middle_entries[i + 1][j].config(state='disabled')
    
    def check_errors_finger_chart_table(self, fingers):
        # Check for errors
        empty_name_error = False
        empty_chart_error = False
        empty_error = False
        repeated_label_error = False
        
        labels = []
        for i in range(len(fingers)):
            for j in range(len(fingers[i])):
                if j == 0:
                    if fingers[i][0] == '':
                        empty_name_error = True
                    else:
                        labels.append(fingers[i][0])
                else:
                    if fingers[i][j] == '':
                        empty_chart_error = True
                
        labels_set = set(labels)
        if len(labels) != len(labels_set):
            repeated_label_error = True
        
        empty_error = empty_name_error or empty_chart_error
        
        if empty_error:
            self.mesagge.set('There are empty fields, please fill them')
        elif repeated_label_error:
            self.mesagge.set('There are repeated labels, please correct them')
        else:
            # If there are no errors, saves finger chart
            self.finger_chart = fingers
            self.finger_chart =  [self.holes_names] + self.finger_chart
            
            # Create finger chart dictionary
            self.finger_chart_dict = {}
            for element in self.finger_chart[1:]:
                self.finger_chart_dict.update({element[0]: element[1:]})
                
            self.finger_chart = traverse(self.finger_chart)
            self.notes = self.finger_chart[0][1:]
            self.notes_available = True
            
            # Enable tabs and parameters
            self.finger_chart_frame_top_clear.state(['!disabled'])
            self.instrument_parent.tab(1, state='normal')

            # Updates notes combobox
            self.view_frame_top_notes = ttk.Combobox(self.view_frame_top, width=10, values=['None'] + self.notes)
            self.view_frame_top_notes.grid(column=4, row=0, sticky=(N, S, W, E), padx=2, pady=2)
            self.view_frame_top_notes.grid_propagate(0)
            self.view_frame_top_notes.bind('<<ComboboxSelected>>', lambda event, x=0: self.change_note(x))
            self.view_frame_top_notes.config(state='normal')
            self.view_frame_top_notes.delete(0, 'end')
            self.view_frame_top_notes.insert(0, 'None')
            self.view_frame_top_notes.config(state='readonly')
            
            # Defines instrument to work with
            self.instrument = InstrumentGeometry(main_bore=self.bore_sections, holes_valves=self.holes, 
                fingering_chart=self.finger_chart, unit=self.unit, diameter=self.diameter)
            
            # Message
            self.mesagge.set('Finger chart saved correctly!')
            
            # Update plot
            # self.plot()
            
            # Create files with instrument data
            path = dirname(abspath(__file__))
            folder_path = join(path, 'data')
            if exists(folder_path):
                try:
                    rmtree(folder_path)
                except Exception as e:
                    print(f"Error deleting '{folder_path}': {e}")
            makedirs(folder_path)
            # print(f"Folder 'data' created successfully at '{folder_path}'")
            
            self.instrument.write_files(generic_name=join(folder_path, 'instrument'), 
                extension ='.txt', unit=self.unit, diameter=self.diameter)
            
            # Create impedance frame
            self.new_impedance_frame = impedance(root=self.root, parent=self.instrument_parent, style=self.style, instrument=self.instrument, 
                bore=self.bore_sections, holes=self.holes, 
                fingers=self.finger_chart, notes=self.notes, 
                unit=self.unit, diameter=self.diameter)
            self.instrument_parent.forget(1)
            self.instrument_parent.insert(1, self.new_impedance_frame.impedance_frame, text='Impedance')

    def plot(self, note=None):
        # Check if figure is already open, if so, close it
        plt.close()
            
        if self.finger_chart:
            self.instrument = InstrumentGeometry(main_bore=self.bore_sections, holes_valves=self.holes, fingering_chart=self.finger_chart, unit=self.unit, diameter=self.diameter)
        elif self.holes:
            self.instrument = InstrumentGeometry(main_bore=self.bore_sections, holes_valves=self.holes, unit=self.unit, diameter=self.diameter)
        else:
            self.instrument = InstrumentGeometry(main_bore=self.bore_sections, unit=self.unit, diameter=self.diameter)
            
        self.check_figure = True

        # Create figure
        self.geometry_figure = plt.figure(figsize=(1, 1), dpi=100)
        
        position = [0, 0, 0.5, 1]
        gs = gridspec.GridSpec(1, 1)
        gs.tight_layout(self.geometry_figure, rect=position)
        if note:
            self.instrument.plot_InstrumentGeometry(figure=self.geometry_figure, double_plot=True, note=note)
        else:
            self.instrument.plot_InstrumentGeometry(figure=self.geometry_figure, double_plot=True)
        ax = self.geometry_figure.get_axes()
        for axe in ax:
            axe.grid()
        if self.holes:
            if note:
                poligons = []
                for axe in ax:
                    poligons.append(axe.findobj(plt.Polygon))
                    
                finger_chart = self.finger_chart_dict[note] 
                finger_types = []
                for i in range(len(ax)):
                    finger_type_ax = []
                    hole_count = len(self.bore_sections)
                    poly_count = 0
                    for element in finger_chart:
                        if element == 'o':
                            finger_type_ax.append(ax[i].lines[hole_count])
                            hole_count += 1
                        else:
                            finger_type_ax.append(poligons[i][poly_count])
                            poly_count += 1
                    finger_types.append(finger_type_ax)
                if self.top_view == True:
                    ax[0].remove()
                    plt.title('Instrument Geometry top view')
                    for i in range(len(self.bore_sections)):
                        ax[1].lines[i].set_color(self.colors[i])
                    for i in range(len(self.holes) - 1):
                        finger_types[1][i].set_color(self.colors[i])     
                    ax[1].set_position(gs[0].get_position(self.geometry_figure))
                    ax[1].set_xlabel('Position (mm)')
                else:
                    ax[1].remove()
                    plt.title('Instrument Geometry side view')
                    for i in range(len(self.bore_sections)):
                        ax[0].lines[i].set_color(self.colors[i])
                    for i in range(len(self.holes) - 1):
                        finger_types[0][i].set_color(self.colors[i])
                    ax[0].set_position(gs[0].get_position(self.geometry_figure)) 
                
            else:
                if self.top_view == True:
                    ax[0].remove()
                    plt.title('Instrument Geometry top view')
                    for i in range(len(self.bore_sections)):
                        ax[1].lines[i].set_color(self.colors[i])
                    for i in range(len(self.holes) - 1):
                        ax[1].lines[i + len(self.bore_sections)].set_color(self.colors[i])
                    ax[1].set_position(gs[0].get_position(self.geometry_figure))
                    ax[1].set_xlabel('Position (mm)')
                else:
                    ax[1].remove()
                    plt.title('Instrument Geometry side view')
                    for i in range(len(self.bore_sections)):
                        ax[0].lines[i].set_color(self.colors[i])
                    for i in range(len(self.holes) - 1):
                        ax[0].lines[i + len(self.bore_sections)].set_color(self.colors[i])
                    ax[0].set_position(gs[0].get_position(self.geometry_figure))     
        else:
            for i in range(len(self.bore_sections)):
                ax[0].lines[i].set_color(self.colors[i])
            plt.title('Instrument sections view')

        
        # Create canvas with figure
        canvas = FigureCanvasTkAgg(self.geometry_figure, self.view_frame_middle)
        canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, W, E, S), pady=10)
    
    def export(self):
        if self.view_frame_top_name.get() != '':
            self.instrument.write_files(generic_name=self.view_frame_top_name.get(), extension='txt', unit=self.unit, diameter=self.diameter, )
            self.mesagge.set('Files exported correctly!')
        else:
            self.mesagge.set('Please enter a name for the files')
    
    def change_view(self, x):
        if self.top_view != x:
            self.top_view = x
            note = self.view_frame_top_notes.get()
            if note != 'None' and note != '':
                note = self.view_frame_top_notes.get()
                self.plot(note)
            else:
                self.plot()
    
    def change_note(self, x):
        note = self.view_frame_top_notes.get()
        if note != 'None' and note != '':
            self.plot(note=note)
        else:
            self.plot()
    
    def pop(self, x):
        self.plot()
        # Get the screen size
        fig = plt.gcf()
        screen_width, screen_height = fig.canvas.get_width_height()

        # Set figure size to fill the screen
        fig.set_size_inches(screen_width / 100, screen_height / 100)

        plt.show()
        plt.close()
        


    def dummy(self):
        pass
    
    
    
def is_float(s):
    try:
        float_value = float(s)
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



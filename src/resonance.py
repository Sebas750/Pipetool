# Tkinter
from tkinter import *
from tkinter import ttk
from ttkbootstrap.scrolled import ScrolledFrame

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

# Inharmonicity
from inharmonicity import inharmonicity

class resonance():
    def __init__(self, root=None, parent=None, style=None, instrument=None,
            res_f=None, res_Q=None, res_Y=None, res_flow=None,
            res_pressure=None, position=None, table_info=None,
            simulation_notes=None, notes=None) -> None:
        
        
        self.root = root
        # Set parent
        self.style = style
        self.parent = parent
        self.instrument = instrument
        self.res_f = res_f
        self.res_Q = res_Q
        self.res_Y = res_Y
        self.res_flow = res_flow
        self.res_pressure = res_pressure
        self.position = position
        self.table_info = table_info
        self.simulation_notes = simulation_notes
        self.notes = notes
        self.to_plot_notes = [True] * (len(self.notes) * 4)
        self.enable_notes = [True] * (len(self.notes) * 4)
        self.single_note_display = [False] * len(self.notes)
        self.flow = False
        self.view_frame_middle = None
        
        self.colors = ['#F44346', '#9C27B0', '#3F51B5', '#03A9F4', '#009688', 
            '#8BC34A', '#FFEB3B', '#FF9800', '#795548', '#607D8B', 
            '#37474F', '#9E9E9E', '#FF5722', '#FFC107', '#CDDC39', 
            '#4CAF50', '#00BCD4', '#2196F3', '#673AB7', '#E91E63', 
            '#F44346', '#9C27B0', '#3F51B5', '#03A9F4', '#009688', 
            '#8BC34A', '#FFEB3B', '#FF9800', '#795548', '#607D8B', 
            '#37474F', '#9E9E9E', '#FF5722', '#FFC107', '#CDDC39', 
            '#4CAF50', '#00BCD4', '#2196F3', '#673AB7', '#E91E63',
            '#F44346', '#9C27B0', '#3F51B5', '#03A9F4', '#009688', 
            '#8BC34A', '#FFEB3B', '#FF9800', '#795548', '#607D8B', 
            '#37474F', '#9E9E9E', '#FF5722', '#FFC107', '#CDDC39', 
            '#4CAF50', '#00BCD4', '#2196F3', '#673AB7', '#E91E63', 
            '#F44346', '#9C27B0', '#3F51B5', '#03A9F4', '#009688', 
            '#8BC34A', '#FFEB3B', '#FF9800', '#795548', '#607D8B', 
            '#37474F', '#9E9E9E', '#FF5722', '#FFC107', '#CDDC39', 
            '#4CAF50', '#00BCD4', '#2196F3', '#673AB7', '#E91E63']
        
        self.message = StringVar()
        self.message.set('RESONANCE')
        
        self.create_widgets(parent)
        self.table_widgets()
        self.view_widgets()
        
    def create_widgets(self, parent):
        # Instrument main frame
        self.resonance_frame = ttk.Frame(parent)
        self.resonance_frame.columnconfigure(0, weight=1)
        self.resonance_frame.columnconfigure(1, weight=1)
        self.resonance_frame.rowconfigure(0, weight=1)
        self.resonance_frame.grid_propagate(0)
        self.parent.add(self.resonance_frame, text='Resonance')
        
        # Instrumenr left frame
        self.resonance_left_frame = ttk.Frame(self.resonance_frame)
        self.resonance_left_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.resonance_left_frame.columnconfigure(0, weight=1)
        self.resonance_left_frame.rowconfigure(0, weight=1)
        self.resonance_left_frame.grid_propagate(0)
        
        # Instrument right frame
        self.resonance_right_frame = ttk.Frame(self.resonance_frame)
        self.resonance_right_frame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.resonance_right_frame.columnconfigure(0, weight=1)
        self.resonance_right_frame.rowconfigure(0, weight=1)
        self.resonance_right_frame.grid_propagate(0)
        
        # Instrument left notebook
        self.resonance_left_notebook = ttk.Notebook(self.resonance_left_frame)
        self.resonance_left_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.resonance_left_notebook.columnconfigure(0, weight=1)
        self.resonance_left_notebook.rowconfigure(0, weight=1)
        self.resonance_left_notebook.grid_propagate(0)
        
        # Instrument right notebook
        self.resonance_right_notebook = ttk.Notebook(self.resonance_right_frame)
        self.resonance_right_notebook.grid(column=0, row=0, sticky=(N, W, E, S))
        self.resonance_right_notebook.columnconfigure(0, weight=1)
        self.resonance_right_notebook.rowconfigure(0, weight=1)
        self.resonance_right_notebook.grid_propagate(0)  
        
    def table_widgets(self):
        self.table_frame = ttk.Frame(self.resonance_left_notebook)
        self.resonance_left_notebook.add(self.table_frame, text='Resonance Table')
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=2)
        self.table_frame.rowconfigure(1, weight=36)
        self.table_frame.rowconfigure(2, weight=2)
        self.table_frame.grid_propagate(0)
        
        # Table top subframe
        self.table_frame_top = ttk.Frame(self.table_frame)
        self.table_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.table_frame_top.columnconfigure(0, weight=1)
        self.table_frame_top.columnconfigure(1, weight=1)
        self.table_frame_top.columnconfigure(2, weight=1)
        self.table_frame_top.columnconfigure(3, weight=1)
        self.table_frame_top.columnconfigure(4, weight=1)
        self.table_frame_top.rowconfigure(0, weight=1)
        self.table_frame_top.grid_propagate(0)
        
        self.table_frame_top_label = ttk.Label(self.table_frame_top, text='Number of peaks:')
        self.table_frame_top_label.grid(column=0, row=0, sticky=(N, W, S), padx=2, pady=2)
        self.table_frame_top_number_peaks = ttk.Combobox(self.table_frame_top, values=[1, 2, 3, 4], state='readonly')
        self.table_frame_top_number_peaks.current(3)
        self.table_frame_top_number_peaks.grid(column=1, row=0, sticky=(N, W, S), padx=2, pady=2)
        self.table_frame_top_number_peaks.bind('<<ComboboxSelected>>', lambda event, x='': self.update_table(x))
        self.table_frame_top_name_label = ttk.Label(self.table_frame_top, text='Name:', anchor='center', justify='center')
        self.table_frame_top_name_label.grid(column=2, row=0, sticky=(N, S, W, E), pady=2)
        self.table_frame_top_name_label.grid_propagate(0)
        self.table_frame_top_name = ttk.Entry(self.table_frame_top, width=10)
        self.table_frame_top_name.grid(column=3, row=0, sticky=(N, S, W, E), padx=2, pady=2)
        self.table_frame_top_name.grid_propagate(0)
        self.table_frame_top_export = ttk.Button(self.table_frame_top, text='Export to files', command=self.export, style='primary.Outline.TButton')
        self.table_frame_top_export.grid(column=4, row=0, sticky=(N, W, S), padx=2, pady=2)
        self.table_frame_top_export.grid_propagate(0)
        
        # Table middle subframe
        self.table_frame_middle = Frame(self.table_frame)
        self.table_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.table_frame_middle.columnconfigure(0, weight=1)
        self.table_frame_middle.columnconfigure(1, weight=1)
        self.table_frame_middle.columnconfigure(2, weight=1)
        self.table_frame_middle.columnconfigure(3, weight=1)
        self.table_frame_middle.columnconfigure(4, weight=1)
        self.table_frame_middle.rowconfigure(0, weight=1)
        self.table_frame_middle.rowconfigure(1, weight=24)
        self.table_frame_middle.grid_propagate(0)
        
        self.table_frame_middle_label_1 = ttk.Label(self.table_frame_middle, text='Note peaks', anchor='center', justify='center', width=-25)
        self.table_frame_middle_label_1.grid(column=0, row=0, sticky=(N, W, E, S), pady=2)
        self.table_frame_middle_label_2 = ttk.Label(self.table_frame_middle, text='Frequency (Hz)', anchor='center', justify='center', width=-25)
        self.table_frame_middle_label_2.grid(column=1, row=0, sticky=(N, W, E, S), pady=2)
        self.table_frame_middle_label_3 = ttk.Label(self.table_frame_middle, text='Closest pitch (cent)', anchor='center', justify='center', width=-25)
        self.table_frame_middle_label_3.grid(column=2, row=0, sticky=(N, W, E, S), pady=2)
        self.table_frame_middle_label_4 = ttk.Label(self.table_frame_middle, text='Quality factor', anchor='center', justify='center', width=-25)
        self.table_frame_middle_label_4.grid(column=3, row=0, sticky=(N, W, E, S), pady=2)
        self.table_frame_middle_label_5 = ttk.Label(self.table_frame_middle, text='Color', anchor='center', justify='center', width=-30)
        self.table_frame_middle_label_5.grid(column=4, row=0, sticky=(N, W, E, S), pady=2)

        self.scrolled_frame = ScrolledFrame(self.table_frame_middle, autohide=True)
        self.scrolled_frame.grid(row=1, column=0, columnspan=5, sticky=(N, S, E, W), padx=[0, 2])
        self.scrolled_frame.columnconfigure(0, weight=1)
        self.scrolled_frame.columnconfigure(1, weight=1)
        self.scrolled_frame.columnconfigure(2, weight=1)
        self.scrolled_frame.columnconfigure(3, weight=1)
        self.scrolled_frame.columnconfigure(4, weight=1)
        self.scrolled_frame.rowconfigure(0, weight=1)

        self.update_table()
        
        # Table bottom subframe
        self.table_frame_bottom = ttk.Frame(self.table_frame) 
        self.table_frame_bottom.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        self.table_frame_bottom.columnconfigure(0, weight=1)
        self.table_frame_bottom.rowconfigure(0, weight=1)
        self.table_frame_bottom.grid_propagate(0)
        
        self.table_frame_bottom_label = ttk.Label(self.table_frame_bottom, textvariable=self.message, anchor='center', justify='center')
        self.table_frame_bottom_label.grid(column=0, row=0, sticky=(W, E, S, N))
        
    def view_widgets(self):
        self.view_frame = ttk.Frame(self.resonance_right_notebook)
        self.resonance_right_notebook.add(self.view_frame, text='Physics')
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.rowconfigure(0, weight=2)
        self.view_frame.rowconfigure(1, weight=18)
        self.view_frame.rowconfigure(2, weight=18)
        self.view_frame.rowconfigure(3, weight=2)
        self.view_frame.grid_propagate(0)
        
        # Table top subframe
        self.view_frame_top = ttk.Frame(self.view_frame)
        self.view_frame_top.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)      
        self.view_frame_top.columnconfigure(0, weight=1)
        self.view_frame_top.columnconfigure(1, weight=1)
        self.view_frame_top.rowconfigure(0, weight=1)
        self.view_frame_top.grid_propagate(0)

        self.view_frame_top_flow = ttk.Button(self.view_frame_top, text='Flow', style='primary.Outline.TButton')
        self.view_frame_top_flow.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top_flow.bind('<Button-1>', lambda event, x=True: self.change_physic(x))
        self.view_frame_top_pressure = ttk.Button(self.view_frame_top, text='Pressure', style='primary.Outline.TButton')
        self.view_frame_top_pressure.grid(column=1, row=0, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_top_pressure.bind('<Button-1>', lambda event, x=False: self.change_physic(x))
        
        # Table middle subframe
        self.view_frame_middle = ttk.Frame(self.view_frame)
        self.view_frame_middle.grid(column=0, row=1, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_middle.columnconfigure(0, weight=1)
        self.view_frame_middle.rowconfigure(0, weight=1)
        self.view_frame_middle.grid_propagate(0)
        
        self.plot()
            
        self.view_frame_middle_geometry = ttk.Frame(self.view_frame)
        self.view_frame_middle_geometry.grid(column=0, row=2, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_middle_geometry.columnconfigure(0, weight=1)
        self.view_frame_middle_geometry.rowconfigure(0, weight=1)
        self.view_frame_middle_geometry.grid_propagate(0)
        
        self.plot_geometry()

        # Table bottom subframe
        self.view_frame_bottom = ttk.Frame(self.view_frame)
        self.view_frame_bottom.grid(column=0, row=3, sticky=(N, W, E, S), padx=2, pady=2)
        self.view_frame_bottom.columnconfigure(0, weight=1)
        self.view_frame_bottom.rowconfigure(0, weight=1)
        self.view_frame_bottom.grid_propagate(0)
        
        self.display_enable_buttons()

    def update_table(self, x=None):
        self.number_peaks = int(self.table_frame_top_number_peaks.get())
        
        for widget in self.scrolled_frame.winfo_children():
            widget.destroy()
        
        # Table middle subframe
        for i in range(len(self.simulation_notes) * self.number_peaks + 2):
            self.scrolled_frame.rowconfigure(i, weight=1)
        self.scrolled_frame.grid_propagate(0)
        
        self.entries = []
        for j, elem in enumerate(self.simulation_notes):
            for i in range(self.number_peaks):
                name = f'{elem}-p{i + 1}'
                frec = round(self.res_f[elem][i], 2)
                if self.table_info[elem][1][i] > 0:
                    pitch = f'{self.table_info[elem][2][i]} +{int(self.table_info[elem][1][i])}'
                else:
                    pitch = f'{self.table_info[elem][2][i]} {int(self.table_info[elem][1][i])}'
                Q = int(self.res_Q[elem][i])
                self.entries.append([name, frec, pitch, Q])
        
        for i, elem in enumerate(self.entries):
            ttk.Label(self.scrolled_frame, text=elem[0], anchor='center', justify='center', width=5).grid(column=0, row=i + 1, sticky=(W, E), padx=2, pady=2)
            ttk.Label(self.scrolled_frame, text=elem[1], anchor='center', justify='center', width=5).grid(column=1, row=i + 1, sticky=(W, E), padx=2, pady=2)
            ttk.Label(self.scrolled_frame, text=elem[2], anchor='center', justify='center', width=5).grid(column=2, row=i + 1, sticky=(W, E), padx=2, pady=2)
            ttk.Label(self.scrolled_frame, text=elem[3], anchor='center', justify='center', width=5).grid(column=3, row=i + 1, sticky=(W, E), padx=2, pady=2)
            if len(self.notes) == len(self.simulation_notes):
                    entry = Frame(self.scrolled_frame, width=7)
                    entry.grid(column=4, row=i + 1, sticky=(N, S, W, E), padx=[10, 20], pady=5)
                    entry.columnconfigure(0, weight=1)
                    entry.rowconfigure(0, weight=1)
                    entry.config(bg=self.colors[i])
            else:
                for k in range(len(self.notes)):
                    if self.notes[k] == self.simulation_notes[0]:
                        for j in range(self.number_peaks):
                            entry = Frame(self.scrolled_frame, width=7)
                            entry.grid(column=4, row=j + 1, sticky=(N, S, W, E), padx=[10, 20], pady=5)
                            entry.columnconfigure(0, weight=1)
                            entry.rowconfigure(0, weight=1)
                            entry.config(bg=self.colors[(self.number_peaks * k) + j])
                        
        
        if self.view_frame_middle:
            self.display_enable_buttons()
            self.plot()
            self.parent.forget(3)
            self.new_inharmonicity_frame = inharmonicity(root=self.root, style=self.style, parent=self.parent, instrument=self.instrument,
                res_f=self.res_f, table_info=self.table_info, simulation_notes=self.simulation_notes, notes=self.notes,
                number_peaks=self.number_peaks)
            self.parent.add(self.new_inharmonicity_frame.inharmo_frame, text='Inharmonicity')
        else:
            self.new_inharmonicity_frame = inharmonicity(root=self.root, style=self.style, parent=self.parent, instrument=self.instrument,
                res_f=self.res_f, table_info=self.table_info, simulation_notes=self.simulation_notes, notes=self.notes,
                number_peaks=self.number_peaks)
            self.parent.add(self.new_inharmonicity_frame.inharmo_frame, text='Inharmonicity')

            
    def display_enable_buttons(self):
        self.number_peaks = int(self.table_frame_top_number_peaks.get())
        
        self.to_plot_notes = [True] * (len(self.notes) * self.number_peaks)
        
        if len(self.notes) == len(self.simulation_notes):
            self.enable_notes = [True] * (len(self.notes) * self.number_peaks)
        else:
            self.enable_notes = [False] * (len(self.notes) * self.number_peaks)
            for i in range(len(self.notes)):
                if self.notes[i] == self.simulation_notes[0]:
                    for j in range(self.number_peaks):
                        self.enable_notes[self.number_peaks * i + j] = True
                    
        
        
        for i in range(len(self.notes) + 1):
            self.view_frame_bottom.columnconfigure(2 * i, weight=1)
            if i == len(self.notes):
                self.view_frame_bottom.columnconfigure(2 * i + 1, weight=2)
            else:
                self.view_frame_bottom.columnconfigure(2 * i + 1, weight=1)
        self.view_frame_bottom.rowconfigure(0, weight=1)
        self.view_frame_bottom.grid_propagate(0)
        
        
        self.view_frame_bottom_frame_subframes = list()
        for i in range(len(self.notes)):
            self.view_frame_bottom_label = ttk.Label(self.view_frame_bottom, text=f'{self.notes[i]}:', anchor='center', justify='center', font=('Helvetica', 8))
            self.view_frame_bottom_label.grid(column=2 * i + 1, row=0, sticky=(E, S, N), pady=2)
            self.view_frame_bottom_label.bind('<Button-1>', lambda event, x= self.number_peaks * i: self.change_plot_note(x))
            self.view_frame_bottom_frame= Frame(self.view_frame_bottom, width=32)
            self.view_frame_bottom_frame.grid(column=2 * i + 2, row=0, sticky=(W, E, S, N), pady=5)
            self.view_frame_bottom_frame.rowconfigure(0, weight=1)
            self.view_frame_bottom_frame.grid_propagate(0)
            for j in range(self.number_peaks):
                self.view_frame_bottom_frame.columnconfigure(j, weight=1)
                self.view_frame_bottom_frame_subframe = Frame(self.view_frame_bottom_frame, width=8, highlightthickness=1)
                self.view_frame_bottom_frame_subframe.grid(column=j, row=0, sticky=(W, E, S, N))
                self.view_frame_bottom_frame_subframe.columnconfigure(0, weight=1)
                self.view_frame_bottom_frame_subframe.rowconfigure(0, weight=1)
                if self.enable_notes[self.number_peaks * i + j]:
                    self.view_frame_bottom_frame_subframe.configure(background=self.colors[self.number_peaks * i + j], 
                        highlightbackground=self.colors[self.number_peaks * i + j])
                else:
                    self.view_frame_bottom_frame_subframe.configure(background='#FFFFFF', highlightbackground=self.colors[self.number_peaks * i + j])
                self.view_frame_bottom_frame_subframe.bind('<Button-1>', lambda event, x=self.number_peaks*i + j: self.change_plot(x))
                self.view_frame_bottom_frame_subframe.bind('<Button-3>', lambda event, x=self.number_peaks*i + j: self.change_plot_single(x))
                self.view_frame_bottom_frame_subframes.append(self.view_frame_bottom_frame_subframe)
    
    def plot_geometry(self):
        plt.close()
        self.geometry_figure = plt.figure(figsize=(1, 1), dpi=100)
        position = [0, 0, 0.5, 1]
        gs = gridspec.GridSpec(1, 1)
        gs.tight_layout(self.view_figure, rect=position)
        
        if len(self.notes) == len(self.simulation_notes):
            if any(self.single_note_display):
                for i in range(len(self.single_note_display)):
                    if self.single_note_display[i]:
                        note = self.notes[i]
                        break
                    
                self.instrument.plot_InstrumentGeometry(figure=self.geometry_figure, double_plot=True, note=note)
                ax = self.geometry_figure.get_axes()
                for axe in ax:
                    axe.grid()
                    
                ax[1].remove()
                ax[0].set_position(gs[0].get_position(self.geometry_figure))
                
                for line in ax[0].lines:
                    line.set_color('black')
                    line.set_linewidth(1)
                    line.set_alpha(0.5)
                
                poligons = ax[0].findobj(plt.Polygon)
                
                for poligon in poligons:
                    poligon.set_color('black')
                    poligon.set_alpha(0.5)
            else:
                self.instrument.plot_InstrumentGeometry(figure=self.geometry_figure, double_plot=True)
                ax = self.geometry_figure.get_axes()
                for axe in ax:
                    axe.grid()
                
                ax[1].remove()
                ax[0].set_position(gs[0].get_position(self.geometry_figure))
                
                for line in ax[0].lines:
                    line.set_color('black')
                    line.set_linewidth(1)
                    line.set_alpha(0.5)
        else:
            self.instrument.plot_InstrumentGeometry(figure=self.geometry_figure, double_plot=True, note=self.simulation_notes[0])
            ax = self.geometry_figure.get_axes()
            for axe in ax:
                axe.grid()
                
            ax[1].remove()
            ax[0].set_position(gs[0].get_position(self.geometry_figure))
            
            for line in ax[0].lines:
                line.set_color('black')
                line.set_linewidth(1)
            
            poligons = ax[0].findobj(plt.Polygon)
            
            for poligon in poligons:
                poligon.set_color('black')
                
        # Create canvas with figure
        canvas = FigureCanvasTkAgg(self.geometry_figure, self.view_frame_middle_geometry)
        canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, W, E, S), pady=10)

    def plot(self):
        plt.close()
        self.view_figure = plt.figure(figsize=(1, 1), dpi=100)
        position = [0, 0, 0.5, 1]
        gs = gridspec.GridSpec(1, 1)
        gs.tight_layout(self.view_figure, rect=position)
        peaks = int(self.table_frame_top_number_peaks.get())
        if len(self.notes) == len(self.simulation_notes):
            for i, note in enumerate(self.simulation_notes):
                for j in range(peaks):
                    if self.to_plot_notes[peaks * i + j] == True:
                        if self.flow:
                            plt.plot(self.position[note] * 1000, np.abs(np.real(self.res_flow[note][0][j])), label=f'{note}-p{j + 1}', color=self.colors[peaks * i + j])
                        else:
                            plt.plot(self.position[note] * 1000, np.abs(np.real(self.res_pressure[note][0][j])), label=f'{note}-p{j + 1}', color=self.colors[peaks * i + j])
        else:
            for i in range(len(self.notes)):
                if self.notes[i] == self.simulation_notes[0]:
                    for j in range(peaks):
                        color = self.colors[peaks * i + j]
                        if self.flow:
                            if self.to_plot_notes[peaks * i + j] == True:
                                plt.plot(self.position[self.simulation_notes[0]] * 1000, np.abs(np.real(self.res_flow[self.simulation_notes[0]][0][j])), 
                                    label=f'{self.simulation_notes[0]}-p{j + 1}', color=self.colors[peaks * i + j])
                        else:
                            if self.to_plot_notes[peaks * i + j] == True:
                                plt.plot(self.position[self.simulation_notes[0]] * 1000, np.abs(np.real(self.res_pressure[self.simulation_notes[0]][0][j])),
                                    label=f'{self.simulation_notes[0]}-p{j + 1}', color=self.colors[peaks * i + j])

            
        if self.flow:
            plt.title('Flow v/s position')
            plt.ylabel('|Flow / Flow max| %')
        else:
            plt.title('Pressure v/s position')
            plt.ylabel('|Pressure / Pressure max| %')
        plt.grid()
        
        # Create canvas with figure
        canvas = FigureCanvasTkAgg(self.view_figure, self.view_frame_middle)
        canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, W, E, S), pady=10)
        
    def change_physic(self, flow):
        if self.flow != flow:
            self.flow = flow
            self.plot()
        
    def change_plot(self, x):
        if self.enable_notes[x] == True:
            if self.to_plot_notes[x] == True:
                self.to_plot_notes[x] = False
                self.view_frame_bottom_frame_subframes[x].configure(background='#FFFFFF')
            else:
                self.to_plot_notes[x] = True
                self.view_frame_bottom_frame_subframes[x].configure(background=self.colors[x])
            self.plot()
            self.check_single_note_display()
        
    def change_plot_single(self, x):
        if self.enable_notes[x] == True:
            self.to_plot_notes = [False] * (len(self.notes) * self.number_peaks)
            self.to_plot_notes[x] = True
            
            for i in range(len(self.notes) * self.number_peaks):
                if self.to_plot_notes[i] == True:
                    self.view_frame_bottom_frame_subframes[i].configure(background=self.colors[i])
                else:
                    self.view_frame_bottom_frame_subframes[i].configure(background='#FFFFFF')
                    
            self.plot()
            self.check_single_note_display()
            
    def change_plot_note(self, x):
        if self.enable_notes[x] == True:
            self.single_note_display = [False] * len(self.notes)
            self.single_note_display[x//self.number_peaks] = True
            self.to_plot_notes = [False] * (len(self.notes) * self.number_peaks)
            for i in range(self.number_peaks):
                self.to_plot_notes[x + i] = True
            
            for i in range(len(self.notes) * self.number_peaks):
                if self.to_plot_notes[i] == True:
                    self.view_frame_bottom_frame_subframes[i].configure(background=self.colors[i])
                else:
                    self.view_frame_bottom_frame_subframes[i].configure(background='#FFFFFF')
                    
            self.plot()
            self.plot_geometry()
    
    def check_single_note_display(self):
        single = []
        for i in range(len(self.notes)):
            active_note = False
            for j in range(self.number_peaks):
                if self.to_plot_notes[self.number_peaks * i + j] == True:
                    active_note = True
            single.append(active_note)
        
        if single != self.single_note_display:
            self.single_note_display = [False] * len(self.notes)
            self.plot_geometry()
    
    def export(self):
        print('Exporting...')
        name = self.table_frame_top_name.get()
        if name != '':
            # Create files with instrument data
            path = dirname(abspath(__file__))
            folder_path = join(path, f'{name}_resonance')
            if exists(folder_path):
                try:
                    rmtree(folder_path)
                except Exception as e:
                    print(f"Error deleting '{folder_path}': {e}")
            makedirs(folder_path)
            
            with open(join(folder_path, f'{name}_resonance.txt'), 'w') as f:
                f.write('# Resonance table\n')
                f.write('\n')
                f.write('Note-Peak Frequency (Hz) Closest pitch (cent) Quality factor\n')
                for j, elem in enumerate(self.simulation_notes):
                    for i in range(self.number_peaks):
                        name = f'{elem}-p{i + 1}'
                        frec = round(self.res_f[elem][i], 2)
                        if self.table_info[elem][1][i] > 0:
                            pitch = f'{self.table_info[elem][2][i]} +{int(self.table_info[elem][1][i])}'
                        else:
                            pitch = f'{self.table_info[elem][2][i]} {int(self.table_info[elem][1][i])}'
                        Q = int(self.res_Q[elem][i])
                        f.write (f'{name:<9}  {frec:<14}  {pitch:<20}  {Q:<14}\n')
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
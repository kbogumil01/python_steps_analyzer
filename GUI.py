from tkinter import *
from tkinter import filedialog, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib import pyplot as plt
import numpy as np

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

# stworzenie okna
def start(function):
    root = Tk()
    root.geometry("600x600")
    root.title("Analiza chodu")
    create_menu_frame(root,function)
    root.mainloop()

# opis zawartości okna
def create_menu_frame(root,function):
    menu_frame = LabelFrame(root)
    menu_frame.pack(anchor=N,ipadx=600)
    
    choose_file_button = Button(menu_frame, text="Choose path", bg="silver",
        command= lambda:choose_file(filepath_label,steps_label,function,plot_frame))
    choose_file_button.grid(column=0, row=0,sticky=NW)

    clear_plot_button= Button(menu_frame, text="Clear plot", bg='silver', 
        command = lambda: clear_plot(plot_frame, filepath_label, steps_label))
    clear_plot_button.grid(column=0, row=1,sticky=NW)

    filepath_label = Label(menu_frame, text="---")
    filepath_label.grid(column=1, row=0,sticky=NW)

    steps_label = Label(menu_frame, text='Number of steps: -')
    steps_label.grid(column=1, row=1,sticky=NW)

    plot_frame = LabelFrame(root)
    plot_frame.pack(anchor=S,ipadx=600)

# wykreslenie przebiegu w postaci plot'a pyplot
def plot_xyz(time, mag, peaks, diff,plot_frame):
    fig = Figure(figsize=(5, 5),dpi=100)

    points = np.array([time, mag]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fig, axs = plt.subplots(1, 1, sharex=True, sharey=True)

    cmap = ListedColormap(['g', 'r'])
    norm = BoundaryNorm([min(diff), 0, max(diff)], cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(diff)
    lc.set_linewidth(2)
    line = axs.add_collection(lc)
    axs.set_xlim(min(time), max(time))
    axs.set_ylim(min(mag), max(mag))

    plt.plot([time[x] for x in peaks], [mag[x] for x in peaks], "x", color='purple')  # piki
    plt.ylabel('ACCELERATION[G]')
    plt.xlabel("TIME[S]")

    figure_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(figure_canvas,plot_frame)
    toolbar.update()
    #figure_canvas.get_tk_widget().grid(column=0, row=0, sticky=NW)
    figure_canvas.get_tk_widget().pack()
    plt.close()

# wybor pliku
def choose_file(filepath_label,steps_label,function,plot_frame):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    file_dir = filedialog.askopenfilename(initialdir='.')
    
    if file_dir: # jesli nie wybrano pliku to nic sie nie dzieje 
        if file_dir[-3:]=="csv": # zabezpieczenie przed wyborem innego pliku niż csv
            Time, mag, peaks, diff_mag = function(file_dir)
            plot_xyz(Time, mag, peaks, diff_mag,plot_frame)
            filepath_label.config(text=file_dir)
            steps_label.config(text="Number of steps: "+str(len(peaks)))
        else:
            messagebox.showinfo("Uwaga", "plik niezgodny z programem!") # wyskakujące okienko z informacją

# wyczyszczenie czesci z plot'em
def clear_plot(plot, filepath_label, steps_label):
    for widget in plot.winfo_children():
        widget.destroy()

    filepath_label.config(text="---")
    steps_label.config(text="Number of steps: -")
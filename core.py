import pandas
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

from GUI import *

# wczytanie pliku csv z danymi o krokach:
def read(a,b):
    c = pandas.read_csv(a, delimiter=b)
    return c

# zmiana czasu z us na s:
def time(b,c):
    a = list(b[c])
    a.reverse()
    a = [i/1000000 for i in a] #czas w sekundach
    return a

# funkcja do stworzenia listy z danymi z każdej osi akcelerometru
def x_y_z(b,c):
    a = list(b[c])
    a = [i.replace(',', '.') for i in a]
    a = [float(i) for i in a]
    return a

# obliczenie wektora magnitude, wypadkowej z każdej osi aby wykrywać zmiany niezależnie od kierunku
def magnitude(x,y,z):
    a = [(x[i]**2+y[i]**2+z[i]**2)**(0.5) for i in range(len(x))]
    a = [i/9.81 for i in a] #normalizacja do G
    return a

# wydobycie częstotliwości próbkowania:
def calculate_samp_freq(time):
    sfreq=1/np.mean(np.diff(time))
    return sfreq

# filtr dolnoprzepustowy:
def low_pass_filter(sfreq,mag):
    critical_freq=sfreq/5
    filter_freq=critical_freq/(sfreq/2)
    b,a= butter(4, filter_freq, btype='lowpass')
    mag=filtfilt(b,a,mag)
    return mag

# wyszukanie peaków do zliczania kroków
def peak_finder(mag):
    peaks,_= find_peaks(mag,1.4)
    return peaks

# obliczenie różniczki aby móc rozróżnić wykrok od podporu
def differential_mag(mag):
    diff_mag=np.diff(mag)
    diff_mag=diff_mag.tolist()
    return diff_mag

# funkcja scalająca wszystkie poprzednie:
def make_graph(path):
    df = read(path, ';')
    Time = time(df, "Time")
    x = x_y_z(df, "Sensor1")
    y = x_y_z(df, "Sensor2")
    z = x_y_z(df, "Sensor3")

    mag = magnitude(x, y, z)

    sfreq = calculate_samp_freq(Time)

    mag = low_pass_filter(sfreq, mag)

    peaks = peak_finder(mag)

    diff_mag = differential_mag(mag)

    return Time, mag, peaks, diff_mag




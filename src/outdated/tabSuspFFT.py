#my_first_plot.py
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd

import src.programTools as ncuTools


def suspFFT(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    sensor_data_a = data['LVDTFL']
    sensor_data_b = data['LVDTFR']
    sensor_data_c = data['LVDTRL']
    sensor_data_d = data['LVDTRR']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    cutFs=5

    filteredsignal_a = ncuTools.bandPassFilter(sensor_data_a, cutf=cutFs, order = 5)
    filteredsignal_b = ncuTools.bandPassFilter(sensor_data_b, cutf=cutFs, order = 5)
    filteredsignal_c = ncuTools.bandPassFilter(sensor_data_c, cutf=cutFs, order = 5)
    filteredsignal_d = ncuTools.bandPassFilter(sensor_data_d, cutf=cutFs, order = 5)

    sensor_data_a = ncuTools.mapDouble(sensor_data_a, 0.59, 0.65, 206, 196)
    sensor_data_b = ncuTools.mapDouble(sensor_data_b, 0.9, 0.94, 206, 196)
    sensor_data_c = ncuTools.mapDouble(sensor_data_c, 0.92, 1.02, 221, 216)
    sensor_data_d = ncuTools.mapDouble(sensor_data_d, 0.76, 0.8, 221, 216)

    filteredsignal_a = ncuTools.mapDouble(filteredsignal_a, 0.59, 0.65, 206, 196)
    filteredsignal_b = ncuTools.mapDouble(filteredsignal_b, 0.9, 0.94, 206, 196)
    filteredsignal_c = ncuTools.mapDouble(filteredsignal_c, 0.92, 1.02, 221, 216)
    filteredsignal_d = ncuTools.mapDouble(filteredsignal_d, 0.76, 0.8, 221, 216)


    p1 = figure(title = 'LVDT FL FFT',
               x_axis_label = 'Hz', y_axis_label = 'dB', toolbar_location="left",
               tools=graphTools, output_backend=renderer,
               tooltips=TOOLTIPS)
    p2 = figure(title = 'LVDT FR FFT',
               x_axis_label = 'Hz', y_axis_label = 'dB', toolbar_location="left",
               tools=graphTools, output_backend=renderer,
               tooltips=TOOLTIPS)
    p3 = figure(title = 'LVDT RL FFT',
               x_axis_label = 'Hz', y_axis_label = 'dB', toolbar_location="left",
               tools=graphTools, output_backend=renderer,
               tooltips=TOOLTIPS)
    p4 = figure(title = 'LVDT RR FFT',
               x_axis_label = 'Hz', y_axis_label = 'dB', toolbar_location="left",
               tools=graphTools, output_backend=renderer,
               tooltips=TOOLTIPS)

    y_overlimit = 0.05  # show y axis below and above y min and max value
    cutFsPlot = 10
    # FIRST AXIS
    x_axis, y_axis = ncuTools.dbfft(sensor_time, sensor_data_a)
    g = p1.line(x_axis, ncuTools.bandPassFilter(y_axis, cutf=cutFsPlot, order=5), color='blue')

    # FIRST AXIS
    x_axis, y_axis = ncuTools.dbfft(sensor_time, sensor_data_b)
    g1 = p2.line(x_axis, ncuTools.bandPassFilter(y_axis, cutf=cutFsPlot, order=5), color='red')

    # FIRST AXIS
    x_axis, y_axis = ncuTools.dbfft(sensor_time, sensor_data_c)
    g2 = p3.line(x_axis, ncuTools.bandPassFilter(y_axis, cutf=cutFsPlot, order=5), color='orange')

    # FIRST AXIS
    x_axis, y_axis = ncuTools.dbfft(sensor_time, sensor_data_d)
    g3 = p4.line(x_axis, ncuTools.bandPassFilter(y_axis, cutf=cutFsPlot, order=5), color='green')

    grid = gridplot([[p1, p2], [p3, p4]], plot_width=700, plot_height=325, merge_tools=True, toolbar_location='left')

    #grid.toolbar.logo = None

    l1 = layout(grid)
    tab = Panel(child=l1, title="Suspension FFT", closable=True)
    return tab

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
import scipy.special
import src.programTools as ncuTools

def suspHisto(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    FrontMotionRatio = 1.05
    RearMotionRatio = 0.98

    sensor_data_a = data['LVDTFL']
    sensor_data_b = data['LVDTFR']
    sensor_data_c = data['LVDTRL']
    sensor_data_d = data['LVDTRR']
    sensor_data_e = data['Speed(Km/h)']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    cutFs=1/0.08

    filteredsignal_a = ncuTools.bandPassFilter(sensor_data_a, cutf=cutFs, order = 5)
    filteredsignal_b = ncuTools.bandPassFilter(sensor_data_b, cutf=cutFs, order = 5)
    filteredsignal_c = ncuTools.bandPassFilter(sensor_data_c, cutf=cutFs, order = 5)
    filteredsignal_d = ncuTools.bandPassFilter(sensor_data_d, cutf=cutFs, order = 5)

    sensor_data_a = ncuTools.mapDouble(sensor_data_a, 0.59, 0.65, 206, 196)   * FrontMotionRatio
    sensor_data_b = ncuTools.mapDouble(sensor_data_b, 0.9, 0.94, 206, 196)    * FrontMotionRatio
    sensor_data_c = ncuTools.mapDouble(sensor_data_c, 0.92, 1.02, 221, 216)   * RearMotionRatio 
    sensor_data_d = ncuTools.mapDouble(sensor_data_d, 0.76, 0.8, 221, 216)    * RearMotionRatio 

    #filteredsignal_a = ncuTools.mapDouble(filteredsignal_a, 0.59, 0.65, 206, 196)
    #filteredsignal_b = ncuTools.mapDouble(filteredsignal_b, 0.9, 0.94, 206, 196)
    #filteredsignal_c = ncuTools.mapDouble(filteredsignal_c, 0.92, 1.02, 221, 216)
    #filteredsignal_d = ncuTools.mapDouble(filteredsignal_d, 0.76, 0.8, 221, 216)

    diffdata_a = np.diff(sensor_data_a) / np.diff(sensor_time)
    diffdata_b = np.diff(sensor_data_b) / np.diff(sensor_time)
    diffdata_c = np.diff(sensor_data_c) / np.diff(sensor_time)
    diffdata_d = np.diff(sensor_data_d) / np.diff(sensor_time)

    diffdata_a = ncuTools.bandPassFilter(diffdata_a, cutf=cutFs, order=5)
    diffdata_b = ncuTools.bandPassFilter(diffdata_b, cutf=cutFs, order=5)
    diffdata_c = ncuTools.bandPassFilter(diffdata_c, cutf=cutFs, order=5)
    diffdata_d = ncuTools.bandPassFilter(diffdata_d, cutf=cutFs, order=5)

    p1 = figure(title = 'LVDT FL DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)
    p2 = figure(title = 'LVDT FR DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)
    p3 = figure(title = 'LVDT RL DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)
    p4 = figure(title = 'LVDT RR DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)

    # Normal Distribution
    hist_a, edges_a = np.histogram(diffdata_a, density=True, bins='auto')
    hist_b, edges_b = np.histogram(diffdata_b, density=True, bins='auto')
    hist_c, edges_c = np.histogram(diffdata_c, density=True, bins='auto')
    hist_d, edges_d = np.histogram(diffdata_d, density=True, bins='auto')

    p1.quad(top=hist_a, bottom=0, left=edges_a[:-1], right=edges_a[1:], fill_color="blue", line_color="blue")
    p2.quad(top=hist_b, bottom=0, left=edges_b[:-1], right=edges_b[1:], fill_color="red", line_color="red")
    p3.quad(top=hist_c, bottom=0, left=edges_c[:-1], right=edges_c[1:], fill_color="orange", line_color="orange")
    p4.quad(top=hist_d, bottom=0, left=edges_d[:-1], right=edges_d[1:], fill_color="green", line_color="green")

    #p1.x_range= Range1d(-300, 300)
    #p2.x_range = Range1d(-300, 300)
    #p3.x_range = Range1d(-300, 300)
    #p4.x_range = Range1d(-300, 300)

    p1.y_range.start = 0
    p2.y_range.start = 0
    p3.y_range.start = 0
    p4.y_range.start = 0

    grid = gridplot([[p1, p2], [p3, p4]], plot_width=700, plot_height=325, merge_tools = True, toolbar_location  = 'left')

    l1 = layout(grid)

    tab = Panel(child=l1, title="Suspension Histogram", closable=True)

    return tab

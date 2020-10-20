#my_first_plot.py
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.models.layouts import Box

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd
#import pandas as pd

import src.programTools as ncuTools

def TK(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]
    renderer = 'webgl'
    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    sensor_data = data['TKFL']
    sensor_data_b = data['TKFR']
    sensor_data_c = data['TKRL']
    sensor_data_d = data['TKRR']
    sensor_data_e = data['Speed(Km/h)']
    sensor_data_f = data['BrakePressure(bar)']
    sensor_data_g = data['GForceLat'] #LONGITUDINAL!

    sensor_data = pd.to_numeric(sensor_data)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_f = pd.to_numeric(sensor_data_f)*10
    sensor_data_g = pd.to_numeric(sensor_data_g)

    cutFs = 5
    filteredsignal_g = ncuTools.bandPassFilter(sensor_data_g, cutf=cutFs, order = 5)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    p = figure(title = 'Brakes Thermocouple',
               x_axis_label = 's', y_axis_label = '°C', toolbar_location="left",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )
    p1 = figure(title = 'Speed and Brakes',
               x_axis_label = 's', y_axis_label = 'G', toolbar_location="left",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               x_range=p.x_range)

    y_overlimit = 0.1  # show y axis below and above y min and max value
    # FIRST AXIS
    p.y_range = Range1d(
        sensor_data.min() * (1 - y_overlimit), sensor_data.max() * (1 + y_overlimit)
    )
    p.extra_y_ranges = {"b": Range1d(
        sensor_data_e.min() * (1 - y_overlimit), sensor_data_e.max() * (1 + y_overlimit)
    )}
    # Adding the second axis to the plot.
    p.add_layout(LinearAxis(y_range_name="b", axis_label="BAR"), 'right')

    p1.y_range = Range1d(
        filteredsignal_g.min() * (1 - y_overlimit), filteredsignal_g.max() * (1 + y_overlimit)
    )
    p1.extra_y_ranges = {"b": Range1d(
        sensor_data_f.min() * (1 - y_overlimit), sensor_data_f.max() * (1 + y_overlimit)
    )}
    # Adding the second axis to the plot.
    p1.add_layout(LinearAxis(y_range_name="b", axis_label="BAR"), 'right')

    g1 = p.line(sensor_time, sensor_data, color='blue', line_width=2)
    g2 = p.line(sensor_time, sensor_data_b, color='red', line_width=2)
    g3 = p.line(sensor_time, sensor_data_c, color='orange', line_width=2)
    g4 = p.line(sensor_time, sensor_data_d, color='green', line_width=2)

    g6 = p.line(sensor_time, sensor_data_e, color='purple', y_range_name="b", line_width=2, alpha=0.5)

    g5 = p1.line(sensor_time, filteredsignal_g, color='green', line_width=2)
    g7 = p1.line(sensor_time, sensor_data_f, color='red', y_range_name="b", line_width=2)

    legend = Legend(items=[
        ("2Hz TKFL @NCU", [g1]),
        ("2Hz TKFR @NCU", [g2]),
        ("2Hz TKRL @NCU", [g3]),
        ("2Hz TKRR @NCU", [g4]),
        ("35Hz Speed @MOTEC", [g6]),
    ], location=(0,0))
    legend1 = Legend(items=[
        ('5Hz Low Pass Filter Y axis MPU6050 @NCU', [g5]),
        ("35Hz Brake Pressure @MOTEC", [g7])
    ], location=(0,0))

    p.add_layout(legend, 'right')
    p1.add_layout(legend1, 'right')

    p.legend.click_policy = 'hide'
    p1.legend.click_policy='hide'

    p.toolbar.logo = None
    p1.toolbar.logo = None

    grid = gridplot([[p], [p1]], plot_width=1450, plot_height=325, merge_tools=True, toolbar_location='left')

    l1 = layout(grid)
    tab = Panel(child=l1, title="Brakes", closable=True)
    return tab

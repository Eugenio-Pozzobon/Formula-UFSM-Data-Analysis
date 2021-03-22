#my_first_plot.pyfrom bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models.layouts import Box
from bokeh.plotting import figure, output_file

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd
import dask.dataframe as dd

import src.programTools as ncuTools

def engine(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'
    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'
    sensor_data_a = data['RPM']
    sensor_data_b = data['Speed']
    sensor_data_c = data['TPS']
    sensor_data_d = data['Gear']
    sensor_data_e = data['MAP']
    sensor_data_f = data['FuelPressure']
    sensor_data_g = data['OilPressure']
    sensor_data_h = data['Lambda']
    sensor_data_i = data['OilTemp']
    sensor_data_j = data['AirTemp']
    sensor_data_k = data['EngineTemp']
    sensor_data_l = data['RadOutTemp']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_f = pd.to_numeric(sensor_data_f)
    sensor_data_g = pd.to_numeric(sensor_data_g)
    sensor_data_h = pd.to_numeric(sensor_data_h)
    sensor_data_i = pd.to_numeric(sensor_data_i)
    sensor_data_j = pd.to_numeric(sensor_data_j)
    sensor_data_k = pd.to_numeric(sensor_data_k)
    sensor_data_l = pd.to_numeric(sensor_data_l)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000
    cutFs=5

    p = figure(title = 'Engine Basics',
               x_axis_label = 's', y_axis_label = 'rpm', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )
    p1 = figure(title = 'Intake',
               x_axis_label = 's', y_axis_label = '', toolbar_location="below",
               tooltips=TOOLTIPS,
               x_range=p.x_range,
               output_backend=renderer,
               tools=graphTools,
               )
    p2 = figure(title='Pressure',
                x_axis_label='s', y_axis_label='bar', toolbar_location="below",
                tooltips=TOOLTIPS,
                x_range=p.x_range,
                output_backend=renderer,
                tools=graphTools,
                )

    p3 = figure(title='Temperature', plot_width = 1500, plot_height = 300,
                x_axis_label='s', y_axis_label='°C', toolbar_location="below",
                tooltips=TOOLTIPS,
                x_range=p.x_range,
                output_backend=renderer,
                tools=graphTools,
                )
    p4 = figure(title='Lambda', plot_width = 1500, plot_height = 300,
                x_axis_label='s', y_axis_label='', toolbar_location="below",
                tooltips=TOOLTIPS,
                output_backend=renderer,
                tools=graphTools,
                )

    p5 = figure(title='Gear', plot_width = 1500, plot_height = 300,
                x_axis_label='s', y_axis_label='', toolbar_location="below",
                tooltips=TOOLTIPS,
                output_backend=renderer,
                tools=graphTools,
                )
    y_overlimit = 0.05  # show y axis below and above y min and max value
    # FIRST AXIS
    p.y_range = Range1d(
        sensor_data_a.min() * (1 - y_overlimit), sensor_data_a.max() * (1 + y_overlimit)
    )

    p.extra_y_ranges = {"b": Range1d(
        sensor_data_b.min() * (1 - y_overlimit), sensor_data_b.max() * (1 + y_overlimit)
    )}
    p.add_layout(LinearAxis(y_range_name="b", axis_label="Speed (km/k)"), 'right')

    p1.y_range = Range1d(0,100)
    p2.y_range = Range1d(0,10)
    p3.y_range = Range1d(20, 125)
    p4.y_range = Range1d(0, 2)
    p5.y_range = Range1d(0, 6)

    g1 = p.line(sensor_time, sensor_data_a, color='red', line_width=2)

    g2 = p.line(sensor_time, sensor_data_b, color='blue', line_width=1, alpha=0.7, y_range_name = "b")

    g3 = p1.line(sensor_time, sensor_data_c, color='green', line_width=2)
    g4 = p1.line(sensor_time, sensor_data_e, color='blue', line_width=2)

    g5 = p2.line(sensor_time, sensor_data_f, color='purple', line_width=2)
    g6 = p2.line(sensor_time, sensor_data_g, color='orange', line_width=2)

    g7 = p3.line(sensor_time, sensor_data_i, color='blue', line_width=2)
    g8 = p3.line(sensor_time, sensor_data_j, color='yellow', line_width=2)
    g9 = p3.line(sensor_time, sensor_data_k, color='green', line_width=2)
    g10 = p3.line(sensor_time, sensor_data_l, color='purple', line_width=2)

    g11 = p4.line(sensor_time, sensor_data_h, color='red', line_width=2)

    g12 = p5.line(sensor_time, sensor_data_d, color='purple', line_width=2)

    legend = Legend(items=[
        ('35Hz RPM @MOTEC', [g1]),
        ('35Hz SPEED @MOTEC', [g2]),
    ], location=(0,0))
    legend1 = Legend(items=[
        ('35Hz TPS(%) @MOTEC', [g3]),
        ('35Hz MAP(kpa) @MOTEC', [g4]),
    ], location=(0,0))
    legend2 = Legend(items=[
        ('35Hz FuelPressure(bar) @MOTEC', [g5]),
        ('35Hz OilPressure(bar) @MOTEC', [g6]),
    ], location=(0,0))
    legend3 = Legend(items=[
        ('35Hz OilTemp(C) @MOTEC', [g7]),
        ('35Hz AirTemp(C) @MOTEC', [g8]),
        ('35Hz EngineTemp(C) @MOTEC', [g9]),
        ('35Hz RadOutTemp(C) @MOTEC', [g10]),
    ], location=(0, 0))
    legend4 = Legend(items=[
        ('35Hz Lambda @MOTEC', [g11]),
    ], location=(0, 0))
    legend5 = Legend(items=[
        ('35Hz Gear @MOTEC', [g12]),
    ], location=(0, 0))

    p.add_layout(legend, 'right')
    p1.add_layout(legend1, 'right')
    p2.add_layout(legend2, 'right')
    p3.add_layout(legend3, 'right')
    p4.add_layout(legend4, 'right')
    p5.add_layout(legend5, 'right')

    p.legend.click_policy = 'hide'
    p1.legend.click_policy = 'hide'
    p2.legend.click_policy = 'hide'
    p3.legend.click_policy = 'hide'
    p4.legend.click_policy = 'hide'
    p5.legend.click_policy = 'hide'

    p.toolbar.logo = None
    p1.toolbar.logo = None
    p2.toolbar.logo = None
    p3.toolbar.logo = None
    p4.toolbar.logo = None
    p5.toolbar.logo = None

    grid = gridplot([[p], [p1], [p2], [p3], [p4], [p5]], plot_width=1450, plot_height=300, merge_tools=True, toolbar_location='left')

    l1 = layout(grid)

    tab = Panel(child=l1, title="Engine", closable=True)

    return tab

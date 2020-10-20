#my_first_plot.py
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
from bokeh.models import CustomJS, RangeSlider, TextAreaInput, Slider
from bokeh.models.layouts import Box

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd
import dask.dataframe as dd

import src.programTools as ncuTools


def BAT(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    sensor_data = data['A_9_map']
    sensor_data_b = data['BatteryVoltage(V)']
    sensor_data_c = data['RPM']
    sensor_data_d = data['EngineTemp(C)']
    sensor_data_e = data['Speed(Km/h)']

    sensor_data = pd.to_numeric(sensor_data)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    halfFan=pd.DataFrame(data, columns=['RPM','EngineTemp(C)'])
    halfFan.loc[(halfFan['RPM'] > 2000) & (halfFan['EngineTemp(C)'] > 84), 'half'] = 1
    halfFan.loc[(halfFan['RPM'] < 2000) | (halfFan['EngineTemp(C)'] < 84), 'half'] = 0

    fullFan=pd.DataFrame(data, columns=['RPM','EngineTemp(C)'])
    fullFan.loc[(fullFan['RPM'] > 2000) & (fullFan['EngineTemp(C)'] > 94), 'full'] = 1
    fullFan.loc[(fullFan['RPM'] < 2000) | (fullFan['EngineTemp(C)'] < 94), 'full'] = 0

    sensor_data_c.loc[sensor_data_c > 32.768] = sensor_data_c.loc[sensor_data_c > 32.768] - 65.536
    sensor_data_d.loc[sensor_data_d > 3276.8]= sensor_data_d.loc[sensor_data_d > 3276.8]-6553.6

    p = figure(title = 'Battery Voltage & RPM',
               x_axis_label = 's', y_axis_label = 'V', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )
    p1 = figure(title = 'Speed and Temperature',
               x_axis_label = 's', y_axis_label = 'Km/h & °C', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               x_range=p.x_range, y_range=p.y_range,
               tools=graphTools,
               )
    p2 = figure(title = 'Fan Status',
               x_axis_label = 's', y_axis_label = '', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               x_range=p.x_range, y_range=p.y_range,
               tools=graphTools,
               )
    y_overlimit = 0.05  # show y axis below and above y min and max value

    p.y_range = Range1d(
        sensor_data.min() * (1 - y_overlimit), sensor_data.max() * (1 + y_overlimit)
    )
    p.extra_y_ranges = {"b": Range1d(
        sensor_data_c.min() * (1 - y_overlimit), sensor_data_c.max() * (1 + y_overlimit)
    )}
    p.add_layout(LinearAxis(y_range_name="b", axis_label="RPM"), 'right')

    p1.y_range = Range1d(
        0, sensor_data_d.max() * (1 + y_overlimit)
    )

    p2.y_range = Range1d(
        0, 1
    )

    g1 = p.line(sensor_time, sensor_data, color='blue', line_width=2)
    g2 = p.line(sensor_time, sensor_data_b, color='orange', line_width=2)
    g3 = p.line(sensor_time, ncuTools.bandPassFilter(sensor_data), color='yellow', line_width=2)
    g4 = p.line(sensor_time, ncuTools.bandPassFilter(sensor_data_b), color='green', line_width=2)

    g5 = p.line(sensor_time, sensor_data_c, color='red', y_range_name="b", line_width=2)


    g6 = p1.line(sensor_time, sensor_data_d, color='blue', line_width=2)
    g7 = p1.line(sensor_time, sensor_data_e, color='green', line_width=2)

    g8 = p2.line(sensor_time, halfFan['half'], color='orange', line_width=2)
    g9 = p2.line(sensor_time, fullFan['full'], color='red', line_width=2)

    legend = Legend(items=[
        ("200Hz BatV @NCU", [g1]),
        ("35Hz BatV @MOTEC", [g2]),
        ("5Hz LowPass Filter @NCU", [g3]),
        ("5Hz LowPass Filter @MOTEC", [g4]),
        ("35Hz RPM", [g5])
    ], location=(0,0))

    legend1 = Legend(items=[
        ("35Hz Engine Temp°C @MOTEC", [g6]),
        ("35Hz Speed @MOTEC", [g7])
    ], location=(0,0))

    legend2 = Legend(items=[
        ("Half Fan Active", [g8]),
        ("Full Fan Active", [g9])
    ], location=(0,0))

    p.add_layout(legend, 'right')
    p1.add_layout(legend1, 'right')
    p2.add_layout(legend2, 'right')

    p.legend.click_policy = 'hide'
    p1.legend.click_policy = 'hide'
    p2.legend.click_policy='hide'

    p.toolbar.logo = None
    p1.toolbar.logo = None
    p2.toolbar.logo = None

    grid = gridplot([[p], [p2], [p1]], plot_width=1450, plot_height=250, merge_tools=True, toolbar_location='left')

    l1 = layout(grid)

    tab = Panel(child=l1, title="Battery", closable=True)

    return tab
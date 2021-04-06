#my_first_plot.py
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout
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


def ncu(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    sensor_data = data['ncuTemp']
    sensor_data_b = data['atmelTemp']
    sensor_data_c = data['sd_bps']
    sensor_data_d = data['fileSize']
    sensor_data_e = data['max_enable']

    sensor_data = pd.to_numeric(sensor_data)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    p = figure(plot_width = 1500, plot_height = 300,
               title = 'NCU Temperature',
               x_axis_label = 's', y_axis_label = '°C', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools
               )
    p1 = figure(plot_width = 1500, plot_height = 300,
               title = 'SD Info',
               x_axis_label = 's', y_axis_label = 'Byte', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               x_range=p.x_range, y_range=p.y_range,
               tools=graphTools
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    p.y_range = Range1d(
        sensor_data.min() * (1 - y_overlimit), sensor_data.max() * (1 + y_overlimit)
    )    # Setting the second y axis range name and range
    p.extra_y_ranges = {"b": Range1d(
        0,1
    )}
    # Adding the second axis to the plot.
    p.add_layout(LinearAxis(y_range_name="b", axis_label="RPM"), 'right')
    p1.y_range = Range1d(0, sensor_data_d.max() * (1 + y_overlimit))

    g1 = p.line(sensor_time, sensor_data, color='blue', line_width=2)
    g2 = p.line(sensor_time, sensor_data_b, color='orange', line_width=2)

    g5 = p.line(sensor_time, sensor_data_e, color='red', y_range_name="b", line_width=2)

    g6 = p1.line(sensor_time, sensor_data_c, color='blue', line_width=2)
    g7 = p1.line(sensor_time, sensor_data_d, color='green', line_width=2)

    legend = Legend(items=[
        ("200Hz ncuTemp @NCU", [g1]),
        ("200Hz atmelTemp @NCU", [g2]),
        ("Max Enable @NCU", [g5]),
    ], location=(0,0))
    legend1 = Legend(items=[
        ("200Hz sd_bps @NCU", [g6]),
        ("200Hz fileSize @NCU", [g7])
    ], location=(0,0))

    p.add_layout(legend, 'right')
    p1.add_layout(legend1, 'right')

    p.legend.click_policy='hide'
    p1.legend.click_policy='hide'

    p.toolbar.logo = None
    p1.toolbar.logo = None

    l1 = layout(row(column(p,p1)
                    #,wb
                    ))

    tab = Panel(child=l1, title="NCU Report", closable=True)

    return tab
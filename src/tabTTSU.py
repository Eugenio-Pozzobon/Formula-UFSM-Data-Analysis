#my_first_plot.py
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models.layouts import Box

import src.programTools as ncuTools
import random

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd
#import dask.dataframe as dd


def tireTemp(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    sensor_data = data['PneuDianteiroInner']
    sensor_data_b = data['PneuDianteiroCenter']
    sensor_data_c = data['PneuDianteiroOuter']
    sensor_data_d = data['PneuTraseiroInner']
    sensor_data_e = data['PneuTraseiroCenter']
    sensor_data_f = data['PneuTraseiroOuter']
    sensor_data_g = data['Speed(Km/h)']

    sensor_data = np.random.randint(30,40) # pd.to_numeric(sensor_data)
    sensor_data_b = np.random.randint(30,40) # pd.to_numeric(sensor_data_b)
    sensor_data_c = np.random.randint(30,40) # pd.to_numeric(sensor_data_c)
    sensor_data_d = np.random.randint(30,40) # pd.to_numeric(sensor_data_d)
    sensor_data_e = np.random.randint(30,40) # pd.to_numeric(sensor_data_e)
    sensor_data_f = np.random.randint(30,40) # pd.to_numeric(sensor_data_f)
    sensor_data_g = pd.to_numeric(sensor_data_g)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    p = figure(plot_width = 700, plot_height = 300,
               title = 'Front Tire',
               x_axis_label = 's', y_axis_label = '°C', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    p.y_range = Range1d(
        20,80
    )
    g1 = p.line(sensor_time, sensor_data, color='red', line_width=2)
    g2 = p.line(sensor_time, sensor_data_b, color='orange', line_width=2)
    g3 = p.line(sensor_time, sensor_data_c, color='green', line_width=2)

    p.extra_y_ranges = {"b": Range1d(
        sensor_data_g.min() * (1 - y_overlimit), sensor_data_g.max() * (1 + y_overlimit)
    )}
    p.add_layout(LinearAxis(y_range_name="b", axis_label="Km/h"), 'right')
    g4 = p.line(sensor_time, sensor_data_g, color='blue', alpha=0.5, line_width=2, y_range_name="b")

    legend = Legend(items=[
        ("5Hz F Inner @TTSU", [g1]),
        ("5Hz F Center @TTSU", [g2]),
        ("5Hz F Outer @TTSU", [g3]),
        ("35Hz Speed @MOTEC", [g4])
    ], location=(0,0))
    p.add_layout(legend, 'right')
    p.legend.click_policy='hide'

    pb = figure(plot_width = 700, plot_height = 300,
               title = 'Front Tire',
               x_axis_label = 's', y_axis_label = '°C', toolbar_location="below",
               tooltips=TOOLTIPS,
               #output_backend="webgl",
               tools=graphTools,
               x_range=p.x_range
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    pb.y_range = Range1d(
        -10,10
    )
    g1b = pb.line(sensor_time, sensor_data-sensor_data_b, color='red', line_width=2)
    g2b = pb.line(sensor_time, sensor_data_b-sensor_data_c, color='orange', line_width=2)
    g3b = pb.line(sensor_time, sensor_data_c-sensor_data, color='green', line_width=2)

    pb.extra_y_ranges = {"b": Range1d(
        sensor_data_g.min() * (1 - y_overlimit), sensor_data_g.max() * (1 + y_overlimit)
    )}
    pb.add_layout(LinearAxis(y_range_name="b", axis_label="Km/h"), 'right')
    g4b = pb.line(sensor_time, sensor_data_g, color='blue', alpha=0.5, line_width=2, y_range_name="b")

    legendb = Legend(items=[
        ("5Hz F Inner-Center @TTSU", [g1b]),
        ("5Hz F Center-Outer @TTSU", [g2b]),
        ("5Hz F Outer-Inner @TTSU", [g3b]),
        ("35Hz Speed @MOTEC", [g4b])
    ], location=(0,0))
    pb.add_layout(legendb, 'right')
    pb.legend.click_policy='hide'

    ##### NEW FIGURE
    p1 = figure(plot_width = 700, plot_height = 300,
               title = 'Rear Tire',
               x_axis_label = 's', y_axis_label = '°C', toolbar_location="below",
               tooltips=TOOLTIPS,
               #output_backend="webgl",
               tools=graphTools,
               x_range=p.x_range)

    # FIRST AXIS
    p1.y_range = Range1d(
        20,80
    )

    g5 = p1.line(sensor_time, sensor_data_d, color='red', line_width=2)
    g6 = p1.line(sensor_time, sensor_data_e, color='orange', line_width=2)
    g7 = p1.line(sensor_time, sensor_data_f, color='green', line_width=2)

    p1.extra_y_ranges = {"b": Range1d(
        sensor_data_g.min() * (1 - y_overlimit), sensor_data_g.max() * (1 + y_overlimit)
    )}
    # Adding the second axis to the plot.
    p1.add_layout(LinearAxis(y_range_name="b", axis_label="Km/h"), 'right')
    g8 = p1.line(sensor_time, sensor_data_g, color='blue', alpha=0.5, y_range_name="b", line_width=2)

    legend1 = Legend(items=[
        ("5Hz R Inner @TTSU", [g5]),
        ("5Hz R Center @TTSU", [g6]),
        ("5Hz R Outer @TTSU", [g7]),
        ("35Hz Speed @MOTEC", [g8])
    ], location=(0,0))

    p1.add_layout(legend1, 'right')
    p1.legend.click_policy='hide'

    p1b = figure(plot_width = 700, plot_height = 300,
               title = 'Front Tire',
               x_axis_label = 's', y_axis_label = '°C', toolbar_location="below",
               tooltips=TOOLTIPS,
               #output_backend="webgl",
               tools=graphTools,
               x_range=p.x_range,
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    p1b.y_range = Range1d(
        -10,10
    )
    g5b = p1b.line(sensor_time, sensor_data_d-sensor_data_e, color='red', line_width=2)
    g6b = p1b.line(sensor_time, sensor_data_e-sensor_data_f, color='orange', line_width=2)
    g7b = p1b.line(sensor_time, sensor_data_f-sensor_data_d, color='green', line_width=2)

    p1b.extra_y_ranges = {"b": Range1d(
        sensor_data_g.min() * (1 - y_overlimit), sensor_data_g.max() * (1 + y_overlimit)
    )}
    p1b.add_layout(LinearAxis(y_range_name="b", axis_label="Km/h"), 'right')
    g8b = p1b.line(sensor_time, sensor_data_g, color='blue', alpha=0.5, line_width=2, y_range_name="b")

    legend1b = Legend(items=[
        ("5Hz R Inner-Center @TTSU", [g5b]),
        ("5Hz R Center-Outer @TTSU", [g6b]),
        ("5Hz R Outer-Inner @TTSU", [g7b]),
        ("35Hz Speed @MOTEC", [g8b])
    ], location=(0,0))
    p1b.add_layout(legend1b, 'right')
    p1b.legend.click_policy='hide'

    p.toolbar.logo = None
    p1.toolbar.logo = None
    pb.toolbar.logo = None
    p1b.toolbar.logo = None

    l1 = layout([[p, pb],[p1,p1b]])
    tab = Panel(child=l1, title="Tire Temp Sensors", closable=True)
    return tab

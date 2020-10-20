#my_first_plot.py
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models.layouts import Box

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd
import dask.dataframe as dd

import src.programTools as ncuTools


def mpu6050(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    sensor_data_a = data['GForceLat']
    sensor_data_b = -data['GForceLong']
    sensor_data_c = -data['gyro_z']
    sensor_data_d = data['SteeringAngle(deg)']
    sensor_data_e = data['Speed(Km/h)']
    sensor_data_f = data['ECU_GForceLat(G)']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_f = pd.to_numeric(sensor_data_f)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    sensor_data_d.loc[sensor_data_d > 3276.8]= sensor_data_d.loc[sensor_data_d > 3276.8]-6553.6
    sensor_data_f.loc[sensor_data_f > 32.768] = sensor_data_f.loc[sensor_data_f > 32.768] - 65.536

    cutFs=5

    filteredsignal_a = ncuTools.bandPassFilter(sensor_data_a, cutf=cutFs, order = 5)
    filteredsignal_b = ncuTools.bandPassFilter(sensor_data_b, cutf=cutFs, order = 5)

    cutFs = 1
    filteredsignal_c = ncuTools.bandPassFilter(sensor_data_c, cutf=cutFs, order = 5)

    p = figure(plot_width = 1500, plot_height = 300,
               title = 'MPU6050',
               x_axis_label = 's', y_axis_label = 'G', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )
    p1 = figure(plot_width = 1500, plot_height = 300,
               title = 'Speed',
               x_axis_label = 's', y_axis_label = 'Speed(km/h)', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               x_range=p.x_range,
               )
    p2 = figure(plot_width = 600, plot_height = 600,
               title = 'GXxGY',
               x_axis_label = 'Gx', y_axis_label = 'Gy', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools = graphTools,
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    # FIRST AXIS
    p.y_range = Range1d(-2, 2)

    p.extra_y_ranges = {"b": Range1d(
        sensor_data_c.min() * (1 - y_overlimit), sensor_data_c.max() * (1 + y_overlimit)
    )}
    p.add_layout(LinearAxis(y_range_name="b", axis_label="Gyro(°/s)"), 'right')

    p1.y_range = Range1d(
        sensor_data_e.min() * (1 - y_overlimit), sensor_data_e.max() * (1 + y_overlimit)
    )

    p1.extra_y_ranges = {"b": Range1d(
        sensor_data_d.min() * (1 - y_overlimit), sensor_data_d.max() * (1 + y_overlimit)
    )}
    p1.add_layout(LinearAxis(y_range_name="b", axis_label="degree(°)"), 'right')

    #g1b = p.line(sensor_time, sensor_data_f, color='orange')  # X and Y axis are inverted
    #g1 = p.line(sensor_time, sensor_data_b, color='red') #X and Y axis are inverted
    #g2 = p.line(sensor_time, sensor_data_a, color='green')
    g1f = p.line(sensor_time, filteredsignal_b, color='red')  # X and Y axis are inverted
    g2f = p.line(sensor_time, filteredsignal_a, color='green')

    #g3 = p.line(sensor_time, sensor_data_c, color='yellow', y_range_name="b", line_width=2)
    g3f = p.line(sensor_time, filteredsignal_c, color='yellow', y_range_name="b", line_width=2)

    g4 = p1.line(sensor_time, sensor_data_e, color='blue', line_width=2)

    g5 = p1.line(sensor_time, sensor_data_d, color='green', y_range_name="b")

    p2.scatter(filteredsignal_b, filteredsignal_a, line_color=None)

    legend = Legend(items=[
        #('35Hz X axis Acelerometer @MOTEC', [g1b]),
        #('200Hz X axis MPU6050 @NCU', [g1]),
        #('200Hz Y axis MPU6050 @NCU', [g2]),
        #('200Hz Gyro Z axis MPU6050 @NCU', [g3]),
        ('5Hz Low Pass Filter X axis MPU6050 @NCU', [g1f]),
        ('5Hz Low Pass Filter Y axis MPU6050 @NCU', [g2f]),
        ('1Hz Low Pass Filter Gyro Z axis MPU6050 @NCU', [g3f])
    ], location=(0,0))

    legend1 = Legend(items=[
        ('35Hz Speed @MOTEC', [g4]),
        ('35Hz Steering Angle @MOTEC', [g5])
    ], location=(0,0))

    p.add_layout(legend, 'right')
    p1.add_layout(legend1, 'right')

    p.legend.click_policy='hide'
    p1.legend.click_policy = 'hide'

    p.toolbar.logo = None
    p1.toolbar.logo = None
    p2.toolbar.logo = None

    grid = gridplot([[p],[p1],[p2]], merge_tools = True, toolbar_location = 'left')

    l1 = layout(grid)

    tab = Panel(child=l1, title="3Axis Acelerometer and Gyro", closable=True)

    return tab
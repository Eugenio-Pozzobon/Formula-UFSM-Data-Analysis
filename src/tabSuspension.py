#my_first_plot.py
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models.layouts import Box

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd
import dask.dataframe as dd

import src.programTools as ncuTools


def LVDT(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]
    renderer = 'webgl'
    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    sensor_data_a = data['LVDTFL']
    sensor_data_b = data['LVDTFR']
    sensor_data_c = data['LVDTRL']
    sensor_data_d = data['LVDTRR']
    sensor_data_e = data['Speed(Km/h)']
    sensor_data_x = -data['GForceLong']
    sensor_data_y = data['GForceLat']
    sensor_data_z = data['GForceVert']
    sensor_data_tps = data['TPS']
    sensor_data_bp = data['BrakePressure(bar)']*10
    sensor_data_sa = data['SteeringAngle(deg)']


    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_sa = pd.to_numeric(sensor_data_sa)

    sensor_data_sa.loc[sensor_data_sa > 3276.8] = sensor_data_sa.loc[sensor_data_sa > 3276.8] - 6553.6

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    cutFs=12

    filteredsignal_a = ncuTools.bandPassFilter(sensor_data_a, cutf=cutFs, order = 5)
    filteredsignal_b = ncuTools.bandPassFilter(sensor_data_b, cutf=cutFs, order = 5)
    filteredsignal_c = ncuTools.bandPassFilter(sensor_data_c, cutf=cutFs, order = 5)
    filteredsignal_d = ncuTools.bandPassFilter(sensor_data_d, cutf=cutFs, order = 5)
    filteredsignal_x = ncuTools.bandPassFilter(sensor_data_x, cutf=5, order=5)
    filteredsignal_y = ncuTools.bandPassFilter(sensor_data_y, cutf=5, order = 5)
    filteredsignal_z = ncuTools.bandPassFilter(sensor_data_z, cutf=5, order = 5)

    sensor_data_a = ncuTools.mapDouble(sensor_data_a, 0.59, 0.65, 206, 196)
    sensor_data_b = ncuTools.mapDouble(sensor_data_b, 0.9 , 0.94, 206, 196)
    sensor_data_c = ncuTools.mapDouble(sensor_data_c, 0.92, 1.02, 221, 216)
    sensor_data_d = ncuTools.mapDouble(sensor_data_d, 0.76, 0.8 , 221, 216)

    filteredsignal_a = ncuTools.mapDouble(filteredsignal_a, 0.59, 0.65, 206, 196)
    filteredsignal_b = ncuTools.mapDouble(filteredsignal_b, 0.9, 0.94, 206, 196)
    filteredsignal_c = ncuTools.mapDouble(filteredsignal_c, 0.92, 1.02, 221, 216)
    filteredsignal_d = ncuTools.mapDouble(filteredsignal_d, 0.76, 0.8, 221, 216)

    diffdata_a = np.diff(sensor_data_a) / np.diff(sensor_time)
    diffdata_b = np.diff(sensor_data_b) / np.diff(sensor_time)
    diffdata_c = np.diff(sensor_data_c) / np.diff(sensor_time)
    diffdata_d = np.diff(sensor_data_d) / np.diff(sensor_time)

    diffdata_a = ncuTools.bandPassFilter(diffdata_a, cutf=cutFs, order=5)
    diffdata_b = ncuTools.bandPassFilter(diffdata_b, cutf=cutFs, order=5)
    diffdata_c = ncuTools.bandPassFilter(diffdata_c, cutf=cutFs, order=5)
    diffdata_d = ncuTools.bandPassFilter(diffdata_d, cutf=cutFs, order=5)

    altFront = filteredsignal_a/2+filteredsignal_b/2
    altRear = filteredsignal_c/2+filteredsignal_d/2

    cutFsAlt=5

    altFront = ncuTools.bandPassFilter(altFront, cutf=cutFsAlt, order=2)
    altRear =  ncuTools.bandPassFilter(altRear, cutf=cutFsAlt, order=2)

    '''
    p = figure(plot_width = 1200, plot_height = 300,
               title = 'LVDT RAW',
               x_axis_label = 's', y_axis_label = 'mm', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphtools,
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    # FIRST AXIS
    p.y_range = Range1d(
        150, 250
    )
    g1 = p.line(sensor_time, sensor_data_a, color='blue', line_width=2)
    g2 = p.line(sensor_time, sensor_data_b, color='red', line_width=2)
    g3 = p.line(sensor_time, sensor_data_c, color='yellow', line_width=2)
    g4 = p.line(sensor_time, sensor_data_d, color='green', line_width=2)

    legend = Legend(items=[
        ('200Hz LVDTFL @NCU', [g1]),
        ('200Hz LVDTFR @NCU', [g2]),
        ('200Hz LVDTRL @NCU', [g3]),
        ('200Hz LVDTRR @NCU', [g4])
    ], location=(0,0))

    p.add_layout(legend, 'right')

    p.legend.click_policy='hide'

    ##### NEW FIGURE
    '''

    p1 = figure(plot_width = 1400, plot_height = 300,
               title = 'LVDT FILTERED',
               x_axis_label = 's', y_axis_label = 'mm', toolbar_location="left",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )

    p2 = figure(plot_width = 1400, plot_height = 300,
               title = 'LVDT DUMPER',
               x_axis_label = 's', y_axis_label = 'mm/s', toolbar_location="left",
               tools=graphTools, output_backend=renderer,
               tooltips=TOOLTIPS, x_range=p1.x_range)

    p3 = figure(plot_width = 1400, plot_height = 300,
               title = 'LATERAL FORCE',
               x_axis_label = 's', y_axis_label = 'mm', toolbar_location="left",
               tools=graphTools, output_backend=renderer,
               tooltips=TOOLTIPS, x_range=p1.x_range)

    p4 = figure(plot_width = 1400, plot_height = 300,
               title = 'ACELERATION',
               x_axis_label = 's', y_axis_label = 'G', toolbar_location="left",
               tools=graphTools, output_backend=renderer,
               tooltips=TOOLTIPS, x_range=p1.x_range)

    y_overlimit = 0.05  # show y axis below and above y min and max value

    p1.y_range = Range1d(
        altFront.min() * (1 - y_overlimit), altRear.max() * (1 + y_overlimit)
    )
    p1.extra_y_ranges = {"b": Range1d(
        sensor_data_sa.min() * (1 - y_overlimit), sensor_data_sa.max() * (1 + y_overlimit)
    )}
    p1.add_layout(LinearAxis(y_range_name="b", axis_label="Speed(km/h)"), 'right')

    p2.y_range = Range1d(-1000,1000)
    p2.extra_y_ranges = {"b": Range1d(
        sensor_data_e.min() * (1 - y_overlimit), sensor_data_e.max() * (1 + y_overlimit)
    )}
    p2.add_layout(LinearAxis(y_range_name="b", axis_label="Speed(km/h)"), 'right')

    p3.extra_y_ranges = {"b": Range1d(
        sensor_data_e.min() * (1 - y_overlimit), sensor_data_e.max() * (1 + y_overlimit)
    )}
    p3.add_layout(LinearAxis(y_range_name="b", axis_label="Speed(km/h)"), 'right')

    p4.y_range = Range1d(sensor_data_x.min() * (1 - y_overlimit), sensor_data_x.max() * (1 + y_overlimit))

    p4.extra_y_ranges = {"b": Range1d(0,100)}
    p4.add_layout(LinearAxis(y_range_name="b", axis_label="TPS(%)"), 'right')
    # FIRST AXIS

    g5 = p1.line(sensor_time, filteredsignal_a, color='blue', line_width=2)
    g6 = p1.line(sensor_time, filteredsignal_b, color='red', line_width=2)
    g7 = p1.line(sensor_time, filteredsignal_c, color='orange', line_width=2)
    g8 = p1.line(sensor_time, filteredsignal_d, color='green', line_width=2)
    g9 = p1.line(sensor_time, sensor_data_sa, color='black', y_range_name = "b", alpha=0.8, line_width=2)

    g13 = p2.line(sensor_time[:-1], diffdata_a, color='blue')
    g14 = p2.line(sensor_time[:-1], diffdata_b, color='red')
    g15 = p2.line(sensor_time[:-1], diffdata_c, color='orange')
    g16 = p2.line(sensor_time[:-1], diffdata_d, color='green')

    g10 = p1.line(sensor_time, altFront, color='yellow', line_width=2)
    g11 = p1.line(sensor_time, altRear, color='purple', line_width=2)

    gx = p4.line(sensor_time, filteredsignal_x, color='blue', line_width=2)

    gy = p4.line(sensor_time, filteredsignal_y, color='purple', line_width=2)
    gz = p4.line(sensor_time, filteredsignal_z, color='orange' , line_width=2)

    gtps = p4.line(sensor_time, sensor_data_tps, color='green', y_range_name="b" , line_width=2)
    gbp = p4.line(sensor_time, sensor_data_bp, color='red', y_range_name="b", line_width=2)

    legend1 = Legend(items=[
        ((str(cutFs) + 'Hz LOW PASS FILTER LVDTFL @NCU'), [g5]),
        ((str(cutFs) + 'Hz LOW PASS FILTER LVDTFR @NCU'), [g6]),
        ((str(cutFs) + 'Hz LOW PASS FILTER LVDTRL @NCU'), [g7]),
        ((str(cutFs) + 'Hz LOW PASS FILTER LVDTRR @NCU'), [g8]),
        ((str(cutFsAlt) + 'Hz LOW PASS FILTER FRONT ALTERNATOR @NCU'), [g10]),
        ((str(cutFsAlt) + 'Hz LOW PASS FILTER REAR ALTERNATOR @NCU'), [g11]),
        ('35Hz Steering Angle @MOTEC', [g9])
    ], location=(0,0))

    legend2 = Legend(items=[
        ((str(cutFs) + 'Hz LOW PASS FILTER DUMPER LVDTFL @NCU'), [g13]),
        ((str(cutFs) + 'Hz LOW PASS FILTER DUMPER LVDTFR @NCU'), [g14]),
        ((str(cutFs) + 'Hz LOW PASS FILTER DUMPER LVDTRL @NCU'), [g15]),
        ((str(cutFs) + 'Hz LOW PASS FILTER DUMPER LVDTRR @NCU'), [g16])
    ], location=(0,0))

    legend3 = Legend(items=[

    ], location=(0,0))

    legend4 = Legend(items=[
        ((str(5) + 'Hz LOW PASS FILTER G LAT FORCE @NCU'), [gx]),
        ((str(5) + 'Hz LOW PASS FILTER G LONGITUDIAL FORCE @NCU'), [gy]),
        ((str(5) + 'Hz LOW PASS FILTER G VERTICAL FORCE @NCU'), [gz]),
        ((str(35) + 'Hz TPS @MOTEC'), [gtps]),
        ((str(35) + 'Hz BRAKE PRESSURE @MOTEC'), [gbp]),
    ], location=(0,0))

    p1.add_layout(legend1, 'right')
    p2.add_layout(legend2, 'right')
    p3.add_layout(legend3, 'right')
    p4.add_layout(legend4, 'right')

    p1.legend.click_policy = 'hide'
    p2.legend.click_policy='hide'
    p3.legend.click_policy = 'hide'
    p4.legend.click_policy = 'hide'

    p1.toolbar.logo = None
    p2.toolbar.logo = None
    p3.toolbar.logo = None
    p4.toolbar.logo = None

    grid1 = gridplot([[p1],[p4],[p2]],  toolbar_location='left')

    l1 = layout([grid1])

    tab = Panel(child=l1, title="Suspension Position", closable=True)
    return tab

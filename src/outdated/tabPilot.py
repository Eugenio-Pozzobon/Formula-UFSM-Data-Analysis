#import bokeh
from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.models.layouts import Box

#import pandas
import pandas as pd

def pilot(data):

    #Tooltips index the mouse pointer and show values
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]
    #set render, can be webgl, svg, or canvas
    renderer = 'webgl'
    #Set the Graphic tools for user, this is write in the same order as is showed
    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    #Set the datasets by the named col inside de csv log
    sensor_data = data['RPM']
    sensor_data_b = data['SteeringAngle']
    sensor_data_c = data['TPS']
    sensor_data_d = data['BrakePressure']
    sensor_data_e = data['Speed']

    #forces the dataset to be recognizes as number
    sensor_data = pd.to_numeric(sensor_data)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)*10
    sensor_data_e = pd.to_numeric(sensor_data_e)

    #get timing indexing
    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    #create the figures. set axis, tools and title
    p = figure(title = 'Engine RPM', plot_width = 1500, plot_height = 300,
               x_axis_label = 's', y_axis_label = '°C', toolbar_location="left",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )
    p1 = figure(title = 'Pedals', plot_width = 1500, plot_height = 300,
               x_axis_label = 's', y_axis_label = '%', toolbar_location="left",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               x_range=p.x_range)
    p2 = figure(title = 'Steering', plot_width = 1500, plot_height = 300,
               x_axis_label = 's', y_axis_label = 'degree', toolbar_location="left",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               x_range=p.x_range,
               )

    #set the axis limitis for each figure

    y_overlimit = 0.05
    p.y_range = Range1d(
        sensor_data.min() * (1 - y_overlimit), sensor_data.max() * (1 + y_overlimit)
    )
    # there is some sexondary axis
    p.extra_y_ranges = {"b": Range1d(
        sensor_data_e.min() * (1 - y_overlimit), sensor_data_e.max() * (1 + y_overlimit)
    )}
    p.add_layout(LinearAxis(y_range_name="b", axis_label="Km/h"), 'right')

    p1.y_range = Range1d(
        sensor_data_c.min() * (1 - y_overlimit), sensor_data_c.max() * (1 + y_overlimit)
    )
    p1.extra_y_ranges = {"b": Range1d(
        sensor_data_d.min() * (1 - y_overlimit), sensor_data_d.max() * (1 + y_overlimit)
    )}
    p1.add_layout(LinearAxis(y_range_name="b", axis_label="bar"), 'right')

    #create line plots for each sensor and for each graphic
    g1 = p.line(sensor_time, sensor_data, color='red', line_cap = 'round', line_join='bevel', line_width=2)

    g3 = p.line(sensor_time, sensor_data_e, color='blue',line_cap = 'round', y_range_name="b",line_join='bevel', line_width=1, alpha = 0.6)

    g6 = p1.line(sensor_time, sensor_data_c, color='green', line_cap = 'round', line_join='bevel', line_width=2)

    g7 = p1.line(sensor_time, sensor_data_d, color='red', line_cap = 'round', y_range_name="b",line_join='round', line_width=2)

    g2 = p2.line(sensor_time, sensor_data_b, color='orange',line_cap = 'round', line_join='bevel', line_width=2)

    #set legends for each plot
    legend = Legend(items=[
        ("35Hz Engine RPM @MOTEC", [g1]), #legend, plot
        ("35Hz Speed Km/h @MOTEC", [g3]),
    ], location=(0,0))
    legend1 = Legend(items=[
        ("35Hz T Position @MOTEC", [g6]),
        ("35Hz Brake Pressure @MOTEC", [g7])
    ], location=(0,0))
    legend2 = Legend(items=[
        ("35Hz Steering Angle @MOTEC", [g2]),
    ], location=(0,0))

    #add the legend into the figures
    p.add_layout(legend, 'right')
    p1.add_layout(legend1, 'right')
    p2.add_layout(legend2, 'right')

    # allows to hide legend by clicking that
    p.legend.click_policy = 'hide'
    p1.legend.click_policy='hide'
    p2.legend.click_policy='hide'

    #try to remove bokeh logo from tools
    p.toolbar.logo = None
    p1.toolbar.logo = None
    p2.toolbar.logo = None

    #create a Gridplot, that allow to combine the plot tools and make a more aligned strcuture of plots
    grid = gridplot([[p], [p1], [p2]], plot_width=1450, plot_height=300, merge_tools=True, toolbar_location='left', sizing_mode='scale_width')

    l1 = layout(grid)
    tab = Panel(child=l1, title="Pilot Analysis", closable=True)

    return tab

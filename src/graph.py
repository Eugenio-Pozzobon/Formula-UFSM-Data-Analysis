from bokeh.io import show, output_notebook
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models import Arc, Circle, ColumnDataSource, Plot, Range1d, Ray, Text
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh.models import ColumnDataSource

from bokeh.plotting import figure, output_file
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.models.layouts import Box
from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d

import pandas as pd
import numpy as np
import src.settings as settings

def plot_ncu_graph(title, labels, renderer, graphtools,
                   figure_plots,
                   source,
                   ):
    '''
    create plots customized by programed and users files
    :param title: plot title
    :param labels: plot label in sequence [x,y,y2], can be just [x,y]
    :param renderer: webgl, svg or canvas
    :param graphtools: tools for user analysis the graph
    :param figure_plots: dataframe containing all data for make the plot
    :param source: ColumnDatSource object for bokeh struct
    :return: plot
    '''

    #try:

    lines = []
    secondary_axis = False
    for ax_ch in figure_plots['axis']:
        if ax_ch == 'b':
            secondary_axis = True

    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    p = figure(title = title,
               x_axis_label = labels[0],
               y_axis_label = labels[1],
               plot_width = 1400, plot_height = 300,
               toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphtools,
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    # FIRST AXIS

    min_all = []
    max_all = []
    for index, figure_plot in figure_plots.iterrows():
        min_all.append(source.data[figure_plot['channel']].min())
        max_all.append(source.data[figure_plot['channel']].max())


    if secondary_axis:

        p.extra_y_ranges = {"b": Range1d( # 0,140
            source.data[figure_plots.iloc[-1, 1]].min() * (1 - y_overlimit),
            source.data[figure_plots.iloc[-1, 1]].max() * (1 + y_overlimit)
        )}
        p.add_layout(LinearAxis(y_range_name='b', axis_label=labels[2]), 'right')

    i=0
    for index, figure_plot in figure_plots.iterrows():

        ch_max = ' | Max: '+ str(int(pd.to_numeric(source.data[figure_plot['channel']]).max()))
        ch_min = ' -- Min: '+ str(int(pd.to_numeric(source.data[figure_plot['channel']]).min()))
        ch_ave = ' | Average: '+ str(int(np.average(pd.to_numeric(source.data[figure_plot['channel']]))))

        leg = figure_plot['legend'] #+ ch_min + ch_ave + ch_max
        color = settings.channels_config_propertise.loc[figure_plot['channel'], 'Color']
        if figure_plot['axis'] == 'b':

            gli = p.line(x=figure_plot['x'], y=figure_plot['channel'], color=color, line_width=figure_plot['line_w'],
                   alpha=figure_plot['alpha'], y_range_name=figure_plot['axis'],
                   source=source,
                         legend_label = leg)
            #lines.append() #, y_range_name=figure_plot['axis']
        else:
            gli = p.line(x=figure_plot['x'], y=figure_plot['channel'], color=color, line_width=figure_plot['line_w'],alpha=figure_plot['alpha'], source=source, legend_label = leg)

    p.toolbar.logo = None
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = '10pt'

    return p

def make_ncu_tabs(source, number_tabs):
    '''

    :param source: ColumnDataSource bokeh object
    :param number_tabs: number of tabs to create in the folder config file, string or int
    :return: array of pannels objects
    '''

    setup_pannel = []
    titles_pannel = []
    numbers_figures_pannel = []



    for i in range(0, int(number_tabs)):
        filetabs = open('projectfolder/configuration/tabs/tab' + str(i) + '/tabSetup.txt')
        setup_pannel.append(filetabs.readlines())
        title_pannel = setup_pannel[i][0].split(':')[1]
        title_pannel = (title_pannel.encode()[:-1]).decode()
        titles_pannel.append(title_pannel)

        number_figures_pannel = setup_pannel[i][1].split(':')[1]
        number_figures_pannel = (number_figures_pannel.encode()[:-1]).decode()
        numbers_figures_pannel.append(number_figures_pannel)
        filetabs.close()

    tabs = []
    for j in range(0, int(number_tabs)):
        gd = []
        for i in range(0, int(numbers_figures_pannel[j])):
            setup = open('projectfolder/configuration/tabs/tab' + str(j) + '/figure' + str(i) + 'Setup.txt')
            setupFigure = setup.readlines()

            setupPlots = pd.read_csv(
                'projectfolder/configuration/tabs/tab' + str(j) + '/figure' + str(i) + 'Plots.csv', sep=';')

            title = setupFigure[0].split(':')[1]
            title = (title.encode()[:-1]).decode()

            labels = setupFigure[1].split(':')[1]
            labels = (labels.encode()[:-1]).decode().split(sep=',')

            renderer = setupFigure[2].split(':')[1]
            renderer = (renderer.encode()[:-1]).decode()
            # Set the Graphic tools for user, this is write in the same order as is showed

            graphtools = setupFigure[3].split(':')[1]
            graphtools = (graphtools.encode()[:-1]).decode()

            # create the figures. set axis, tools and title

            p = plot_ncu_graph(title, labels, renderer, graphtools, setupPlots, source)
            gd.append([p])
            setup.close()

            # create a Gridplot, that allow to combine the plot tools and make a more aligned strcuture of plots
        grid = gridplot(gd, plot_width=1400, plot_height=300, merge_tools=True, toolbar_location='left',
                            sizing_mode='scale_width')
            # , [p1], [p2]

        tabs.append(Panel(child=layout(grid), title=titles_pannel[j], closable=True))
    return tabs

def plot_layout_tab(source, index):
    '''

    :param source: ColumnDataSource bokeh object
    :param number_tabs: number of tabs to create in the folder config file, string or int
    :return: array of pannels objects
    '''

    setup_pannel = ''

    filetabs = open('projectfolder/configuration/tabs/tab' + str(index) + '/tabSetup.txt')
    setup_pannel = filetabs.readlines()
    number_figures_pannel = setup_pannel[1].split(':')[1]
    number_figures_pannel = (number_figures_pannel.encode()[:-1]).decode()
    filetabs.close()

    gd = []
    for i in range(0, int(number_figures_pannel)):
        setup = open('projectfolder/configuration/tabs/tab' + str(index) + '/figure' + str(i) + 'Setup.txt')
        setupFigure = setup.readlines()

        setupPlots = pd.read_csv(
            'projectfolder/configuration/tabs/tab' + str(index) + '/figure' + str(i) + 'Plots.csv', sep=';')

        title = setupFigure[0].split(':')[1]
        title = (title.encode()[:-1]).decode()

        labels = setupFigure[1].split(':')[1]
        labels = (labels.encode()[:-1]).decode().split(sep=',')

        renderer = setupFigure[2].split(':')[1]
        renderer = (renderer.encode()[:-1]).decode()
        # Set the Graphic tools for user, this is write in the same order as is showed

        graphtools = setupFigure[3].split(':')[1]
        graphtools = (graphtools.encode()[:-1]).decode()

        # create the figures. set axis, tools and title

        p = plot_ncu_graph(title, labels, renderer, graphtools, setupPlots, source)
        gd.append([p])
        setup.close()

    for i in range(1, int(number_figures_pannel)):
        gd[i][0].x_range=gd[0][0].x_range

    # create a Gridplot, that allow to combine the plot tools and make a more aligned strcuture of plots
    grid = gridplot(gd, plot_width=1400, plot_height=300, merge_tools=True, toolbar_location='left',
                        sizing_mode='scale_width')
        # , [p1], [p2]
    return layout(grid)
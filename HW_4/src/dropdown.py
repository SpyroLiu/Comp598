from bokeh.layouts import column
from bokeh.models import  ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.models import Dropdown
import bokeh.palettes as pl
import numpy as np

import json
import os.path as osp

def createZipCodeDropdown():
    script_dir = osp.dirname(__file__)
    path = osp.join(script_dir, '..', 'data', 'month_avg.json')
    with open(path) as json_file:
        month_avg = json.load(json_file)
    path = osp.join(script_dir, '..', 'data', 'zip_avg.json')
    with open(path) as json_file:
        zip_avg = json.load(json_file)

    menu = list(zip_avg.keys())
    d1 = Dropdown(label='Select Zipcode 1', menu=menu)
    d2 = Dropdown(label='Select Zipcode 2', menu=menu)
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    p = figure(x_range=month, x_axis_label='Months of 2020', y_axis_label='Average incident create-to-closed time in hours')

    source = ColumnDataSource(data=dict(
        x=[month, month, month],
        y=[[np.nan]*12, [np.nan]*12, [month_avg[i] for i in month_avg]],
        colors=pl.Category20[3],
        legend=['Zipcode 1 N/A', 'Zipcode 2 N/A', 'All']
    ))

    multiline = p.multi_line(xs='x', ys='y', line_width=4, color='colors', legend='legend', source=source)
    ds = multiline.data_source

    def handler1(event):
        zipcode = event.item
        new_data = {}
        new_data['x'] = ds.data['x']
        new_data['y'] = ds.data['y']
        new_data['y'][0] = list(zip_avg[zipcode].values())
        new_data['colors'] = ds.data['colors']
        new_data['legend'] = ds.data['legend']
        new_data['legend'][0] = str(zipcode) + ' '
        ds.data = new_data

    def handler2(event):
        zipcode = event.item
        new_data = {}
        new_data['x'] = ds.data['x']
        new_data['y'] = ds.data['y']
        new_data['y'][1] = list(zip_avg[zipcode].values())
        new_data['colors'] = ds.data['colors']
        new_data['legend'] = ds.data['legend']
        new_data['legend'][1] = str(zipcode) + ' '
        ds.data = new_data

    p.legend.location = "top_left"
    d1.on_click(handler1)
    d2.on_click(handler2)
    curdoc().add_root(column(d1, d2, p))

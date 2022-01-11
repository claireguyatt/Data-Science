import pandas as pd
import csv

from bokeh.io import push_notebook
from bokeh.layouts import column
from bokeh.models import CustomJS, Dropdown, ColumnDataSource, Select
from bokeh.plotting import figure, curdoc

# create a plot and style its properties
p = figure(title="Monthly Average Response Times", x_axis_label="month", 
y_axis_label="time (t=h)", x_range=(0, 12), y_range=(0, 250), toolbar_location=None)
p.border_fill_color = 'white'
p.background_fill_color = 'white'
p.outline_line_color = 'blue'
p.grid.grid_line_color ='blue'

# read csv of all 2020 complaints
# use to set up data in a dict
complaints = pd.read_csv("all.csv")
month = complaints['month']
time = complaints['time']
source = ColumnDataSource(data=dict(x=month, y=time))

# initial plot: data for all of 2020 using just-made dict
p.line(x='x', y='y', source=source, line_width=2)

#p.line('month', 'time')

curdoc().add_root(p)

# return df with only matching ZIP

def get_dataset(src, name):
    df = src[src.ZIP == name]
    return ColumnDataSource(data=df)

def make_plot(source):
    plot = figure(title="Monthly Average Response Times",
    toolbar_location=None)
    plot.line(x='x', y='y', source=source, legend_label=name)

    # plot fixed attributes
    plot.title = ("Monthly Average Response Times")
    plot.x_axis_label = "Month"
    plot.y_axis_label = "Average Hours Until Complaint Closed"

    return plot

def update_plot(attrname, old, new):
    ZIP = zip_select.value
    src = get_dataset(df, complaints)

# make list of strings for dropdown

complaints['ZIP'] = complaints['ZIP'].astype(str)
ZIPlist = complaint['ZIP'].tolist()

zip_select = Select(value=ZIP, title='Zipcode', options='ZIPlist')

df = complaints
source = get_dataset(df, ZIP)
plot = make_plot(source)

zip_select.on_chnage('value', update_plot)
curdoc().add_root(plot)


# change zips into list for Select

#d = dict()
#f = open('ZIPs_only.CSV')

#for line in f:
#    line = line.strip('\n')
#    (key,val) = line.split(",")
#    d[key] = val

#menu = Select(options=[d], value='11210', title='ZIP1')

# def callback(attr, old, new):
#dropdown.on_change(ZIP_cb)
#layout = column(menu, plot)
#curdoc().add_root(column(dropdown))


import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plotly_line(df, x, y, title, x_title = None, y_title = None):
    if x_title and y_title:
        labels = {'x' : x_title, 'y' : y_title}
    else:
        labels = {}
    fig = px.line(x = x, y = y, title = title, labels = labels)
    return fig

def plotly_bar(df, x, y, title):
    if len(y) > 1:
        labels = {'value' : 'count'}
    else:
        labels = {}
    fig = px.bar(df, x, y, title = title, labels = labels)
    return fig

def plotly_pie_subplots(values, labels, nrows, ncols, names, title):
    assert type(values) == list, 'Pass values for each subplot'
    specs = [[{'type' : 'pie'}] * ncols]
    fig = make_subplots(rows=nrows, cols=ncols, specs=specs, subplot_titles=names)
    for i in range(nrows * ncols):
        fig.add_trace(go.Pie(values = values[i], labels = labels, name = names[i]), row=1, col=i + 1)
    fig.update_layout(height=500, width=1350, title= {'text' : title, 'x' : 0.5})
    return fig




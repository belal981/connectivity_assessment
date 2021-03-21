import dash
import dash_core_components as dcc
import dash_html_components as html
from modules.processing import DataHolder
import dash_bootstrap_components as dbc
from modules.visualization import *

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# set color scheme for plotly plots
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# read dataframe from csv and process it
holder = DataHolder('assets/connectivity_task.csv')
holder.load()
holder.process()

# aggregate data for plotting

# aggregated assets names
agg_assets = holder.aggregate('asset_name')

# aggregated top places names
n = 10
top_assets = list(agg_assets.index)[:n]
top_places = holder.df[holder.df['asset_name'].isin(
    top_assets)]['place_name'].unique()
agg_places = holder.aggregate(
    data=holder.df[holder.df['place_name'].isin(top_places)], target='place_name')

# aggregated assets types
agg_types = holder.aggregate('asset_type')

# aggregated week days
agg_weekdays = holder.aggregate('week_day')

# aggregated module ids
agg_modules = holder.aggregate(
    data=holder.df[holder.df['module_id'].notna()], target='module_id')


figs = []

# line plot days vs no.events
x = holder.df.groupby('event_day').count().index
y = holder.df.groupby('event_day').count()['event_type']
title = 'Days vs No. Events'
x_title = 'Day'
y_title = 'Count'
figs.append(plotly_line(holder.df, x, y, title, x_title, y_title))

# bar plot for assets names, places names, assets types, and module ids


def abstract_plot(df, title):
    x = df.index
    y = ['connected', 'disconnected']
    new_fig = plotly_bar(df, x, y, title)
    new_title = {'text' : title, 'x' : 0.5}
    new_fig.update_layout(title = new_title)
    figs.append(new_fig)


bar_aggs = [agg_assets, agg_places, agg_weekdays, agg_modules]
bar_titles = ['Assests Connectivity', 'Top Places Connectivity',
              'WeekDays Connectivity', 'Module Connectivity']
for i in range(len(bar_aggs)):
    abstract_plot(bar_aggs[i], bar_titles[i])

figs.append(plotly_pie_subplots(values=[agg_types['connected'], agg_types['disconnected']], labels=agg_types.index, nrows=1, ncols=2, names=[
            'Connected', 'Disconnected'], title='Asset Types Connectivity'))

# apply colors on figure layout
[fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
) for fig in figs]


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H3(
        children='Plotly Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Connectivity Data Analytics.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(dcc.Graph(
        id=figs[0].layout.title.text,
        figure=figs[0])),
    html.Div(dcc.Graph(
        id=figs[1].layout.title.text,
        figure=figs[1]
    )),
    html.Div(dcc.Graph(
        id=figs[2].layout.title.text,
        figure=figs[2]
    )),
    html.Div(dcc.Graph(
        id=figs[3].layout.title.text,
        figure=figs[3]
    )),
    html.Div(dcc.Graph(
        id=figs[4].layout.title.text,
        figure=figs[4]
    )),
    html.Div(dcc.Graph(
        id = figs[5].layout.title.text,
        figure=figs[5]
    ))

])


if __name__ == '__main__':
    app.run_server(debug=True)

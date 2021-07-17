import pandas as pd
import json
import plotly.express as px
from datetime import date, datetime

from filters import get_daily_movie_views, get_daily_series_views
from helpers import get_clean_serie_name

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__,
                title='Datathon')

########################################
# 1. First let's import the data
########################################
df_base_train = pd.read_csv('data/train.csv')
df_base_metadata = pd.read_csv('data/metadata.csv', delimiter=';')

with open('data/iso_3166_1.json', 'r') as jsonfile:
    json_country_codes = json.loads(jsonfile.read())

########################################
# 2. App layout
########################################

app.layout = html.Div([

    html.Img(src='assets/logo.webp', id='logo'),

    html.H1('Prueba de contenido:'),

    html.Div(dcc.DatePickerSingle(
        id='date-picker-single',
        min_date_allowed=date(2021, 1, 1),
        max_date_allowed=date(2021, 3, 31),
        date=date(2021, 3, 31),
        display_format='DD/MM/YYYY'
    )),
    dcc.Dropdown(id="slct_amount",
                 options=[
                     {"label": "Top 3", "value": 3},
                     {"label": "Top 5", "value": 5},
                     {"label": "Top 10", "value": 10}],
                 multi=False,
                 clearable=False,
                 value=5,
                 style={'width': "40%"}
                 ),
    html.Br(),
    dcc.Graph(id='daily_movies', figure={}),
    html.Br(),
    dcc.Graph(id='daily_series', figure={}),

    html.Div(html.P(['<> with ❤ by ',
                    html.A('Nachichuri', href='https://github.com/Nachichuri', target='_blank'),
                    ' - Source code available on ',
                    html.A('Github', href='https://github.com/Nachichuri/datathon21-dataviz-challenge', target='_blank')]),
            id='credits')
    
], id='main-cont')

########################################
# 3. Callbacks
########################################

@app.callback(
    [Output(component_id='daily_movies', component_property='figure'),
     Output(component_id='daily_series', component_property='figure')],
    
    [Input(component_id='date-picker-single', component_property='date'),
     Input(component_id='slct_amount', component_property='value')]
)
def update_graph(date_slctd, amount_slctd):

    parsed_date = datetime.strptime(date_slctd, '%Y-%m-%d').strftime('%d/%m/%Y')

    df_daily_movies = pd.DataFrame(get_daily_movie_views(df_base_train, df_base_metadata, date_slctd, amount_slctd))
    df_daily_series = get_daily_series_views(df_base_train, df_base_metadata, date_slctd, amount_slctd)
    # The series include season and episode in every title, so we clean it for display in a new column:
    df_daily_series['clean_title'] = df_daily_series.apply(lambda row: get_clean_serie_name(row['title']), axis=1)
    

    daily_movies = px.bar(
        data_frame=df_daily_movies,
        x='title',
        y='views',
        hover_data=['views', 'asset_id'],
        labels={'title': f'Películas más vistas el {parsed_date}',
                'views': 'Visualizaciones'},
        template='plotly_dark'
    )

    daily_series = px.bar(
        data_frame=df_daily_series,
        x='clean_title',
        y='views',
        hover_data=['views', 'serie_id'],
        labels={'clean_title': f'Series más vistas el {parsed_date}',
                'views': 'Visualizaciones',
                'serie_id': 'asset_id'},
        template='plotly_dark'
    )

    return daily_movies, daily_series

########################################
# 4. Run
########################################

if __name__ == '__main__':
    app.run_server(debug=True)

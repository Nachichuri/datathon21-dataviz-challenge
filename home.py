import pandas as pd
import json
import plotly.express as px
import plotly.io as pio
from assets.template import get_flow_template
from datetime import datetime

from filters import get_movie_views, get_series_views, get_shows_watch, get_mostwatched_episodes, get_device_used
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

first_date = datetime.strptime(sorted(df_base_train['tunein'].str[0:10].value_counts().keys().to_list())[0], '%Y-%m-%d').date()
last_date = datetime.strptime(sorted(df_base_train['tunein'].str[0:10].value_counts().keys().to_list())[-1], '%Y-%m-%d').date()

########################################
# 2. App layout
########################################

# Flow graph template
pio.templates['flow_theme'] = get_flow_template()

app.layout = html.Div([

    html.Img(src='assets/logo.webp', id='logo'),
    html.Hr(),
    html.H1('Estadísticas diarias:', className='section-title'),
    html.Div([
        html.Div([
            html.H2('Fecha:'),
            dcc.DatePickerSingle(
                id='date-picker-single',
                min_date_allowed=first_date,
                max_date_allowed=last_date,
                date=last_date,
                display_format='DD/MM/YYYY'
                )],
            className='selector-container'),
        html.Div([
            html.H2('Cantidad:'),
            dcc.Dropdown(
                id="slct_amount",
                options=[
                    {"label": "Top 3", "value": 3},
                    {"label": "Top 5", "value": 5},
                    {"label": "Top 10", "value": 10}],
                multi=False,
                clearable=False,
                value=5,
                style={'width': "40%"}
                )],
            className='selector-container')
    ], className='main-selector'),

    html.Br(),
    html.Div([
    dcc.Graph(id='daily_series', figure={}),
    dcc.Graph(id='daily_episodes', figure={})
    ], className='graph-container'),
    html.Br(),
    html.Div([
    dcc.Graph(id='daily_movies', figure={}),
    dcc.Graph(id='daily_shows', figure={})
    ], className='graph-container'),
    html.Br(),
    dcc.Graph(id='daily_device_used', figure={}),



    html.Hr(),
    html.H1('Estadísticas mensuales:', className='section-title'),
    html.Div([
        html.Div([
            html.H2('Mes:'),
            dcc.Dropdown(
                id="month_amount",
                options=[{"label": month, "value": month} for month in sorted(df_base_train['tunein'].str[0:7].value_counts().keys().to_list())],
                multi=False,
                clearable=False,
                value=sorted(df_base_train['tunein'].str[0:7].value_counts().keys().to_list())[-1],
                style={'width': "40%"}
                )],
            className='selector-container'),
        html.Div([
            html.H2('Cantidad:'),
            dcc.Dropdown(
                id="slct_amount_monthly",
                options=[
                    {"label": "Top 3", "value": 3},
                    {"label": "Top 5", "value": 5},
                    {"label": "Top 10", "value": 10}],
                multi=False,
                clearable=False,
                value=5,
                style={'width': "40%"}
                )],
            className='selector-container')
    ], className='main-selector'),
    
    dcc.Graph(id='monthly_movies', figure={}),
    html.Br(),
    html.Div([
    dcc.Graph(id='monthly_series', figure={}),
    dcc.Graph(id='monthly_shows', figure={})
    ], className='graph-container'),

    html.Div(html.P(['<> with ☕ by ',
                    html.A('Nachichuri', href='https://github.com/Nachichuri', target='_blank'),
                    ' - Source code available on ',
                    html.A('Github', href='https://github.com/Nachichuri/datathon21-dataviz-challenge', target='_blank')]),
            id='credits')
    
], id='main-cont')

########################################
# 3. Callbacks
########################################

@app.callback(
    [Output(component_id='daily_series', component_property='figure'),
     Output(component_id='daily_episodes', component_property='figure'),
     Output(component_id='daily_movies', component_property='figure'),
     Output(component_id='daily_shows', component_property='figure'),
     Output(component_id='daily_device_used', component_property='figure'),
     Output(component_id='monthly_movies', component_property='figure'),
     Output(component_id='monthly_series', component_property='figure'),
     Output(component_id='monthly_shows', component_property='figure')],
    
    [Input(component_id='date-picker-single', component_property='date'),
     Input(component_id='slct_amount', component_property='value'),
     Input(component_id='month_amount', component_property='value'),
     Input(component_id='slct_amount_monthly', component_property='value')]
)
def update_graph(date_slctd, amount_slctd, month_amount, slct_amount_monthly):

    parsed_date = datetime.strptime(date_slctd, '%Y-%m-%d').strftime('%d/%m/%Y')

    df_base_daily = df_base_train[df_base_train['tunein'].str.startswith(str(date_slctd))]
    df_base_monthly = df_base_train[df_base_train['tunein'].str.startswith(str(month_amount))]

    df_daily_movies = pd.DataFrame(get_movie_views(df_base_daily, df_base_metadata, amount_slctd))
    df_monthly_movies = pd.DataFrame(get_movie_views(df_base_monthly, df_base_metadata, slct_amount_monthly))
    df_daily_series = get_series_views(df_base_daily, df_base_metadata, amount_slctd)
    df_monthly_series = get_series_views(df_base_monthly, df_base_metadata, slct_amount_monthly)
    # The series include season and episode in every title, so we clean it for display in a new column:
    df_daily_series['clean_title'] = df_daily_series.apply(lambda row: get_clean_serie_name(row['title']), axis=1)
    df_monthly_series['clean_title'] = df_monthly_series.apply(lambda row: get_clean_serie_name(row['title']), axis=1)
    df_daily_shows = get_shows_watch(df_base_daily, df_base_metadata, amount_slctd)
    df_monthly_shows = get_shows_watch(df_base_monthly, df_base_metadata, slct_amount_monthly)
    df_daily_episodes = get_mostwatched_episodes(df_base_daily, df_base_metadata, amount_slctd)
    df_daily_device_used = pd.DataFrame(get_device_used(df_base_daily, df_base_train))

    daily_movies = px.bar(
        data_frame=df_daily_movies,
        x='title',
        y='views',
        hover_data=['views', 'asset_id'],
        labels={'title': 'Nombre de la película',
                'views': 'Visualizaciones'},
        template='flow_theme',
        title=f'Películas más vistas el {parsed_date}'
    )

    daily_series = px.bar(
        data_frame=df_daily_series,
        x='clean_title',
        y='views',
        hover_data=['views', 'serie_id'],
        labels={'clean_title': 'Nombre de la serie',
                'views': 'Visualizaciones',
                'serie_id': 'asset_id'},
        template='flow_theme',
        title=f'Series más vistas el {parsed_date}'
    )

    daily_shows = px.bar(
        data_frame=df_daily_shows,
        x='title',
        y='views',
        hover_data=['views', 'episode_title', 'show_id'],
        labels={'title': 'Nombre del show',
                'episode_title': 'Título',
                'views': 'Visualizaciones',
                'show_id': 'asset_id'},
        template='flow_theme',
        title=f'Shows de TV más vistos el {parsed_date}'
    )

    daily_episodes = px.bar(
        data_frame=df_daily_episodes,
        x='title',
        y='views',
        hover_data=['views', 'episode_title', 'serie_id'],
        labels={'title': 'Nombre del episodio',
                'episode_title': 'Título',
                'views': 'Visualizaciones',
                'serie_id': 'asset_id'},
        template='flow_theme',
        title=f'Episodios con más visualizaciones el {parsed_date}'
    )

    daily_device_used = px.line(
        data_frame=df_daily_device_used,
        x='hour',
        y='views',
        color='device',
        template='flow_theme',
        hover_data=['device', 'hour', 'views'],
        labels={'device': 'Dispositivo',
                'hour': 'Horario',
                'views': 'Visualizaciones'},
        title=f'Consumo de contenido por dispositivo el {parsed_date}'
    )

    monthly_movies = px.bar(
        data_frame=df_monthly_movies,
        x='title',
        y='views',
        hover_data=['views', 'asset_id'],
        labels={'title': 'Nombre de la película',
                'views': 'Visualizaciones'},
        template='flow_theme',
        title=f'Películas más vistas en {datetime.strptime(month_amount, "%Y-%m").strftime("%B %Y")}'
    )

    monthly_series = px.bar(
        data_frame=df_monthly_series,
        x='clean_title',
        y='views',
        hover_data=['views', 'serie_id'],
        labels={'clean_title': 'Nombre de la serie',
                'views': 'Visualizaciones',
                'serie_id': 'asset_id'},
        template='flow_theme',
        title=f'Series más vistas en {datetime.strptime(month_amount, "%Y-%m").strftime("%B %Y")}'
    )

    monthly_shows = px.bar(
        data_frame=df_monthly_shows,
        x='title',
        y='views',
        hover_data=['views', 'episode_title', 'show_id'],
        labels={'title': 'Nombre del show',
                'episode_title': 'Título',
                'views': 'Visualizaciones',
                'show_id': 'asset_id'},
        template='flow_theme',
        title=f'Shows de TV más vistos en {datetime.strptime(month_amount, "%Y-%m").strftime("%B %Y")}'
    )    

    return daily_series, daily_episodes, daily_movies, daily_shows, daily_device_used, monthly_movies, monthly_series, monthly_shows

########################################
# 4. Run
########################################

if __name__ == '__main__':
    app.run_server(host= '0.0.0.0', debug=True)

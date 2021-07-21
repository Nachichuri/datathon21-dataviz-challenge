import pathlib
import pandas as pd
import plotly.express as px
import plotly.io as pio
from assets.template import get_flow_template
from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime

from filters import get_movie_views, get_series_views, get_shows_watch, get_mostwatched_episodes, get_device_used, get_category_per_showtype, get_potential_most_dropped_content
from helpers import get_clean_serie_name

from app import app

DATA_PATH = pathlib.Path(__file__).parent.joinpath("../data").resolve()

########################################
# 1. First let's import the data
########################################

df_base_train = pd.read_csv(f'{DATA_PATH}/train.csv')
df_base_metadata = pd.read_csv(f'{DATA_PATH}/metadata.csv', delimiter=';')

first_date = datetime.strptime(sorted(df_base_train['tunein'].str[0:10].value_counts().keys().to_list())[0], '%Y-%m-%d').date()
last_date = datetime.strptime(sorted(df_base_train['tunein'].str[0:10].value_counts().keys().to_list())[-1], '%Y-%m-%d').date()


########################################
# 2. App layout
########################################

pio.templates['flow_theme'] = get_flow_template()

layout = html.Div([
    html.H1('Estadísticas diarias', className='section-title'),
    # Inputs
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
    # Plots
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
    html.Br(),
    dcc.Graph(id='daily_category_per_showtype', figure={}),
    html.Br(),
    html.Div([
        dcc.Graph(id='daily_dropped_movies', figure={}),
        dcc.Graph(id='daily_dropped_series', figure={})
        ], className='graph-container'),
    html.P('* Se entiende como "dropeado" al total de reproducciones que finalizaron antes de los 5 minutos de visualización.')
])


########################################
# 3. Callbacks
########################################

@app.callback(
    [Output(component_id='daily_series', component_property='figure'),
     Output(component_id='daily_episodes', component_property='figure'),
     Output(component_id='daily_movies', component_property='figure'),
     Output(component_id='daily_shows', component_property='figure'),
     Output(component_id='daily_device_used', component_property='figure'),
     Output(component_id='daily_category_per_showtype', component_property='figure'),
     Output(component_id='daily_dropped_movies', component_property='figure'),
     Output(component_id='daily_dropped_series', component_property='figure')],
    
    [Input(component_id='date-picker-single', component_property='date'),
     Input(component_id='slct_amount', component_property='value')]
)
def update_graph(date_slctd, amount_slctd):

    parsed_date = datetime.strptime(date_slctd, '%Y-%m-%d').strftime('%d/%m/%Y')

    df_base_daily = df_base_train[df_base_train['tunein'].str.startswith(str(date_slctd))].merge(df_base_metadata, on='asset_id')

    df_daily_movies = pd.DataFrame(get_movie_views(df_base_daily, amount_slctd))
    df_daily_series = get_series_views(df_base_daily, df_base_metadata, amount_slctd)
    # The series include season and episode in every title, so we clean it for display in a new column:
    df_daily_series['clean_title'] = df_daily_series.apply(lambda row: get_clean_serie_name(row['title']), axis=1)
    df_daily_shows = get_shows_watch(df_base_daily, df_base_metadata, amount_slctd)
    df_daily_episodes = get_mostwatched_episodes(df_base_daily, df_base_metadata, amount_slctd)
    df_daily_device_used = pd.DataFrame(get_device_used(df_base_daily, df_base_train))
    df_daily_category_per_showtype = pd.DataFrame(get_category_per_showtype(df_base_daily, amount_slctd))
    df_potentially_dropped_movies = get_potential_most_dropped_content(df_base_daily[df_base_daily['show_type'] == 'Película'], df_base_metadata, amount_slctd)
    df_potentially_dropped_series = get_potential_most_dropped_content(df_base_daily[df_base_daily['show_type'] == 'Serie'], df_base_metadata, amount_slctd)
    df_potentially_dropped_series['clean_title'] = df_potentially_dropped_series.apply(lambda row: get_clean_serie_name(row['title']), axis=1)

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

    daily_category_per_showtype = px.bar(
        data_frame=df_daily_category_per_showtype,
        x='category',
        y='views',
        color='show_type',
        template='flow_theme',
        hover_data=['category', 'show_type', 'views'],
        labels={'category': 'Categoría',
                'show_type': 'Tipo de show',
                'views': 'Visualizaciones'},
        title=f'Categorías con más visualizaciones el {parsed_date}'
    )

    daily_potentially_dropped_movies = px.bar(
        data_frame=df_potentially_dropped_movies,
        x='title',
        y='drops',
        hover_data=['drops', 'content_id'],
        labels={'title': 'Nombre de la película',
                'drops': 'Drops'},
        template='flow_theme',
        title=f'Películas más dropeadas* el {parsed_date}',
    )

    daily_potentially_dropped_series = px.bar(
        data_frame=df_potentially_dropped_series,
        x='clean_title',
        y='drops',
        hover_data=['drops', 'content_id'],
        labels={'clean_title': 'Nombre de la serie',
                'drops': 'Drops'},
        template='flow_theme',
        title=f'Series más dropeadas* el {parsed_date}',
    )


    return daily_series, daily_episodes, daily_movies, daily_shows, daily_device_used, daily_category_per_showtype, daily_potentially_dropped_movies, daily_potentially_dropped_series
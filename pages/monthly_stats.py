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

from filters import get_movie_views, get_series_views, get_shows_watch, get_country_from_watched_content
from helpers import get_clean_serie_name

from app import app

DATA_PATH = pathlib.Path(__file__).parent.joinpath('../data').resolve()


########################################
# 1. First let's import the data
########################################

df_base_train = pd.read_csv(f'{DATA_PATH}/train.csv')
df_base_metadata = pd.read_csv(f'{DATA_PATH}/metadata.csv', delimiter=';')


########################################
# 2. App layout
########################################

pio.templates['flow_theme'] = get_flow_template()

layout = html.Div([
    html.H1('Estadísticas mensuales', className='section-title'),
    html.Div([
        html.Div([
            html.H2('Mes:'),
            dcc.Dropdown(
                id='month_amount',
                options=[{'label': month, 'value': month} for month in sorted(df_base_train['tunein'].str[0:7].value_counts().keys().to_list())],
                multi=False,
                clearable=False,
                value=sorted(df_base_train['tunein'].str[0:7].value_counts().keys().to_list())[-1],
                style={'width': '40%'}
                )],
            className='selector-container'),
        html.Div([
            html.H2('Cantidad:'),
            dcc.Dropdown(
                id='slct_amount_monthly',
                options=[
                    {'label': 'Top 3', 'value': 3},
                    {'label': 'Top 5', 'value': 5},
                    {'label': 'Top 10', 'value': 10}],
                multi=False,
                clearable=False,
                value=5,
                style={'width': '40%'}
                )],
            className='selector-container')
    ], className='main-selector'),
    
    dcc.Graph(id='monthly_movies', figure={}),
    html.Br(),
    html.Div([
    dcc.Graph(id='monthly_series', figure={}),
    dcc.Graph(id='monthly_shows', figure={})
    ], className='graph-container'),
    html.Br(),
    dcc.Graph(id='monthly_country_of_views', figure={})
])


########################################
# 3. Callbacks
########################################

@app.callback(
    [Output(component_id='monthly_movies', component_property='figure'),
     Output(component_id='monthly_series', component_property='figure'),
     Output(component_id='monthly_shows', component_property='figure'),
     Output(component_id='monthly_country_of_views', component_property='figure')],
    
    [Input(component_id='month_amount', component_property='value'),
     Input(component_id='slct_amount_monthly', component_property='value')]
)
def update_graph(month_amount, slct_amount_monthly):

    df_base_monthly = df_base_train[df_base_train['tunein'].str.startswith(str(month_amount))].merge(df_base_metadata, on='asset_id')

    df_monthly_movies = pd.DataFrame(get_movie_views(df_base_monthly, slct_amount_monthly))
    df_monthly_series = get_series_views(df_base_monthly, df_base_metadata, slct_amount_monthly)
    # The series include season and episode in every title, so we clean it for display in a new column:
    df_monthly_series['clean_title'] = df_monthly_series.apply(lambda row: get_clean_serie_name(row['title']), axis=1)
    df_monthly_shows = get_shows_watch(df_base_monthly, df_base_metadata, slct_amount_monthly)
    # Required metadata for choropleth
    gapminder = px.data.gapminder().query('year==2007')
    df_country_from_watched_content = pd.DataFrame(get_country_from_watched_content(df_base_monthly))

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

    monthly_map_contentorigin = px.choropleth(pd.merge(gapminder, df_country_from_watched_content, how='left', on='country'), locations='iso_alpha',
                    color='views', 
                    hover_name='country',
                    template='flow_theme',
                    labels={'iso_alpha': 'Cod. ISO',
                            'views': 'Visualizaciones de contenido'},
                    color_continuous_scale=px.colors.sequential.Greens,
                    title=f'País de origen de cada visualizacion individual de contenido para {datetime.strptime(month_amount, "%Y-%m").strftime("%B %Y")}')

    return monthly_movies, monthly_series, monthly_shows, monthly_map_contentorigin
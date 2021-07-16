import pandas as pd
import json
import plotly.express as px
from datetime import date

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__,
                title='Datathon')
 
# First let's import the data
df_base_train = pd.read_csv('data/train.csv')
df_base_metadata = pd.read_csv('data/metadata.csv', delimiter=';')

with open('data/iso_3166_1.json', 'r') as jsonfile:
    json_country_codes = json.loads(jsonfile.read())

# App layout

app.layout = html.Div([

    html.Img(src='assets/logo.webp', id='logo'),

    html.H1('Test!'),

    html.Div(dcc.DatePickerSingle(
        id='date-picker-single',
        min_date_allowed=date(2021, 1, 1),
        max_date_allowed=date(2021, 3, 31),
        date=date(2021, 3, 31),
        display_format='DD/MM/YYYY'
    )),

    html.Div(html.P(['<> with ❤ by ',
                    html.A('Nachichuri', href='https://github.com/Nachichuri', target='_blank'),
                    ' - Source code available in ',
                    html.A('Github', href='https://github.com/Nachichuri/datathon21-dataviz-challenge', target='_blank')]),
            id='credits')
    
], id='main-cont')


# ----------
if __name__ == '__main__':
    app.run_server(debug=True)

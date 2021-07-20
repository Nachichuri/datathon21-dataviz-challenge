import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

from pages import daily_stats, monthly_stats


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Img(src='assets/logo.webp', id='logo'),
    html.Hr(),
    html.Div([
        html.P('Mostrar reporte:'),
        dcc.Link('Diario', href='/diario'),
        html.P('|'),
        dcc.Link('Mensual', href='/mensual'),
    ], className="link-row"),
    html.Hr(),

    html.Div(id='page-content', children=[]),

    html.Div(html.P(['<> with ☕ by ',
                    html.A('Nachichuri', href='https://github.com/Nachichuri', target='_blank'),
                    ' - Source code available on ',
                    html.A('Github', href='https://github.com/Nachichuri/datathon21-dataviz-challenge', target='_blank')]),
            id='credits')
], id='main-cont')


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/diario':
        return daily_stats.layout
    if pathname == '/mensual':
        return monthly_stats.layout
    else:
        return daily_stats.layout


if __name__ == '__main__':
    app.run_server(host= '0.0.0.0', debug=False)
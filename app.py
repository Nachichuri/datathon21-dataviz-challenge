import dash

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                title='Datathon 2021 | Data Viz Challenge'
                )
server = app.server
import dash

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                title='Datathon'
                )
server = app.server
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
import pandas as pd
from main_board import dashboard
from main_board import board
from algorithm import find_path

df = pd.read_excel("gps.xlsx", index_col=0)
df = df.sort_values(by='city', ascending=True)
df['city'] = df.index

drawing = False
counter = 0
path = []


def navBar():
    navbar = dbc.NavbarSimple(
        children=[],
        brand="Tradesman problem",
        brand_href="/",
        color="primary",
        dark=True,
    )
    return navbar


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([dcc.Location(id='loc', refresh=True),
                       navBar(),
                       html.Div(id='page-content', children=[]),
                       dcc.Interval(id='run-timer', interval=1000)])


@app.callback(Output('page-content', 'children'),
              [Input('loc', 'pathname')])
def return_layout(pathname):
    if pathname == '/':
        return dashboard(df)
    else:
        return html.P('Error ' + str(pathname))


@app.callback(
    Output('board', 'children'),
    [Input('start-id', 'value'),
     Input('finish-id', 'value'),
     Input('launch', 'n_clicks'),
     Input('reset', 'n_clicks'),
     Input('run-timer', 'n_intervals')]
)
def board_update(value1, value2, n1, n2, timer):
    global df, path, counter, drawing
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if ctx == 'launch':
        path = find_path(cities=df, start=value1, finish=value2)
        drawing = True
        return board(df, value1, value2)
    elif ctx == 'run-timer':
        if drawing:
            if counter < len(path):
                counter += 1
        return board(df, value1, value2, path=path[:counter])
    else:
        counter = 0
        drawing = False
        if value1 != value2:
            return board(df, value1, value2)
        else:
            return board(df)


if __name__ == '__main__':
    app.run_server(debug=True)


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
import pandas as pd
from main_board_cl import dashboard
from main_board_cl import board
from algorithm import find_path

df = pd.read_excel("gps.xlsx", index_col=0)
df = df.sort_values(by='city', ascending=True)
df['city'] = df.index

drawing = False
counter = 0
path = []
zoom = 4


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
                       dcc.Interval(id='run-timer', interval=1000, disabled=True),
                       navBar(),
                       html.Div(id='page-content', children=[dashboard(zoom=zoom)])
                       ])


@app.callback(Output('page-content', 'children'),
              [Input('loc', 'pathname')])
def return_layout(pathname):
    if pathname == '/':
        return dashboard(zoom=zoom)
    else:
        return html.P('Error ' + str(pathname))


@app.callback(
    [Output('board', 'children'),
     Output('run-timer', 'disabled')],
    [Input('reset', 'n_clicks'),
     Input('launch', 'n_clicks'),
     Input('run-timer', 'n_intervals'),
     Input('start-id', 'value')],
    [State('cities-list', 'value'),
     State('main-graph', 'relayoutData')]
)
def board_update(n1, n2, timer, value1, cities, relayoutData):
    global df, path, counter, drawing, zoom

    if relayoutData:
        try:
            zoom = relayoutData['mapbox.zoom']
        except:
            pass

    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if (ctx == 'launch') & (n2 is not None):
        path = find_path(cities=df.loc[df.city.isin(cities)], start=value1)
        drawing = True
        return board(st=value1, selected_cities=cities, zoom=zoom), False

    elif ctx == 'run-timer':
        if drawing:
            if counter < len(path):
                counter += 1
                return board(st=value1, selected_cities=cities, path=path[:counter], zoom=zoom), False
            else:
                return board(st=value1, selected_cities=cities, path=path, zoom=zoom), True

    elif ((ctx == 'reset') & (n1 is not None)) | (ctx == 'start-id'):
        counter = 0
        drawing = False
        return board(st=value1, selected_cities=cities, zoom=zoom), True

    else:
        return board(selected_cities=cities, zoom=zoom), True


@app.callback(
    [Output('start-id', 'options'),
     Output('start-id', 'value')],
    Input('cities-list', 'value'),
    State('start-id', 'value')
)
def change_list(value, current):
    value_lst = [{'label': c + '\n', 'value': c} for c in sorted(value)]
    current_value = current if current in [c for c in sorted(value)] else [c for c in sorted(value)][0]
    return value_lst, current_value


if __name__ == '__main__':
    app.run_server(debug=True)

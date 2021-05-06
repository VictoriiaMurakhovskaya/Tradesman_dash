import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

start, finish, fig = None, None, None

map_token = 'pk.eyJ1IjoiZG11cmFraG92c2t5aSIsImEiOiJja29jeG9wbDQwdjh1Mm9wZ3Bvbm1ndmYzIn0.qeqHa9f5UB3iY0_vdhiXgA'


def dashboard(df):
    global start, finish
    start = list(df.city)[0]
    finish = list(df.city)[-1]
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([controls(df.city)], md=3, width='auto'),
            dbc.Col(id='board', children=[board(df)], md=9, width='auto')
        ])

    ], fluid=True)

    return layout


def controls(cities):
    start_drop = [{'label': c, 'value': c} for c in cities]
    finish_drop = [{'label': c, 'value': c} for c in cities]
    main_controls = dbc.Card([
        html.Label(id='start-label', children=['Start city']),
        dcc.Dropdown(id='start-id',
                     options=start_drop,
                     value=start,
                     multi=False,
                     style={'margin-bottom': '10px'}),
        html.Label(id='finish-label', children=['Finish city']),
        dcc.Dropdown(id='finish-id',
                     options=finish_drop,
                     value=finish,
                     multi=False,
                     style={'margin-bottom': '10px'}),
        html.Div([
            dbc.Button('Run', id='launch', color='success', className='mr-1',
                       style={'width': '90px'}),
            dbc.Button('Reset', id='reset', color='primary', className='mr-1',
                       style={'width': '90px'})
        ], style={'margin': 'auto'})
    ], style={'width': '18rem', 'height': '16rem', "margin-top": "30px"}, body=True)
    return main_controls


def board(cities, st=None, fin=None, path=None):
    global fig, start, finish

    if not st:
        st = start
    else:
        start = st

    if not fin:
        fin = finish
    else:
        finish = fin

    start_df = cities.loc[cities.city == st].copy()
    finish_df = cities.loc[cities.city == fin].copy()

    return dcc.Graph(id='main-graph', figure=fig_map(cities, start_df, finish_df, path), style={"margin-top": "30px"})


def fig_map(cities, start_df, finish_df, path=None):
    if path:
        fig = base_map(cities, start_df, finish_df)
        connect = cities.loc[cities.city.isin(path)]
        connect = connect.reindex(index=path)
        fig.add_trace(go.Scattermapbox(
            lat=connect.lat,
            lon=connect.long,
            mode='lines',
            line=go.scattermapbox.Line(
                color='yellow',
                width=3
            ),
            text=connect.city,
            hoverinfo='text'
        ))
        return fig
    else:
        return base_map(cities, start_df, finish_df)


def base_map(cities, start_df, finish_df):
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
                                    lat=start_df.lat,
                                    lon=start_df.long,
                                    mode='markers',
                                    marker=go.scattermapbox.Marker(
                                        size=17,
                                        color='green',
                                        opacity=0.7
                                    ),
                                    text=start_df.city,
                                    hoverinfo='text'
                                    ))
    fig.add_trace(go.Scattermapbox(
                                    lat=finish_df.lat,
                                    lon=finish_df.long,
                                    mode='markers',
                                    marker=go.scattermapbox.Marker(
                                        size=17,
                                        color='red',
                                        opacity=0.7
                                    ),
                                    text=finish_df.city,
                                    hoverinfo='text'
                                    ))
    fig.add_trace(go.Scattermapbox(
                                    lat=cities.lat,
                                    lon=cities.long,
                                    mode='markers',
                                    marker=go.scattermapbox.Marker(
                                        size=8,
                                        color='blue',
                                        opacity=0.7
                                    ),
                                    text=cities.city,
                                    hoverinfo='text'
                                    ))
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        showlegend=False,
        margin_l=0,
        margin_t=0,
        mapbox=dict(
            accesstoken=map_token,
            bearing=0,
            center=dict(
                lat=cities.lat.mean(),
                lon=cities.long.mean(),
            ),
            pitch=0,
            zoom=5,
            style='light'
        ),
    )

    return fig
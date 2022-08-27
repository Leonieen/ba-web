from dash import Dash
#from jupyter_dash import JupyterDash
import numpy as np
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.offline as py  # (version 4.4.1)
import plotly.graph_objs as go
from plotly.subplots import make_subplots

mapbox_access_token = ("pk.eyJ1IjoiZ2VvbmllIiwiYSI6ImNsM210Ymc3ODA4NGozaWw4aG1hNDJtMW4ifQ.mmjDtqmcSpEZM2JyXe9Q8g")

url = (
    "https://raw.githubusercontent.com/Leonieen/BA/main/Data"
)

unfallorte2021_bayern = f"{url}/Unfallorte2021_Bayern_Teilnehmer.csv"
df21 = pd.read_csv(unfallorte2021_bayern)
unfallorte2020_bayern = f"{url}/Unfallorte2020_Bayern_Teilnehmer.csv"
df20 = pd.read_csv(unfallorte2020_bayern)
unfallorte2019_bayern = f"{url}/Unfallorte2019_Bayern_Teilnehmer.csv"
df19 = pd.read_csv(unfallorte2019_bayern)
unfallorte2018_bayern = f"{url}/Unfallorte2018_Bayern_Teilnehmer.csv"
df18 = pd.read_csv(unfallorte2018_bayern)
unfallorte2017_bayern = f"{url}/Unfallorte2017_Bayern_Teilnehmer.csv"
df17 = pd.read_csv(unfallorte2017_bayern)
unfallorte2016_bayern = f"{url}/Unfallorte2016_Bayern_Teilnehmer.csv"
df16 = pd.read_csv(unfallorte2016_bayern)
unfallorte2020_bayern = f"{url}/Unfallorte2020_Bayern_Teilnehmer.csv"
df = pd.read_csv(unfallorte2020_bayern)
unfallorte_alle = f"{url}/UnfallorteAlle_Bayern.csv"
df_alle = pd.read_csv(unfallorte_alle)
unfallorte_trend = f"{url}/Trend_Bayern3.csv"
df_trend = pd.read_csv(unfallorte_trend)
unfallorte_treemap = f"{url}/Treemap_Bayern3.csv"
df_treemap = pd.read_csv(unfallorte_treemap)

mapbox_access_token = ("pk.eyJ1IjoiZ2VvbmllIiwiYSI6ImNsM210Ymc3ODA4NGozaWw4aG1hNDJtMW4ifQ.mmjDtqmcSpEZM2JyXe9Q8g")

def set_jahr(chosen_jahr):
    if chosen_jahr == 'df16':
        df = df16
    elif chosen_jahr == 'df17':
        df = df17
    elif chosen_jahr == 'df18':
        df = df18
    elif chosen_jahr == 'df19':
        df = df19
    elif chosen_jahr == 'df20':
        df = df20
    elif chosen_jahr == 'df21':
        df = df21
    return df


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Declare server for Heroku deployment. Needed for Procfile.
server = app.server
blackbold = {'color': 'black', 'font-weight': 'bold'}

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'color': 'black',
    "overflow": "scroll",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "32rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Filter", className="display-4"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Vergleich", href="/page-1", active="exact"),
                dbc.NavLink("Trend", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        # Jahr
        html.Label(children=['Jahr: '], style=blackbold),
        dcc.RadioItems(id='jahr',
                       options=[
                           {'label': '2016', 'value': 'df16'},
                           {'label': '2017', 'value': 'df17'},
                           {'label': '2018', 'value': 'df18'},
                           {'label': '2019', 'value': 'df19'},
                           {'label': '2020', 'value': 'df20'},
                           {'label': '2021', 'value': 'df21'}
                       ],
                       value='df16',
                       style={'border-color': '#000000', 'padding-top': '6px',
                              'color': 'black'},
                       labelStyle={"display": "inline"}
                       ),
        html.Hr(),
        html.Ul([
            html.Li("Fahrrad", className='circle', style={'background': '#66c2a5', 'color': 'black',
                                                          'list-style': 'none', 'text-indent': '17px'}),
            html.Li("PKW", className='circle', style={'background': '#fc8d62', 'color': 'black',
                                                      'list-style': 'none', 'text-indent': '17px',
                                                      'white-space': 'nowrap'}),
            html.Li("Fußgänger", className='circle', style={'background': '#8da0cb', 'color': 'black',
                                                            'list-style': 'none', 'text-indent': '17px'}),
            html.Li("Kraftrad", className='circle', style={'background': '#e78ac3', 'color': 'black',
                                                           'list-style': 'none', 'text-indent': '17px'}),
            html.Li("GKFZ", className='circle', style={'background': '#a6d854', 'color': 'black',
                                                       'list-style': 'none', 'text-indent': '17px'}),
            html.Li("Sonstige", className='circle', style={'background': '#ffd92f', 'color': 'black',
                                                           'list-style': 'none', 'text-indent': '17px'}),
        ], style={'padding-top': '6px'}
        ),
        html.Hr(),
        # Monat_type_checklist
        html.Label(children=['Monat: '], style=blackbold),
        dcc.Checklist(id='monat',
                      options=[{'label': str(b), 'value': b} for b in sorted(df['UMONAT'].unique())],
                      value=[b for b in sorted(df['UMONAT'].unique())],
                      style={"display": "inline", 'color': 'black'},
                      labelStyle={"display": "inline"}
                      ),
        # Wochentage_checklist
        html.Label(children=['Wochentag: '], style=blackbold),
        dcc.Checklist(id='wochentage',
                      options=[{'label': str(b), 'value': b} for b in sorted(df['USTUNDE'].unique())],
                      value=[b for b in sorted(df['USTUNDE'].unique())],
                      style={"display": "inline", 'color': 'black'},  # 'label':{'color':'black'}},
                      labelStyle={"display": "inline"}
                      ),
        # Monat_type_checklist
        html.Label(children=['Stunden: '], style=blackbold),
        dcc.Checklist(id='stunden',
                      options=[{'label': str(b), 'value': b} for b in sorted(df['UMONAT'].unique())],
                      value=[b for b in sorted(df['UMONAT'].unique())],
                      style={"display": "inline", 'color': 'black'},
                      labelStyle={"display": "inline"}
                      ),

        html.Hr(),
        # Lichtverhaeltnisse_type_checklist
        html.Label(children=['Lichtverhaeltnisse: '], style=blackbold),
        dcc.Checklist(id='lichtverhaeltnisse',
                      options=[{'label': str(b), 'value': b} for b in sorted(df['ULICHTVERH'].unique())],
                      value=[b for b in sorted(df['ULICHTVERH'].unique())],
                      style={"display": "inline", 'color': 'black'},
                      labelStyle={"display": "inline", 'padding-top': '6px'}
                      ),
        # Strassenverhaeltnisse_type_checklist
        html.Label(children=['Strassenverhaeltnisse: '], style=blackbold),
        dcc.Checklist(id='strassenverhaeltnisse',
                      options=[{'label': str(b), 'value': b} for b in sorted(df['STRZUSTAND'].unique())],
                      value=[b for b in sorted(df['STRZUSTAND'].unique())],
                      style={"display": "inline", 'color': 'black'},
                      labelStyle={"display": "inline", 'padding-top': '6px'}
                      ),
        html.Hr(),
        # Unfallart_type_checklist -> austauschen dann durch neue Spalte
        html.Label(children=['Unfallart: '], style=blackbold),
        dcc.Checklist(id='unfallart',
                      options=[{'label': str(b), 'value': b} for b in sorted(df['UART'].unique())],
                      value=[b for b in sorted(df['UART'].unique())],
                      style={"display": "inline", 'color': 'black'},
                      labelStyle={"display": "inline"}
                      ),

        # Unterkategorie_type_checklist
        html.Label(children=['Unterkategorie: '], style=blackbold),
        dcc.Checklist(id='unterkategorie',
                      options=[{'label': str(b), 'value': b} for b in sorted(df['UKATEGORIE'].unique())],
                      value=[b for b in sorted(df['UKATEGORIE'].unique())],
                      style={"display": "inline", 'color': 'black'},
                      labelStyle={"display": "inline"}
                      ),

    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"),
     ]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.Div([
                # Map
                html.Div([
                    dbc.Spinner(children=[dcc.Graph(id='map1', config={'displayModeBar': False, 'scrollZoom': True},
                                                    style={'background': '#000000', 'padding-bottom': '2px',
                                                           'padding-left': '2px',
                                                           'height': '100vh', 'width': '150vh'}
                                                    )], size="lg", color="primary", type="border", fullscreen=False, ),
                    # Karte 1 Auswahl
                    html.Label(children=['Karte 1: '], style=blackbold),
                    dcc.Checklist(id='checklist_map1',
                                  options=[
                                      {'label': 'Rad', 'value': 1},
                                      {'label': 'PKW', 'value': 2},
                                      {'label': 'Fußgänger', 'value': 3},
                                      {'label': 'Krad', 'value': 4},
                                      {'label': 'Gkfz', 'value': 5},
                                      {'label': 'Sonstige', 'value': 6},
                                  ],
                                  value=[b for b in sorted(df['Teilnehmer'].unique())],
                                  style={"display": "inline", 'color': 'black', 'border-bottom': 'solid 3px',
                                         'border-color': '#000000', 'padding-top': '6px'},
                                  labelStyle={"display": "inline"}
                                  ),

                    dbc.Spinner(children=[dcc.Graph(id='map2', config={'displayModeBar': False, 'scrollZoom': True},
                                                    style={'background': '#000000', 'padding-bottom': '2px',
                                                           'padding-left': '2px',
                                                           'height': '100vh', 'width': '150vh'}
                                                    )], size="lg", color="primary", type="border", fullscreen=False, ),
                    # Karte 2 Auswahl
                    html.Label(children=['Karte 2: '], style=blackbold),
                    dcc.Checklist(id='checklist_map2',
                                  options=[
                                      {'label': 'Rad', 'value': 1},
                                      {'label': 'PKW', 'value': 2},
                                      {'label': 'Fußgänger', 'value': 3},
                                      {'label': 'Krad', 'value': 4},
                                      {'label': 'Gkfz', 'value': 5},
                                      {'label': 'Sonstige', 'value': 6},
                                  ],
                                  value=[b for b in sorted(df['Teilnehmer'].unique())],
                                  style={"display": "inline", 'color': 'black', 'border-bottom': 'solid 3px',
                                         'border-color': '#000000', 'padding-top': '6px'},
                                  labelStyle={"display": "inline"}
                                  ),

                    dbc.Spinner(children=[dcc.Graph(id='graph2', config={'displayModeBar': False, 'scrollZoom': True},
                                                    style={'background': '#000000', 'padding-bottom': '2px',
                                                           'padding-left': '2px',
                                                           'height': '100vh', 'width': '150vh'}
                                                    )], size="lg", color="primary", type="border", fullscreen=False, ),
                    # Sunburst Auswahl Faktor
                    html.Label(children=['Sunburst: '], style=blackbold),
                    dcc.Dropdown(id='my_dropdown',
                                 options=[
                                     {'label': 'Unfall mit Rad', 'value': 'IstRad'},
                                     {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
                                     {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
                                     {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
                                     {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
                                     {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
                                     {'label': 'Teilnehmer', 'value': 'Teilnehmer'}
                                 ],
                                 optionHeight=35,  # height/space between dropdown options
                                 value='Teilnehmer',  # dropdown value selected automatically when page loads
                                 disabled=False,  # disable dropdown value selection
                                 multi=False,  # allow multiple dropdown values to be selected
                                 searchable=True,  # allow user-searching of dropdown values
                                 search_value='',  # remembers the value searched in dropdown
                                 placeholder='Please select...',  # gray, default text shown when no option is selected
                                 clearable=True,  # allow user to removes the selected value
                                 style={'width': "100%", 'color': 'black', 'border-bottom': 'solid 3px',
                                        'border-color': '#000000', 'padding-top': '6px'},
                                 # use dictionary to define CSS styles of your dropdown
                                 # className='select_box',           #activate separate CSS document in assets folder
                                 # persistence=True,                 #remembers dropdown value. Used with persistence_type
                                 # persistence_type='memory'         #remembers dropdown value selected until...
                                 ),
                    dbc.Spinner(children=[dcc.Graph(id='graph3', config={'displayModeBar': False, 'scrollZoom': True},
                                                    style={'background': '#000000', 'padding-bottom': '2px',
                                                           'padding-left': '2px',
                                                           'height': '100vh', 'width': '150vh'}
                                                    )], size="lg", color="primary", type="border", fullscreen=False, ),
                    # Sunburst Auswahl Faktor
                    html.Label(children=['Heatmap/Kalender: '], style=blackbold),
                    dcc.Dropdown(id='dropdown_heatmap',
                                 options=[
                                     {'label': 'Unfall mit Rad', 'value': 'IstRad'},
                                     {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
                                     {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
                                     {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
                                     {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
                                     {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
                                     {'label': 'Teilnehmer', 'value': 'Teilnehmer'}
                                 ],
                                 optionHeight=35,
                                 value='Teilnehmer',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 search_value='',
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "100%", 'color': 'black', 'border-bottom': 'solid 3px',
                                        'border-color': '#000000', 'padding-top': '6px'},
                                 ),
                    # Graph Tageszeiten
                    dbc.Spinner(children=[dcc.Graph(id='graph4', config={'displayModeBar': False, 'scrollZoom': True},
                                                    style={'background': '#000000', 'padding-bottom': '2px',
                                                           'padding-left': '2px',
                                                           'height': '100vh', 'width': '150vh'}
                                                    )], size="lg", color="primary", type="border", fullscreen=False, ),
                    html.Label(children=['Tageszeiten: '], style=blackbold),
                    dcc.Checklist(id='checklist_tageszeiten',
                                  options=[
                                      {'label': 'Unfall mit Rad', 'value': 'IstRad'},
                                      {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
                                      {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
                                      {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
                                      {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
                                      {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
                                  ],
                                  value=['UKATEGORIE', 'UART', 'UTYP1', 'ULICHTVERH', 'IstRad', 'IstPKW', 'IstFuss',
                                         'IstKrad', 'IstGkfz', 'IstSonstig', 'STRZUSTAND'],
                                  style={"display": "inline", 'color': 'black', 'border-bottom': 'solid 3px',
                                         'border-color': '#000000', 'padding-top': '6px'},
                                  labelStyle={"display": "inline"}
                                  ),
                ],  # className='nine columns'
                ),

            ], className='row'
            ),

        ]
    elif pathname == "/page-1":
        return [
            html.H1('Zwei Jahre vergleichen',
                    style={'textAlign': 'center', 'color': 'black'}),
            dcc.Dropdown(id='vergleich_year1',
                         options=[
                             {'label': '2016', 'value': 'df16'},
                             {'label': '2017', 'value': 'df17'},
                             {'label': '2018', 'value': 'df18'},
                             {'label': '2019', 'value': 'df19'},
                             {'label': '2020', 'value': 'df20'},
                             {'label': '2021', 'value': 'df21'}
                         ],
                         optionHeight=35,
                         value='df16',
                         disabled=False,
                         multi=False,
                         searchable=True,
                         search_value='',
                         placeholder='Please select...',
                         clearable=True,
                         style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                         ),
            dcc.Dropdown(id='vergleich_year2',
                         options=[
                             {'label': '2016', 'value': 'df16'},
                             {'label': '2017', 'value': 'df17'},
                             {'label': '2018', 'value': 'df18'},
                             {'label': '2019', 'value': 'df19'},
                             {'label': '2020', 'value': 'df20'},
                             {'label': '2021', 'value': 'df21'}
                         ],
                         optionHeight=35,
                         value='df20',
                         disabled=False,
                         multi=False,
                         searchable=True,
                         search_value='',
                         placeholder='Please select...',
                         clearable=True,
                         style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                         ),
            dcc.Checklist(id='checklist_vergleich_map',
                          options=[
                              {'label': 'Rad', 'value': 1},
                              {'label': 'PKW', 'value': 2},
                              {'label': 'Fußgänger', 'value': 3},
                              {'label': 'Krad', 'value': 4},
                              {'label': 'Gkfz', 'value': 5},
                              {'label': 'Sonstige', 'value': 6},
                          ],
                          value=[b for b in sorted(df['Teilnehmer'].unique())],
                          style={"display": "inline", 'color': 'black', 'border-bottom': 'solid 3px',
                                 'border-color': '#000000', 'padding-top': '6px'},
                          labelStyle={"display": "inline"}
                          ),

            dbc.Spinner(children=[dcc.Graph(id='map_vergleich', config={'displayModeBar': False, 'scrollZoom': True},
                                            style={'background': '#000000', 'padding-bottom': '2px',
                                                   'padding-left': '2px',
                                                   'height': '100vh', 'width': '150vh', 'display': 'inline-block'}
                                            )], size="lg", color="primary", type="border", fullscreen=False, ),

            # Sunburst Auswahl Faktor1
            html.Label(children=['Sunburst: '], style=blackbold),
            dcc.Dropdown(id='vergleich_sunburst_dropdown1',
                         options=[
                             {'label': 'Unfall mit Rad', 'value': 'IstRad'},
                             {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
                             {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
                             {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
                             {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
                             {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
                             {'label': 'Teilnehmer', 'value': 'Teilnehmer'}
                         ],
                         optionHeight=35,
                         value='Teilnehmer',
                         disabled=False,
                         multi=False,
                         searchable=True,
                         search_value='',
                         placeholder='Please select...',
                         clearable=True,
                         style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                         ),
            # Sunburst Auswahl Faktor2
            # html.Label(children=['Sunburst 2: '], style=blackbold),
            # dcc.Dropdown(id='vergleich_sunburst_dropdown2',
            #              options=[
            #                  {'label': 'Unfall mit Rad', 'value': 'IstRad'},
            #                  {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
            #                  {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
            #                  {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
            #                  {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
            #                  {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
            #                  {'label': 'Teilnehmer', 'value': 'Teilnehmer'}
            #              ],
            #              optionHeight=35,
            #              value='Teilnehmer',
            #              disabled=False,
            #              multi=False,
            #              searchable=True,
            #              search_value='',
            #              placeholder='Please select...',
            #              clearable=True,
            #              style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
            #              ),
            html.Div(children=[
                dbc.Spinner(
                    children=[dcc.Graph(id='sunburst_vergleich1', config={'displayModeBar': False, 'scrollZoom': True},
                                        style={'background': '#000000', 'display': 'inline-block'}
                                        ),
                              dcc.Graph(id='sunburst_vergleich2', config={'displayModeBar': False, 'scrollZoom': True},
                                        style={'background': '#000000', 'display': 'inline-block'}
                                        )], size="lg", color="primary", type="border", fullscreen=False, ),
            ],
            ),
            html.Label(children=['Heatmap: '], style=blackbold),
            dcc.Dropdown(id='vergleich_heatmap_dropdown1',
                         options=[
                             {'label': 'Unfall mit Rad', 'value': 'IstRad'},
                             {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
                             {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
                             {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
                             {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
                             {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
                             {'label': 'Teilnehmer', 'value': 'Teilnehmer'}
                         ],
                         optionHeight=35,
                         value='Teilnehmer',
                         disabled=False,
                         multi=False,
                         searchable=True,
                         search_value='',
                         placeholder='Please select...',
                         clearable=True,
                         style={'width': "100%", 'color': 'black',
                                'padding-top': '6px'},
                         ),
            # html.Label(children=['Heatmap 2: '], style=blackbold),
            # dcc.Dropdown(id='vergleich_heatmap_dropdown2',
            #              options=[
            #                  {'label': 'Unfall mit Rad', 'value': 'IstRad'},
            #                  {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
            #                  {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
            #                  {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
            #                  {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
            #                  {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
            #                  {'label': 'Teilnehmer', 'value': 'Teilnehmer'}
            #              ],
            #              optionHeight=35,
            #              value='Teilnehmer',
            #              disabled=False,
            #              multi=False,
            #              searchable=True,
            #              search_value='',
            #              placeholder='Please select...',
            #              clearable=True,
            #              style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
            #              ),
            html.Div(children=[
                dbc.Spinner(
                    children=[dcc.Graph(id='kalender_vergleich1', config={'displayModeBar': False, 'scrollZoom': True},
                                        style={'background': '#000000', 'display': 'inline-block'}
                                        )], size="lg", color="primary", type="border", fullscreen=False, ),
                dbc.Spinner(
                    children=[dcc.Graph(id='kalender_vergleich2', config={'displayModeBar': False, 'scrollZoom': True},
                                        style={'background': '#000000', 'display': 'inline-block'}
                                        )], size="lg", color="primary", type="border", fullscreen=False, ),
            ],
            ),
            html.Label(children=['Tageszeiten: '], style=blackbold),
            dcc.Checklist(id='vergleich_tageszeiten_checklist',
                          options=[
                              {'label': 'Unfall mit Rad', 'value': 'IstRad'},
                              {'label': 'Unfall mit PKW', 'value': 'IstPKW'},
                              {'label': 'Unfall mit Fußgänger', 'value': 'IstFuss'},
                              {'label': 'Unfall mit Kraftrad', 'value': 'IstKrad'},
                              {'label': 'Unfall mit Güterkraftfahrzeug', 'value': 'IstGkfz'},
                              {'label': 'Unfall mit Sonstigen', 'value': 'IstSonstig'},
                          ],
                          value=['UKATEGORIE', 'UART', 'UTYP1', 'ULICHTVERH', 'IstRad', 'IstPKW', 'IstFuss',
                                 'IstKrad', 'IstGkfz', 'IstSonstig', 'STRZUSTAND'],
                          style={"display": "inline", 'color': 'black', 'padding-top': '6px'},
                          labelStyle={"display": "inline"}
                          ),
            html.Div(children=[
                dbc.Spinner(children=[
                    dcc.Graph(id='tageszeiten_vergleich1', config={'displayModeBar': False, 'scrollZoom': True},
                              style={'background': '#000000', 'display': 'inline-block'}
                              )], size="lg", color="primary", type="border", fullscreen=False, ),
                dbc.Spinner(children=[
                    dcc.Graph(id='tageszeiten_vergleich2', config={'displayModeBar': False, 'scrollZoom': True},
                              style={'background': '#000000', 'display': 'inline-block'}
                              )], size="lg", color="primary", type="border", fullscreen=False, ),
            ],
            ),
        ]
    elif pathname == "/page-2":
        return [
            html.Div([
                html.H1('Trends', style={'textAlign': 'center', 'color': 'black'}),
                html.Div(children=[
                    dcc.Dropdown(id='trend_dropdown1',
                                 options=[
                                     {'label': 'Summe aller Unfälle', 'value': 'SummeUnfaelle'},
                                     {'label': 'Unfälle mit Getöteten', 'value': 'UKategorie1'},
                                     {'label': 'Unfälle mit Schwerverletzten', 'value': 'UKategorie2'},
                                     {'label': 'Unfälle mit Leichtverletzten', 'value': 'UKategorie3'}
                                 ],
                                 optionHeight=35,
                                 value='SummeUnfaelle',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 search_value='',
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                                 ),
                    html.Div(children=[
                        dbc.Spinner(children=[dcc.Graph(id='trend_graph1',
                                                        # figure=px.bar(df20, x = "USTUNDE", y="Teilnehmer", title="Tageszeiten Jahr 2"),
                                                        config={'displayModeBar': False, 'scrollZoom': True},
                                                        style={'background': '#000000', 'display': 'inline-block'}
                                                        ), ], size="lg", color="primary", type="border",
                                    fullscreen=False, ),
                    ],
                    ),
                    html.H2('Wochentage', style={'textAlign': 'center', 'color': 'black'}),
                    dcc.Dropdown(id='trend_wochentage_dropdown',
                                 options=[
                                     {'label': 'Montag', 'value': 'Montag'},
                                     {'label': 'Dienstag', 'value': 'Dienstag'},
                                     {'label': 'Mittwoch', 'value': 'Mittwoch'},
                                     {'label': 'Donnerstag', 'value': 'Donnerstag'},
                                     {'label': 'Freitag', 'value': 'Freitag'},
                                     {'label': 'Samstag', 'value': 'Samstag'},
                                     {'label': 'Sonntag', 'value': 'Sonntag'}
                                 ],
                                 optionHeight=35,
                                 value='Montag',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 search_value='',
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                                 ),
                    html.Div(children=[
                        dbc.Spinner(children=[dcc.Graph(id='trend_wochentage',
                                                        config={'displayModeBar': False, 'scrollZoom': True},
                                                        style={'background': '#000000', 'display': 'inline-block'}
                                                        ), ], size="lg", color="primary", type="border",
                                    fullscreen=False, ),
                    ],
                    ),
                    html.H2('Monate', style={'textAlign': 'center', 'color': 'black'}),
                    dcc.Dropdown(id='trend_monate_dropdown',
                                 options=[
                                     {'label': 'Januar', 'value': 'Jan'},
                                     {'label': 'Februar', 'value': 'Feb'},
                                     {'label': 'März', 'value': 'Mar'},
                                     {'label': 'April', 'value': 'Apr'},
                                     {'label': 'Mai', 'value': 'Mai'},
                                     {'label': 'Juni', 'value': 'Jun'},
                                     {'label': 'Juli', 'value': 'Jul'},
                                     {'label': 'August', 'value': 'Aug'},
                                     {'label': 'September', 'value': 'Sep'},
                                     {'label': 'Oktober', 'value': 'Okt'},
                                     {'label': 'November', 'value': 'Nov'},
                                     {'label': 'Dezember', 'value': 'Dez'}
                                 ],
                                 optionHeight=35,
                                 value='Jan',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 search_value='',
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                                 ),
                    html.Div(children=[
                        dbc.Spinner(children=[dcc.Graph(id='trend_monate',
                                                        config={'displayModeBar': False, 'scrollZoom': True},
                                                        style={'background': '#000000', 'display': 'inline-block'}
                                                        ), ], size="lg", color="primary", type="border",
                                    fullscreen=False, ),
                    ],
                    ),
                    html.H2('Beleuchtung', style={'textAlign': 'center', 'color': 'black'}),
                    dcc.Dropdown(id='trend_beleuchtung_dropdown',
                                 options=[
                                     {'label': 'Tageslicht', 'value': 'Tag'},
                                     {'label': 'Dämmerung', 'value': 'Daemmerung'},
                                     {'label': 'Dunkelheit', 'value': 'Dunkelheit'}
                                 ],
                                 optionHeight=35,
                                 value='Tag',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 search_value='',
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                                 ),
                    html.Div(children=[
                        dbc.Spinner(children=[dcc.Graph(id='trend_beleuchtung',
                                                        config={'displayModeBar': False, 'scrollZoom': True},
                                                        style={'background': '#000000', 'display': 'inline-block'}
                                                        ), ], size="lg", color="primary", type="border",
                                    fullscreen=False, ),
                    ],
                    ),
                    html.H2('Straßenbedingungen', style={'textAlign': 'center', 'color': 'black'}),
                    dcc.Dropdown(id='trend_strassen_dropdown',
                                 options=[
                                     {'label': 'Trocken', 'value': 'Trocken'},
                                     {'label': 'Nass', 'value': 'Nass'},
                                     {'label': 'Winterglatt', 'value': 'Winterglatt'}
                                 ],
                                 optionHeight=35,
                                 value='Trocken',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 search_value='',
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                                 ),
                    html.Div(children=[
                        dbc.Spinner(children=[dcc.Graph(id='trend_strassen',
                                                        config={'displayModeBar': False, 'scrollZoom': True},
                                                        style={'background': '#000000', 'display': 'inline-block'}
                                                        ), ], size="lg", color="primary", type="border",
                                    fullscreen=False, ),
                    ],
                    ),
                    html.H2('Treemap', style={'textAlign': 'center', 'color': 'black'}),
                    dcc.Dropdown(id='trend_treemap_dropdown',
                                 options=[
                                     {'label': 'Fahrrad', 'value': 'IstRad'},
                                     {'label': 'PKW', 'value': 'IstPKW'},
                                     {'label': 'Fußgänger', 'value': 'IstFuss'},
                                     {'label': 'Krad', 'value': 'IstKrad'},
                                     {'label': 'Gkfz', 'value': 'IstGkfz'},
                                     {'label': 'Sonstige', 'value': 'IstSonstige'}
                                 ],
                                 optionHeight=35,
                                 value='IstRad',
                                 disabled=False,
                                 multi=False,
                                 searchable=True,
                                 search_value='',
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "100%", 'color': 'black', 'padding-top': '6px'},
                                 ),
                    html.Div(children=[
                        dbc.Spinner(children=[
                            dcc.Graph(id='trend_treemap1', config={'displayModeBar': False, 'scrollZoom': True},
                                      style={'background': '#000000', 'display': 'inline-block'}
                                      )], size="lg", color="primary", type="border", fullscreen=False, ),
                        dbc.Spinner(children=[
                            dcc.Graph(id='trend_treemap2', config={'displayModeBar': False, 'scrollZoom': True},
                                      style={'background': '#000000', 'display': 'inline-block'}
                                      )], size="lg", color="primary", type="border", fullscreen=False, ),
                        dbc.Spinner(children=[
                            dcc.Graph(id='trend_treemap3', config={'displayModeBar': False, 'scrollZoom': True},
                                      style={'background': '#000000', 'display': 'inline-block'}
                                      )], size="lg", color="primary", type="border", fullscreen=False, ),
                        dbc.Spinner(children=[
                            dcc.Graph(id='trend_treemap4', config={'displayModeBar': False, 'scrollZoom': True},
                                      style={'background': '#000000', 'display': 'inline-block'}
                                      )], size="lg", color="primary", type="border", fullscreen=False, ),
                        dbc.Spinner(children=[
                            dcc.Graph(id='trend_treemap5', config={'displayModeBar': False, 'scrollZoom': True},
                                      style={'background': '#000000', 'display': 'inline-block'}
                                      )], size="lg", color="primary", type="border", fullscreen=False, ),
                        dbc.Spinner(children=[
                            dcc.Graph(id='trend_treemap6', config={'displayModeBar': False, 'scrollZoom': True},
                                      style={'background': '#000000', 'display': 'inline-block'}
                                      )], size="lg", color="primary", type="border", fullscreen=False, ),
                    ],
                    ),
                ], ),
            ])
        ]

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# callback home maps
@app.callback([Output(component_id='map1', component_property='figure'),
               Output(component_id='map2', component_property='figure'),
               ],
              [Input('jahr', 'value'),
               Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('checklist_map1', 'value'),
               Input('checklist_map2', 'value'),
               ])
def home_maps(chosen_jahr, chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse, chosen_strassen, chosen_wochentag,
              chosen_unterkategorie, chosen_unfallart, chosen_map1, chosen_map2):
    df = set_jahr(chosen_jahr)
    filter_wochentag = (df['UWOCHENTAG'].isin(chosen_wochentag))
    filter_lichtverhaeltnisse = (df['ULICHTVERH'].isin(chosen_lichtverhaeltnisse))
    filter_strasse = (df['STRZUSTAND'].isin(chosen_strassen))
    filter_monat = (df['UMONAT'].isin(chosen_monat))
    filter_unterkategorie = (df['UKATEGORIE'].isin(chosen_unterkategorie))
    filter_unfallart = (df['UART'].isin(chosen_unfallart))
    filter_stunde = (df['USTUNDE'].isin(chosen_stunde))
    filter_map1 = (df['Teilnehmer'].isin(chosen_map1))
    filter_map2 = (df['Teilnehmer'].isin(chosen_map2))

    df_sub = df[
        filter_wochentag & filter_lichtverhaeltnisse & filter_strasse & filter_monat & filter_unterkategorie & filter_unfallart & filter_stunde]
    df_map1 = df_sub[filter_map1]
    df_map2 = df_sub[filter_map2]

    # Create figure
    locations = [go.Scattermapbox(
        lon=df_map1['XGCSWGS84'],
        lat=df_map1['YGCSWGS84'],
        mode='markers',
        marker_color=df_map1["color"].values,
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.5, 'size': 25}},
        hovertext=df_map1['symbol'],
    )]

    locations2 = [go.Scattermapbox(
        lon=df_map2['XGCSWGS84'],
        lat=df_map2['YGCSWGS84'],
        mode='markers',
        marker_color=df_map2["color"].values,
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.5, 'size': 25}},
        hovertext=df_map2['symbol'],
    )]

    # Return figure
    return {
               'data': locations,
               'layout': go.Layout(
                   uirevision='foo',  # preserves state of figure/map after callback activated
                   clickmode='event+select',
                   hovermode='closest',
                   hoverdistance=2,
                   title=dict(text="Unfaelle", font=dict(size=50, color='purple')),
                   mapbox=dict(
                       accesstoken=mapbox_access_token,
                       bearing=0,
                       style='streets',
                       center=dict(
                           lat=48.216346,
                           lon=11.158529
                       ),
                       pitch=0,
                       zoom=8.25
                   ),

               )

           }, {
               'data': locations2,
               'layout': go.Layout(
                   uirevision='foo',  # preserves state of figure/map after callback activated
                   clickmode='event+select',
                   hovermode='closest',
                   hoverdistance=2,
                   title=dict(text="Unfaelle", font=dict(size=50, color='purple')),
                   mapbox=dict(
                       accesstoken=mapbox_access_token,
                       bearing=0,
                       style='streets',
                       center=dict(
                           lat=48.216346,
                           lon=11.158529
                       ),
                       pitch=0,
                       zoom=8.25
                   ),

               )

           }


# callback home sunburst
@app.callback([Output(component_id='graph2', component_property='figure'),
               ],
              [Input('jahr', 'value'),
               Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('my_dropdown', 'value'),
               ])
def home_sunburst(chosen_jahr, chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse, chosen_strassen,
                  chosen_wochentag, chosen_unterkategorie, chosen_unfallart, chosen_sunburst_values):
    df = set_jahr(chosen_jahr)
    filter_wochentag = (df['UWOCHENTAG'].isin(chosen_wochentag))
    filter_lichtverhaeltnisse = (df['ULICHTVERH'].isin(chosen_lichtverhaeltnisse))
    filter_strasse = (df['STRZUSTAND'].isin(chosen_strassen))
    filter_monat = (df['UMONAT'].isin(chosen_monat))
    filter_unterkategorie = (df['UKATEGORIE'].isin(chosen_unterkategorie))
    filter_unfallart = (df['UART'].isin(chosen_unfallart))
    filter_stunde = (df['USTUNDE'].isin(chosen_stunde))

    df_sub = df[
        filter_wochentag & filter_lichtverhaeltnisse & filter_strasse & filter_monat & filter_unterkategorie & filter_unfallart & filter_stunde]

    graph2 = px.sunburst(
        data_frame=df_sub,
        path=["UMONAT", 'UWOCHENTAG', "USTUNDE"],  # Root, branches, leaves
        color=df_sub[chosen_sunburst_values],
        color_discrete_sequence=px.colors.qualitative.Pastel,
        maxdepth=2,
    )
    graph2.update_traces(textinfo='label+percent parent')
    graph2.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return [go.Figure(data=graph2)]


# callback home kalender heatmap
@app.callback([Output(component_id='graph3', component_property='figure'),
               ],
              [Input('jahr', 'value'),
               Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('dropdown_heatmap', 'value'),
               ])
def home_kalendar_heatmap(chosen_jahr, chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse, chosen_strassen,
                          chosen_wochentag, chosen_unterkategorie, chosen_unfallart, chosen_heatmap):
    df = set_jahr(chosen_jahr)
    filter_wochentag = (df['UWOCHENTAG'].isin(chosen_wochentag))
    filter_lichtverhaeltnisse = (df['ULICHTVERH'].isin(chosen_lichtverhaeltnisse))
    filter_strasse = (df['STRZUSTAND'].isin(chosen_strassen))
    filter_monat = (df['UMONAT'].isin(chosen_monat))
    filter_unterkategorie = (df['UKATEGORIE'].isin(chosen_unterkategorie))
    filter_unfallart = (df['UART'].isin(chosen_unfallart))
    filter_stunde = (df['USTUNDE'].isin(chosen_stunde))

    df_sub = df[
        filter_wochentag & filter_lichtverhaeltnisse & filter_strasse & filter_monat & filter_unterkategorie & filter_unfallart]  # & filter_stunde]

    graph3 = px.density_heatmap(df_sub,
                                labels=dict(x="Monat", y="Wochentag", color="Auswahl"),
                                x=df_sub["UMONAT"],
                                y=df_sub["UWOCHENTAG"],
                                z=df_sub[chosen_heatmap], histfunc="count",
                                marginal_x="histogram", marginal_y="histogram",
                                # color_continuous_scale = 'virdis'
                                )
    return [go.Figure(data=graph3)]


# callback home tageszeitengraph
@app.callback([Output(component_id='graph4', component_property='figure'),
               ],
              [Input('jahr', 'value'),
               Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('checklist_tageszeiten', 'value'),
               ])
def home_tageszeiten(chosen_jahr, chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse, chosen_strassen,
                     chosen_wochentag, chosen_unterkategorie, chosen_unfallart, chosen_tageszeit):
    df = set_jahr(chosen_jahr)
    filter_wochentag = (df['UWOCHENTAG'].isin(chosen_wochentag))
    filter_lichtverhaeltnisse = (df['ULICHTVERH'].isin(chosen_lichtverhaeltnisse))
    filter_strasse = (df['STRZUSTAND'].isin(chosen_strassen))
    filter_monat = (df['UMONAT'].isin(chosen_monat))
    filter_unterkategorie = (df['UKATEGORIE'].isin(chosen_unterkategorie))
    filter_unfallart = (df['UART'].isin(chosen_unfallart))
    # filter_stunde = (df['USTUNDE'].isin(chosen_stunde))
    df_sub = df[
        filter_wochentag & filter_lichtverhaeltnisse & filter_strasse & filter_monat & filter_unterkategorie & filter_unfallart]  # & filter_stunde]

    graph4 = px.bar(df_sub, x="USTUNDE", y=chosen_tageszeit, title="Tageszeiten")
    return [go.Figure(data=graph4)]


# callback jahresvergleich maps
@app.callback([Output(component_id='map_vergleich', component_property='figure'),
               ],
              [Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('vergleich_year1', 'value'),
               Input('vergleich_year2', 'value'),
               Input('checklist_vergleich_map', 'value'),
               ])
def vergleich_maps(chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse, chosen_strassen, chosen_wochentag,
                   chosen_unterkategorie, chosen_unfallart, chosen_jahr1, chosen_jahr2, chosen_vergleich):
    df_map1 = set_jahr(chosen_jahr1)
    df_map2 = set_jahr(chosen_jahr2)

    df_sub_map1 = df_map1[
        df_map1['UWOCHENTAG'].isin(chosen_wochentag) & df_map1['ULICHTVERH'].isin(chosen_lichtverhaeltnisse) & df_map1[
            'STRZUSTAND'].isin(chosen_strassen) & df_map1['UMONAT'].isin(chosen_monat) & df_map1['UKATEGORIE'].isin(
            chosen_unterkategorie) & df_map1['UART'].isin(chosen_unfallart) & df_map1['Teilnehmer'].isin(
            chosen_vergleich)]
    df_sub_map2 = df_map2[
        df_map2['UWOCHENTAG'].isin(chosen_wochentag) & df_map2['ULICHTVERH'].isin(chosen_lichtverhaeltnisse) & df_map2[
            'STRZUSTAND'].isin(chosen_strassen) & df_map2['UMONAT'].isin(chosen_monat) & df_map2['UKATEGORIE'].isin(
            chosen_unterkategorie) & df_map2['UART'].isin(chosen_unfallart) & df_map2['Teilnehmer'].isin(
            chosen_vergleich)]
    # & df_map1['USTUNDE'].isin(chosen_stunde) , & df_map2['USTUNDE'].isin(chosen_stunde)

    data_mapbox = [
        go.Scattermapbox(
            lon=df_sub_map1['XGCSWGS84'],
            lat=df_sub_map1['YGCSWGS84'],
            mode='markers',
            marker_color=df_sub_map1["color"].values,
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 25}},
            hovertext=df_sub_map1['symbol'],
            subplot='mapbox',
        ),
        go.Scattermapbox(
            lon=df_sub_map2['XGCSWGS84'],
            lat=df_sub_map2['YGCSWGS84'],
            mode='markers',
            marker_color=df_sub_map2["color"].values,
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 25}},
            hovertext=df_map2['symbol'],
            subplot='mapbox2',
        )
    ]

    # Return figure
    return [go.Figure(
        data=data_mapbox,
        layout=go.Layout(
            uirevision='foo',  # preserves state of figure/map after callback activated
            clickmode='event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                style='streets',
                center=dict(
                    lat=48.216346,
                    lon=11.158529
                ),
                pitch=0,
                zoom=8.25
            ),
            mapbox2=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                style='streets',
                center=dict(
                    lat=48.216346,
                    lon=11.158529
                ),
                pitch=0,
                zoom=8.25
            ), ))
    ]


# callback jahresvergeleich sunbursts
@app.callback([Output(component_id='sunburst_vergleich1', component_property='figure'),
               Output(component_id='sunburst_vergleich2', component_property='figure'),
               ],
              [Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('vergleich_year1', 'value'),
               Input('vergleich_year2', 'value'),
               Input('vergleich_sunburst_dropdown1', 'value'),
               # Input('vergleich_sunburst_dropdown2', 'value'),
               ])
def vergleich_sunburst(chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse, chosen_strassen, chosen_wochentag,
                       chosen_unterkategorie, chosen_unfallart, chosen_jahr1, chosen_jahr2, chosen_sunburst1):
    df_sunburst1 = set_jahr(chosen_jahr1)
    df_sunburst2 = set_jahr(chosen_jahr2)

    df_sub_sunburst1 = df_sunburst1[
        df_sunburst1['UWOCHENTAG'].isin(chosen_wochentag) & df_sunburst1['ULICHTVERH'].isin(chosen_lichtverhaeltnisse) &
        df_sunburst1['STRZUSTAND'].isin(chosen_strassen) & df_sunburst1['UMONAT'].isin(chosen_monat) & df_sunburst1[
            'UKATEGORIE'].isin(chosen_unterkategorie) & df_sunburst1['UART'].isin(chosen_unfallart)]
    df_sub_sunburst2 = df_sunburst2[
        df_sunburst2['UWOCHENTAG'].isin(chosen_wochentag) & df_sunburst2['ULICHTVERH'].isin(chosen_lichtverhaeltnisse) &
        df_sunburst2['STRZUSTAND'].isin(chosen_strassen) & df_sunburst2['UMONAT'].isin(chosen_monat) & df_sunburst2[
            'UKATEGORIE'].isin(chosen_unterkategorie) & df_sunburst2['UART'].isin(chosen_unfallart)]
    # & df_sunburst1['USTUNDE'].isin(chosen_stunde) , & df_sunburst2['USTUNDE'].isin(chosen_stunde)
    sunburst1 = px.sunburst(
        data_frame=df_sub_sunburst1,
        path=["UMONAT", 'UWOCHENTAG', "USTUNDE"],
        color=df_sub_sunburst1[chosen_sunburst1],
        color_discrete_sequence=px.colors.qualitative.Pastel,
        maxdepth=2,
    )
    sunburst1.update_traces(textinfo='label+percent parent')
    sunburst1.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    sunburst2 = px.sunburst(
        data_frame=df_sub_sunburst2,
        path=["UMONAT", 'UWOCHENTAG', "USTUNDE"],
        color=df_sub_sunburst2[chosen_sunburst1],
        color_discrete_sequence=px.colors.qualitative.Pastel,
        maxdepth=2,
    )
    sunburst2.update_traces(textinfo='label+percent parent')
    sunburst2.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    # Return figure
    return [go.Figure(data=sunburst1), go.Figure(data=sunburst2)]


# callback jahresvergleich kalender heatmap
@app.callback([Output(component_id='kalender_vergleich1', component_property='figure'),
               Output(component_id='kalender_vergleich2', component_property='figure'),
               ],
              [Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('vergleich_year1', 'value'),
               Input('vergleich_year2', 'value'),
               Input('vergleich_heatmap_dropdown1', 'value'),
               # Input('vergleich_heatmap_dropdown2', 'value'),
               ])
def vergleich_kalendar_heatmap(chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse, chosen_strassen,
                               chosen_wochentag, chosen_unterkategorie, chosen_unfallart, chosen_jahr1, chosen_jahr2,
                               chosen_heatmap1):
    df_heatmap1 = set_jahr(chosen_jahr1)
    df_heatmap2 = set_jahr(chosen_jahr2)

    df_sub_heatmap1 = df_heatmap1[
        df_heatmap1['UWOCHENTAG'].isin(chosen_wochentag) & df_heatmap1['ULICHTVERH'].isin(chosen_lichtverhaeltnisse) &
        df_heatmap1['STRZUSTAND'].isin(chosen_strassen) & df_heatmap1['UMONAT'].isin(chosen_monat) & df_heatmap1[
            'UKATEGORIE'].isin(chosen_unterkategorie) & df_heatmap1['UART'].isin(chosen_unfallart)]
    df_sub_heatmap2 = df_heatmap2[
        df_heatmap2['UWOCHENTAG'].isin(chosen_wochentag) & df_heatmap2['ULICHTVERH'].isin(chosen_lichtverhaeltnisse) &
        df_heatmap2['STRZUSTAND'].isin(chosen_strassen) & df_heatmap2['UMONAT'].isin(chosen_monat) & df_heatmap2[
            'UKATEGORIE'].isin(chosen_unterkategorie) & df_heatmap2['UART'].isin(chosen_unfallart)]
    # & df_heatmap1['USTUNDE'].isin(chosen_stunde) , & df_heatmap2['USTUNDE'].isin(chosen_stunde)
    kalender1 = px.density_heatmap(df_sub_heatmap1,
                                   labels=dict(x="Monat", y="Wochentag", color="Auswahl"),
                                   x=df_sub_heatmap1["UMONAT"],
                                   y=df_sub_heatmap1["UWOCHENTAG"],
                                   z=df_sub_heatmap1[chosen_heatmap1], histfunc="count",
                                   marginal_x="histogram", marginal_y="histogram",
                                   # color_continuous_scale = 'virdis'
                                   )
    kalender2 = px.density_heatmap(df_sub_heatmap2,
                                   labels=dict(x="Monat", y="Wochentag", color="Auswahl"),
                                   x=df_sub_heatmap2["UMONAT"],
                                   y=df_sub_heatmap2["UWOCHENTAG"],
                                   z=df_sub_heatmap2[chosen_heatmap1], histfunc="count",
                                   marginal_x="histogram", marginal_y="histogram",
                                   # color_continuous_scale = 'virdis'
                                   )

    return [go.Figure(data=kalender1), go.Figure(data=kalender2)]


# callback jahresvergleich tageszeiten
@app.callback([Output(component_id='tageszeiten_vergleich1', component_property='figure'),
               Output(component_id='tageszeiten_vergleich2', component_property='figure'),
               ],
              [Input('vergleich_year1', 'value'),
               Input('vergleich_year2', 'value'),
               Input('monat', 'value'),
               Input('stunden', 'value'),
               Input('lichtverhaeltnisse', 'value'),
               Input('strassenverhaeltnisse', 'value'),
               Input('wochentage', 'value'),
               Input('unterkategorie', 'value'),
               Input('unfallart', 'value'),
               Input('vergleich_tageszeiten_checklist', 'value'),
               ])
def vergleich_tageszeiten(chosen_jahr1, chosen_jahr2, chosen_monat, chosen_stunde, chosen_lichtverhaeltnisse,
                          chosen_strassen, chosen_wochentag, chosen_unterkategorie, chosen_unfallart, chosen_value):
    df_tageszeiten1 = set_jahr(chosen_jahr1)
    df_tageszeiten2 = set_jahr(chosen_jahr2)
    # df1 = set_jahr(chosen_jahr1)
    # df2 = set_jahr(chosen_jahr2)
    # filter_wochentag = (df['UWOCHENTAG'].isin(chosen_wochentag))
    # filter_lichtverhaeltnisse = (df['ULICHTVERH'].isin(chosen_lichtverhaeltnisse))
    # filter_strasse = (df['STRZUSTAND'].isin(chosen_strassen))
    # filter_monat = (df['UMONAT'].isin(chosen_monat))
    # filter_unterkategorie = (df['UKATEGORIE'].isin(chosen_unterkategorie))
    # filter_unfallart = (df['UART'].isin(chosen_unfallart))
    # filter_stunde = (df['USTUNDE'].isin(chosen_stunde))

    # df_tageszeiten1 = df1[filter_wochentag & filter_lichtverhaeltnisse & filter_strasse & filter_monat & filter_unterkategorie & filter_unfallart] #& filter_stunde]
    # df_tageszeiten2 = df2[filter_wochentag & filter_lichtverhaeltnisse & filter_strasse & filter_monat & filter_unterkategorie & filter_unfallart] #& filter_stunde]

    tageszeit1 = px.bar(df_tageszeiten1, x="USTUNDE", y=chosen_value, title="Tageszeiten Jahr 1")
    tageszeit2 = px.bar(df_tageszeiten2, x="USTUNDE", y=chosen_value, title="Tageszeiten Jahr 2")

    return [go.Figure(data=tageszeit1), go.Figure(data=tageszeit2)]


@app.callback([Output(component_id='trend_graph1', component_property='figure'),
               Output(component_id='trend_wochentage', component_property='figure'),
               Output(component_id='trend_monate', component_property='figure'),
               Output(component_id='trend_beleuchtung', component_property='figure'),
               Output(component_id='trend_strassen', component_property='figure'),
               ],
              [Input('trend_dropdown1', 'value'),
               Input('trend_wochentage_dropdown', 'value'),
               Input('trend_monate_dropdown', 'value'),
               Input('trend_beleuchtung_dropdown', 'value'),
               Input('trend_strassen_dropdown', 'value'),
               ])
def trend_graph1(chosen_trend, chosen_trend1, chosen_trend2, chosen_trend3, chosen_trend4):
    trend2 = px.area(df_trend, x="Jahr", y=chosen_trend, color="Teilnehmer", line_group="Teilnehmer")
    # trend2.update_yaxes(range = [0,50000])
    wochentage = px.area(df_trend, x="Jahr", y=chosen_trend1, color="Teilnehmer", line_group="Teilnehmer")
    # wochentage.update_yaxes(range = [0,50000])
    monate = px.area(df_trend, x="Jahr", y=chosen_trend2, color="Teilnehmer", line_group="Teilnehmer")
    # monate.update_yaxes(range = [0,50000])
    beleuchtung = px.area(df_trend, x="Jahr", y=chosen_trend3, color="Teilnehmer", line_group="Teilnehmer")
    # beleuchtung.update_yaxes(range = [0,50000])
    strassen = px.area(df_trend, x="Jahr", y=chosen_trend4, color="Teilnehmer", line_group="Teilnehmer")
    # strassen.update_yaxes(range = [0,50000])
    return [go.Figure(data=trend2), go.Figure(data=wochentage), go.Figure(data=monate), go.Figure(data=beleuchtung),
            go.Figure(data=strassen)]


@app.callback([Output(component_id='trend_treemap1', component_property='figure'),
               Output(component_id='trend_treemap2', component_property='figure'),
               Output(component_id='trend_treemap3', component_property='figure'),
               Output(component_id='trend_treemap4', component_property='figure'),
               Output(component_id='trend_treemap5', component_property='figure'),
               Output(component_id='trend_treemap6', component_property='figure'),
               ],
              [Input('trend_treemap_dropdown', 'value'),
               ])
def trend_treemap(chosen_treemap):
    df_treemap16 = df_treemap.query("Jahr == 2016")
    df_treemap17 = df_treemap.query("Jahr == 2017")
    df_treemap18 = df_treemap.query("Jahr == 2018")
    df_treemap19 = df_treemap.query("Jahr == 2019")
    df_treemap20 = df_treemap.query("Jahr == 2020")
    df_treemap21 = df_treemap.query("Jahr == 2021")

    treemap1 = px.treemap(df_treemap16, path=[px.Constant("IstRad"), 'Jahr', 'Monat', 'Wochentag'],
                          color=chosen_treemap, hover_data=['Monat'],
                          color_continuous_scale='blues')
    # treemap1.update_yaxes(range = [0,4000])
    treemap2 = px.treemap(df_treemap17, path=[px.Constant("IstRad"), 'Jahr', 'Monat', 'Wochentag'],
                          color=chosen_treemap, hover_data=['Monat'],
                          color_continuous_scale='blues')
    # treemap2.update_yaxes(range = [0,4000])
    treemap3 = px.treemap(df_treemap18, path=[px.Constant("IstRad"), 'Jahr', 'Monat', 'Wochentag'],
                          color=chosen_treemap, hover_data=['Monat'],
                          color_continuous_scale='blues')
    # treemap3.update_yaxes(range = [0,4000])
    treemap4 = px.treemap(df_treemap19, path=[px.Constant("IstRad"), 'Jahr', 'Monat', 'Wochentag'],
                          color=chosen_treemap, hover_data=['Monat'],
                          color_continuous_scale='blues')
    # treemap4.update_yaxes(range = [0,4000])
    treemap5 = px.treemap(df_treemap20, path=[px.Constant("IstRad"), 'Jahr', 'Monat', 'Wochentag'],
                          color=chosen_treemap, hover_data=['Monat'],
                          color_continuous_scale='blues')
    # treemap5.update_yaxes(range = [0,4000])
    treemap6 = px.treemap(df_treemap21, path=[px.Constant("IstRad"), 'Jahr', 'Monat', 'Wochentag'],
                          color=chosen_treemap, hover_data=['Monat'],
                          color_continuous_scale='blues')
    # treemap6.update_yaxes(range = [0,4000])

    return [go.Figure(data=treemap1), go.Figure(data=treemap2), go.Figure(data=treemap3), go.Figure(data=treemap4),
            go.Figure(data=treemap5), go.Figure(data=treemap6)]


if __name__ == '__main__':
    app.run(debug=False)



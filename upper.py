from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import linregress

df = pd.read_parquet('all_matabolites_7_11_22.parquet.gzip')
list_metabolites = df.Metabolite.unique()
metabo2 = 'Alanine'
app = Dash(__name__, )
app.title = 'Metabolite'
upper_layout = html.Div([



    html.Div([
        html.Div([
            html.P('Select Metabolie:', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='metabo2',
                         multi=False,
                         clearable=False,
                         disabled=False,
                         style={'display': True},
                         value='Alanine',
                         placeholder='Select Matabolite',
                         options=[{'label': c, 'value': c}
                                  for c in list_metabolites], className='dcc_compon'),

            html.P('Select Repetition:', className='fix_label',
                   style={'color': 'white'}),
            dcc.RadioItems(id='reps2',
                           inline=True,
                           labelStyle={
                               'padding-left': 20, },

                           options=[],
                           className='dcc_compon'),


            html.P('Select Concentration:', className='fix_label', style={
                   'color': 'white', 'margin-left': '1%'}),

            dcc.RangeSlider(id='select_conc2',
                            min=0,
                            max=500,
                            tooltip={"placement": "topLeft",
                                     "always_visible": True},
                            value=[0, 500],
                            updatemode='drag'),

            html.P('The Concentration:', className='fix_label', style={
                   'color': 'white', 'margin-left': '1%'}),

             html.P(id='list_rep_conc2', className='fix_label', style={
                 'color': 'white',  'fontSize': 14, 'margin-left': '1%'}),

             html.P('Select Time:', className='fix_label', style={
                 'color': 'white', 'margin-left': '1%'}),

             dcc.RangeSlider(id='select_time_up',
                             min=0,
                             max=60,
                             step=5,
                             tooltip={"placement": "topLeft",
                                      "always_visible": True},
                             value=[0, 60],
                             updatemode='drag'),

             html.P('Select:  ', className='fix_label', style={
                 'color': 'white', 'margin-left': '1%'}),
             html.Div([
                 html.Div(['Regression', dcc.Input(id='range1', type='number', min=2, max=12,
                                                   step=1, value=5)]),
                 html.Div(['Length', dcc.Input(
                     id='range2', type='number', min=0, max=20, step=1, value=2, )]),
                 html.Div(['Percent', dcc.Input(
                     id='range3', type='number', min=5, max=100, step=5, value=25, )]),
                 html.Div(['Mean', dcc.Input(id='range4', type='number', min=0.1, max=5,
                                             step=0.1, value=0.5, )]),
             ], className='input_range'),
             #  html.Pre('  A      B      C     D', className='pre_label', style={
             #      'color': 'white', 'margin-left': '1%'}),

             ], className="create_container three columns"),

        ####################################################################################################


        html.Div([
            dcc.Graph(id='scatter_chart_up1',
                      config={'displayModeBar': 'hover'},
                      style={"height": "100%", "width": "100%", }),

        ], className="create_container six columns"),

        html.Div([
            # dcc.Graph(id='pie_chart',
            #           config={'displayModeBar': 'hover'}),
            html.Iframe(
                id='frame', src="https://pubchem.ncbi.nlm.nih.gov/compound/"+metabo2+"#section=3D-Conformer&embed=true",
                style={"height": "100%", "width": "100%", }),
        ], className="create_container three columns"),

    ], className="row flex-display"),
    ##############################################################################################
    #                                   end of first row
    ##############################################################################################
    html.Div([
        html.Div([
            dcc.Graph(id='chart_up2',
                      config={'displayModeBar': 'hover'},
                      clickData={'points': [{'x': 0}, {'x': 0}]}),


        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='chart_up3',
                      config={'displayModeBar': 'hover'},
                      clickData={'points': [{'x': 0}, {'x': 0}]}),

        ], className="create_container six columns"),

    ], className="row flex-display"),

    ##############################################################################################
    #                                   end of second row
    ##############################################################################################

    html.Div([
        html.Div([
            dcc.Graph(id='chart_up4',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='chart_up5',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

    ], className="row flex-display"),

    ##############################################################################################
    #                                   end of third row
    ##############################################################################################


], id="mainContainer", style={"display": "flex", "flex-direction": "column"})

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go


df = pd.read_parquet('all_matabolites_7_11_22.parquet.gzip')
list_metabolites = df.Metabolite.unique()

app = Dash(__name__, )
app.title = 'Metabolite'
explor_layout = html.Div([



    html.Div([
        html.Div([
            html.P('Select Metabolie:', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='metabo',
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
            dcc.RadioItems(id='reps',
                           inline=True,
                           labelStyle={
                               'padding-left': 20},
                           options=[],
                           className='dcc_compon'),


            html.P('Select Concentration:', className='fix_label', style={
                   'color': 'white', 'margin-left': '1%'}),

            dcc.RangeSlider(id='select_conc',
                            min=0,
                            max=500,
                            tooltip={"placement": "topLeft",
                                     "always_visible": True},
                            value=[0, 500],
                            updatemode='drag'),

            html.P('The Concentration:', className='fix_label', style={
                   'color': 'white', 'margin-left': '1%'}),

             html.P(id='list_rep_conc', className='fix_label', style={
                 'color': 'white',  'fontSize': 14, 'margin-left': '1%'}),

             ], className="create_container three columns"),

        ####################################################################################################


        html.Div([
            dcc.Graph(id='scatter_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='pie_chart',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container three columns"),

    ], className="row flex-display"),
    ##############################################################################################
    #                                   end of first row
    ##############################################################################################
    html.Div([
        html.Div([
            dcc.Graph(id='chart_2',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='chart_3',
                      config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

    ], className="row flex-display"),


    ##############################################################################################
    #                                   end of second row
    ##############################################################################################
    html.Div([

        html.Div([
            dcc.Graph(id='chart_ex4',
                      config={'displayModeBar': 'hover'},

                      ),

        ], className="create_container twelve columns"),

    ], className="row flex-display"),


], id="mainContainer", style={"display": "flex", "flex-direction": "column"})

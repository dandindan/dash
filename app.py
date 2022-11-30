from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go


df = pd.read_csv('30_11_22.csv')


def set_dtypes(df):
    df['Time'] = df['Time'].astype('float32')
    # ###df['Strain'] = df['Strain'].astype('category')
    df['Strain'] = df['Strain'].astype('str')
    df['Metabolite'] = df['Metabolite'].astype('category')
    df['Concentration'] = df['Concentration'].astype('float32')
    df['Date'] = df['Date'].astype('category')
    # ####df["Date"] = pd.to_datetime(df["Date"], format='%d%m%y')
    df['Number'] = df['Number'].astype('int32')
    # ###df['Number'] = df['Number'].astype('category')
    df['OD600'] = df['OD600'].astype('float32')
    return df


df = set_dtypes(df)  # set datatypes


list_metabolites = df.Metabolite.unique()

app = Dash(__name__, )
server = app.server

app.title = 'Metabolite'
app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H2('Metabolite Upper Limit!', style={
                        "margin-bottom": "0px", 'color': 'white'}),
                html.H4('2021-2023',
                        style={"margin-top": "0px", 'color': 'white'}),

            ]),
        ], className="six column", id="title")

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

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

], id="mainContainer", style={"display": "flex", "flex-direction": "column"})


# changes the radio button acording to the dropdown


@ app.callback(
    Output('reps', 'options'),
    Input('metabo', 'value'))
def get_reps_options(metabo):
    df_met = df.loc[df["Metabolite"] == metabo].sort_values(
        by='Number', ascending=True)
    return [{'label': i, 'value': i} for i in df_met['Number'].unique()]

# returns the value of the radio button with the first repitition  ##############################################################


@ app.callback(
    Output('reps', 'value'),
    Input('reps', 'options'))
def get_reps_value(reps):
    return [k['value'] for k in reps][0]


# slider callback ##############################################################
@ app.callback(
    Output('select_conc', 'value'),
    Output('select_conc', 'min'),
    Output('select_conc', 'max'),
    Output('list_rep_conc', 'children'),
    Input('metabo', 'value'),
    Input('reps', 'value'))
def get_conc_value(metabo, reps):
    if metabo:
        df_met = df.loc[(df["Metabolite"] == metabo) & (df['Number'] == reps)]
        df_met_conc = df_met['Concentration'].unique()[0:]
        global df_met_print
        df_met_print = df_met['Concentration'].unique()
        # [{'label': i, 'value': i} for i in df_met['Number'].unique()]
        lower = min(df_met['Concentration'].unique())
        upper = max(df_met['Concentration'].unique())
        concetration_string = ' , '.join(df_met_print.astype(str))

    return df_met_conc, lower, upper, concetration_string
    # Create scatterplot chart


@ app.callback(Output('scatter_chart', 'figure'),
               [Input('metabo', 'value')],
               [Input('reps', 'value')],
               [Input('select_conc', 'value')])
def update_graph(metabo, reps, select_conc):
    # Data for scatter plot

    plot_data = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Concentration'] >= min(select_conc)) & (df['Concentration'] <= max(select_conc))]
    fig = px.scatter(plot_data, x="Time",
                     y="OD600",
                     color="Strain",
                     hover_name="Concentration",
                     # marginal_y='histogram',
                     # marginal_y='violin',
                     range_y=[-.1, 1.8],
                     labels={
                         "Time": "Time(h)",
                         "OD600": "Abs(OD600)",
                     },
                     template="plotly_dark",
                     animation_frame="Concentration",
                     animation_group="OD600"
                     )
    fig.update_layout(
        yaxis=dict(
            tickmode='linear',
            dtick=0.4
        )
    )
    fig.update_layout(
        title={
            'text': metabo,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig

# pie chart#######################################################


@ app.callback(Output('pie_chart', 'figure'),
               [Input('metabo', 'value')])
def update_graph(metabo):
    plot_data = df.loc[(df["Metabolite"] == metabo)].sort_values(
        by='Number', ascending=True)

    fig = px.pie(plot_data,  names='Number', template="plotly_dark",
                 color='Number', hole=.4, title=f'% reps {metabo}')  # hover_name=df.value_counts())
    fig.update_traces(textposition='outside', textinfo='percent+label+value')
    fig.update_layout(legend=dict(orientation='h'))

    return fig


@ app.callback(Output('chart_2', 'figure'),
               [Input('metabo', 'value')])
def update_graph(metabo):
    plot_data = df.loc[(df["Metabolite"] == metabo)].sort_values(
        by='Number', ascending=True)

    fig = px.histogram(plot_data,  x='Concentration', barmode='relative', template="plotly_dark",
                       color='Number', title=f' {metabo}', nbins=200)  # hover_name=df.value_counts())
    # fig.update_traces(textposition='outside', textinfo='percent+label+value')
    fig.update_layout(legend_title="Repeat")
    fig.update_xaxes(nticks=20)

    return fig


@ app.callback(Output('chart_3', 'figure'),
               [Input('metabo', 'value')])
def update_graph(metabo):
    plot_data = df.loc[(df["Metabolite"] == metabo)].sort_values(
        by='Number', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Violin(x=plot_data['Number'][plot_data['Strain'] == 'WT'],
                            y=plot_data['Concentration'][plot_data['Strain'] == 'WT'],
                            legendgroup='WT', scalegroup='WT', name='WT',
                            side='positive', meanline_visible=True,
                            line_color='#636EFA'))
    fig.add_trace(go.Violin(x=plot_data['Number'][plot_data['Strain'] == '152'],
                            y=plot_data['Concentration'][plot_data['Strain'] == '152'],
                            legendgroup='152', scalegroup='152', name='152',
                            side='negative', meanline_visible=True,
                            line_color='#EF553B'))
    fig.update_layout(template="plotly_dark", title=f' {metabo}',
                      xaxis_title="# Repeat",
                      yaxis_title="Concentration(mM)",
                      legend_title="Strain",)
    fig.update_traces(meanline_visible=True,
                      # points='all',  # show all points
                      # jitter=0.05,  # add some jitter on points for better visibility
                      scalemode='count')  # scale violin plot area with total count
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

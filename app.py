from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import linregress
import time

from upper import upper_layout
from explor import explor_layout

df = pd.read_csv('7_12_22.csv')
loading_style = {'position': 'absolute', 'align-self': 'center'}


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
metabo = 'Alanine'
app = Dash(__name__, )
server = app.server

app.title = 'Metabolite'

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {

    "color": '#AEAEAE',
    "fontSize": '.9vw',
    "backgroundColor": '#010914',
    'border-bottom': '1px white solid',
    'border-radius': '30px 30px 0px 0px',

}

tab_selected_style = {
    "fontSize": '.9vw',
    "color": '#F4F4F4',

    'fontWeight': 'bold',
    "backgroundColor": '#566573',
    'border-top': '1px white solid',
    'border-left': '1px white solid',
    'border-right': '1px white solid',
    'border-radius': '30px 30px 0px 0px',
}


app.layout = html.Div([


    html.Div([
        html.H1('Metabolite Upper Limit', style={
            "margin-bottom": "20px", 'color': 'white'}),
        html.H3('2021-2023',
                style={"margin-top": "10px", 'color': 'white'}),

    ], className="six column", id="title"),

    html.Div([
        dcc.Tabs(value='Upper limit', children=[
            dcc.Tab(upper_layout,
                    label='Upper limit',
                    value='Upper limit',
                    style=tab_style,
                    selected_style=tab_selected_style,
                    className='font_size'),
            dcc.Tab(explor_layout,
                    label='Exploratory Data',
                    value='Exploratory Data',
                    style=tab_style,
                    selected_style=tab_selected_style,
                    className='font_size'),
            dcc.Tab(
                label='Empty Tab',
                value='Empty Tab',
                style=tab_style,
                selected_style=tab_selected_style,
                className='font_size'),
        ], style=tabs_styles,

            colors={"border": None,
                    "primary": None,
                    }, className='tabs_width')

    ], id='div_color', className='create_container twelve columns')], className='outer_div', style={"display": "flex", "flex-direction": "column"})


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

        global df_met_print
        df_met_print = df_met['Concentration'].unique()
        # [{'label': i, 'value': i} for i in df_met['Number'].unique()]
        lower = min(df_met['Concentration'].unique())
        upper = max(df_met['Concentration'].unique())
        concetration_string = ' , '.join(df_met_print.astype(str))
        df_met_conc = [lower, upper]

    return df_met_conc, lower, upper, concetration_string

 #############################################################################################
    # Create scatterplot chart


@ app.callback([Output('scatter_chart', 'figure')],
               [Output('load_icon', 'parent_style')],
               [Input('metabo', 'value')],
               [Input('reps', 'value')],
               [Input('select_conc', 'value')])
def update_graph(metabo, reps, select_conc):
    # Data for scatter plot
    new_loading_style = loading_style
    time.sleep(1)
    plot_data = df.loc[(df["Metabolite"] == metabo) & (
        df['Number'] == reps) & (df['Concentration'] >= min(select_conc)) & (df['Concentration'] <= max(select_conc))]
    fig = px.scatter(plot_data, x="Time",
                     y="OD600",
                     color="Strain",
                     #  symbol='Concentration',
                     hover_name="Concentration",
                     marginal_y='histogram',
                     # marginal_y='violin',
                     #  marginal_y='box',
                     # range_y=[-.1, 1.8],
                     labels={
                         "Time": "Time(h)",
                         "OD600": "Abs(OD600)",
                     },
                     template="plotly_dark",
                     #  animation_frame="Concentration",
                     #  animation_group="OD600"
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

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=0.9))

    fig.update_traces(
        marker=dict(size=6, line=dict(width=0.1, color='white')),
        selector=dict(mode="markers"))

    return fig, new_loading_style


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


@ app.callback(Output('chart_ex4', 'figure'),
               [Input('metabo', 'value')])
def update_graph(metabo):

    fig = px.box(df,
                 x='Metabolite',
                 y='Concentration',
                 range_y=[0, 500],
                 template="plotly_dark",
                 # template="seaborn",
                 # symbol="Number",
                 color='Number',
                 # barmode='group',
                 hover_name=('OD600'),
                 height=600,
                 )

    # fig.update_traces(mode='markers', marker_line_width=1,
    #                   marker_size=10, opacity=1)
    fig.update_layout(title="Metabolite Concentration distribution")


#    fig.update_xaxes(rangeslider_visible=True)
    return fig


@ app.callback(
    Output('reps2', 'options'),
    Input('metabo2', 'value'))
def get_reps_options(metabo2):
    df_met = df.loc[df["Metabolite"] == metabo2].sort_values(
        by='Number', ascending=True)
    return [{'label': i, 'value': i} for i in df_met['Number'].unique()]


# returns the value of the radio button with the first repitition

@ app.callback(
    Output('reps2', 'value'),
    Input('reps2', 'options'))
def get_reps_value(reps2):
    return [k['value'] for k in reps2][0]


# concentration slider callback
@ app.callback(
    Output('select_conc2', 'value'),
    Output('select_conc2', 'min'),
    Output('select_conc2', 'max'),
    Output('list_rep_conc2', 'children'),
    Input('metabo2', 'value'),
    Input('reps2', 'value'))
def get_conc_value(metabo2, reps2):
    if metabo2:
        df_met = df.loc[(df["Metabolite"] == metabo2)
                        & (df['Number'] == reps2)]
        # df_met_conc = df_met['Concentration'][0][-1]
        global df_met_print
        df_met_print = df_met['Concentration'].unique()
        # [{'label': i, 'value': i} for i in df_met['Number'].unique()]
        lower = min(df_met['Concentration'].unique())
        upper = max(df_met['Concentration'].unique())
        concetration_string = ' , '.join(df_met_print.astype(str))
        df_met_conc = [lower, upper]

    return df_met_conc, lower, upper, concetration_string

    # Create scatterplot chart
###################################################################
####                         scatter chart       #1            ####
###################################################################


@ app.callback(Output('scatter_chart_up1', 'figure'),
               [Input('metabo2', 'value')],
               [Input('reps2', 'value')],
               [Input('select_conc2', 'value')],
               [Input('select_time_up', 'value')])
def update_graph(metabo2, reps2, select_conc2, select_time_up):
    # Data for scatter plot

    plot_data = df.loc[(df["Metabolite"] == metabo2) & (df['Number'] == reps2) & (df['Concentration'] >= min(select_conc2)) & (
        df['Concentration'] <= max(select_conc2)) & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]
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
            'text': metabo2,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig

###################################################################
####                       Molecule display                    ####
###################################################################


@ app.callback(Output('frame', 'src'),
               [Input('metabo2', 'value')],)
def update_graph(metabo2):
    if metabo2 == 'AspaticAcid':
        metabo2 = 'Aspartic Acid'
    else:
        metabo2 = metabo2

    if metabo2 == 'Tymine':
        metabo2 = 'Thymine'
    else:
        metabo2 = metabo2

    if metabo2 == 'Tryptopan':
        metabo2 = 'Tryptophan'
    else:
        metabo2 = metabo2

    if metabo2 == 'Adenine Hemi':
        metabo2 = 'Adenine'
    else:
        metabo2 = metabo2

    return f'https://pubchem.ncbi.nlm.nih.gov/compound/{metabo2}#section=3D-Conformer&embed=true'


###################################################################
####                        linear chart   #2                  ####
###################################################################


@ app.callback(Output('chart_up2', 'figure'),
               [Input('metabo2', 'value'),
               Input('reps2', 'value'),
               Input('range1', 'value'),
               Input('range3', 'value'),
               Input('select_time_up', 'value')])
def update_graph(metabo2, reps2, range1, range3, select_time_up):
    plot_data = df.loc[(df["Metabolite"] == metabo2) & (
        df['Number'] == reps2) & (df['Strain'] == 'WT') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]
    plot_data_152 = df.loc[(df["Metabolite"] == metabo2) & (
        df['Number'] == reps2) & (df['Strain'] == '152') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]
    upper_title = ''

    def find_slope(x, y):
        slope = 0
        w = range1
        for t in range(0, x.size-w):
            x_t, y_t = x[t:t+w], y[t:t+w]
            res = linregress(x_t, y_t)
            if res.slope > slope:
                slope = res.slope
        return slope

    all_slopes = []
    all_slopes_152 = []
    con = plot_data.Concentration.unique()

    for i in range(0, len(con)):
        # conc=con[i]
        in_plot_data = plot_data.loc[plot_data['Concentration'] == con[i]]
        in_plot_data_152 = plot_data_152.loc[plot_data_152['Concentration'] == con[i]]

        x = in_plot_data['Time'].values
        y = in_plot_data['OD600'].values

        x_152 = in_plot_data_152['Time'].values
        y_152 = in_plot_data_152['OD600'].values

        alls = find_slope(x, y)
        alls_152 = find_slope(x_152, y_152)

        all_slopes.append(alls)
        all_slopes_152.append(alls_152)

    percent = range3/100

    try:
        y_line = max(all_slopes)*percent
    except ValueError:
        y_line = 0

    try:
        y_line_152 = max(all_slopes_152)*percent
    except ValueError:
        y_line_152 = 0

    # y_line_152 = max(all_slopes_152)*0.25
    # y_line_152 = np.percentile(all_slopes, 25)# return the percentile of the list
    # list_all_slopes = all_slopes.tolist()
    # upper_limit = filter(lambda x: x > list_all_slopes, y_line)
    # print(upper_limit)
    upper_limit = [i for i in all_slopes if i <= y_line]
    # for i in all_slopes:
    #     if i <=y_line:
    if upper_limit:

        index = [n for n, i in enumerate(all_slopes) if i < y_line][0]

        upper_title = f'  The upper limit is between {con[index-1]} and {con[index]}mM'

    else:

        upper_title = 'There is NO Upper Limit!!!'

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=con, y=all_slopes,
                             mode='lines+markers', name='WT',
                             marker=dict(
                                 symbol="cross",
                                 size=10,

                             ),))

    fig.add_trace(go.Scatter(x=con, y=all_slopes_152,
                             mode='lines+markers', name='152',
                             marker=dict(
                                 symbol="cross",
                                 size=10,

                             ),))

    fig.update_layout(

        title=metabo2+" #"+str(reps2)+" "+upper_title+" ",
        template="plotly_dark",
        xaxis_title="Concentration(mM)",
        yaxis_title="Slope",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))
    # fig.update_traces(
    #     marker=dict(size=8, symbol="diamond", line=dict(
    #         width=2, color="DarkSlateGrey")),
    #     selector=dict(mode="markers"),)
    fig.add_hline(y=y_line, line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Min Slope + "+str(range3) + "% = "+str(round(y_line, 4)), annotation_position="bottom right")

    fig.add_hline(y=y_line_152, line_width=3, line_dash="dot", line_color='#EF553B', name='152-Line',
                  annotation_text="   152 Min Slope +"+str(range3) + "% = "+str(round(y_line_152, 4)), annotation_position="top right")

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig


###################################################################
####                          logaritmic chart    #3           ####
###################################################################


@ app.callback(Output('chart_up3', 'figure'),
               [Input('metabo2', 'value'),
               Input('reps2', 'value'),
                Input('range1', 'value'),
               Input('range3', 'value'),
               Input('range4', 'value'),
               Input('select_time_up', 'value')])
def update_graph(metabo2, reps2, range1, range3, range4, select_time_up):
    plot_data = df.loc[(df["Metabolite"] == metabo2) & (
        df['Number'] == reps2) & (df['Strain'] == 'WT') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]
    plot_data_152 = df.loc[(df["Metabolite"] == metabo2) & (
        df['Number'] == reps2) & (df['Strain'] == '152') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]

    upper_title = ''

    def find_slope(x, y):
        slope = 0
        w = range1
        z = range4
        for t in range(0, x.size-w):
            x_t, y_t = x[t:t+w], y[t:t+w]
            res = linregress(x_t, y_t)
            if abs(sum(y_t))/w < z and res.slope > slope:
                slope = res.slope
        return slope

    all_slopes = []
    all_slopes_152 = []
    con = plot_data.Concentration.unique()

    for i in range(0, len(con)):
        # conc=con[i]
        in_plot_data = plot_data.loc[plot_data['Concentration'] == con[i]]
        in_plot_data_152 = plot_data_152.loc[plot_data_152['Concentration'] == con[i]]

        x = in_plot_data['Time'].values
        y = np.log(abs(in_plot_data['OD600'].values))

        x_152 = in_plot_data_152['Time'].values
        y_152 = np.log(abs(in_plot_data_152['OD600'].values))

        alls = find_slope(x, y)
        alls_152 = find_slope(x_152, y_152)

        all_slopes.append(alls)
        all_slopes_152.append(alls_152)

    percent = range3/100

    try:
        y_line = max(all_slopes)*percent
    except ValueError:
        y_line = 0

    try:
        y_line_152 = max(all_slopes_152)*percent
    except ValueError:
        y_line_152 = 0

    upper_limit = [i for i in all_slopes if i <= y_line]

    if upper_limit:

        index = [n for n, i in enumerate(all_slopes) if i < y_line][0]

        upper_title = f'  The upper limit is between {con[index-1]} and {con[index]}mM'

    else:

        upper_title = 'There is NO Upper Limit!!!'
    # y_line_152 = max(all_slopes_152)*0.25
    # y_line_152 = np.percentile(all_slopes, 25)# return the percentile of the list
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=con, y=all_slopes,
                             mode='lines+markers', name='WT',
                             marker=dict(
                                 symbol="cross",
                                 size=10,

                             ),))

    fig.add_trace(go.Scatter(x=con, y=all_slopes_152,
                             mode='lines+markers', name='152',
                             marker=dict(
                                 symbol="cross",
                                 size=10,

                             ),))

    fig.update_layout(

        title=metabo2+" #"+str(reps2) +
        " logaritmic scale - ln = log e "+upper_title,
        template="plotly_dark",
        xaxis_title="Concentration(mM)",
        yaxis_title="Slope",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))

    fig.add_hline(y=y_line, line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Min Slope +" + str(range3) + "% = "+str(round(y_line, 4)), annotation_position="bottom right")

    fig.add_hline(y=y_line_152, line_width=3, line_dash="dot", line_color='#EF553B', name='152-Line',
                  annotation_text="   152 Min Slope +" + str(range3)+"% = "+str(round(y_line_152, 4)), annotation_position="top right")

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig

###################################################################
####                          linear chart #4                  ####
###################################################################


@ app.callback(Output('chart_up4', 'figure'),
               [Input('metabo2', 'value'),
               Input('reps2', 'value'),
               Input('range1', 'value'),
               Input('range2', 'value'),
               Input('select_time_up', 'value'),
               Input('chart_up2', 'clickData')])
def update_graph(metabo2, reps2, range1, range2, select_time_up, clickData):

    plot_data = df.loc[(df["Metabolite"] == metabo2) & (df['Concentration'] == (clickData['points'][0]['x'])) & (df['Number'] == reps2) & (
        df['Strain'] == 'WT') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]

    plot_data_152 = df.loc[(df["Metabolite"] == metabo2) & (df['Concentration'] == (clickData['points'][1]['x'])) & (df['Number'] == reps2) & (
        df['Strain'] == '152') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]

    conc_value = str(clickData['points'][1]['x'])

    x = plot_data['Time'].values
    y = plot_data['OD600'].values

    x_152 = plot_data_152['Time'].values
    y_152 = plot_data_152['OD600'].values

    slope = 0
    w = range1
    extend_line = range2
    t_slope = 0
    for t in range(0, x.size-w):
        x_t, y_t = x[t:t+w], y[t:t+w]
        res = linregress(x_t, y_t)
        if res.slope > slope:
            slope = res.slope
            intercept = res.intercept
            t_slope = t

        x_range = np.arange(x[t_slope]-extend_line, x[t_slope]+extend_line)

    # print(clickData['points'][0]['x'])
    # print(type(clickData))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,

                             ),))
    fig.add_trace(go.Scatter(x=x_152, y=y_152,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,

                             ),))
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=intercept + slope * x_range,
            name='y='+str(round(slope, 3))+'X'+str(round(intercept, 3)),
            mode='lines+markers'))

    fig.add_vline(x=x[t_slope], line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Slope = "+str(round(x[t_slope], 4)), annotation_position="top left")

    fig.update_layout(

        title=metabo2+" #"+str(reps2) +
        " linear scale  Concentration "+conc_value+' mM',
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="ln(OD600)",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig

###################################################################
####                          logaritmic chart  #5             ####
###################################################################


@ app.callback(Output('chart_up5', 'figure'),
               [Input('metabo2', 'value'),
               Input('reps2', 'value'),
               Input('range1', 'value'),
               Input('range2', 'value'),
               Input('range4', 'value'),
               Input('select_time_up', 'value'),
               Input('chart_up3', 'clickData')])
def update_graph(metabo2, reps2, range1, range2, range4, select_time_up, clickData):

    plot_data = df.loc[(df["Metabolite"] == metabo2) & (df['Concentration'] == (clickData['points'][0]['x'])) & (df['Number'] == reps2) & (
        df['Strain'] == 'WT') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]

    plot_data_152 = df.loc[(df["Metabolite"] == metabo2) & (df['Concentration'] == (clickData['points'][1]['x'])) & (df['Number'] == reps2) & (
        df['Strain'] == '152') & (df['Time'] >= min(select_time_up)) & (df['Time'] <= max(select_time_up))]

    conc_value = str(clickData['points'][1]['x'])

    x = plot_data['Time'].values
    y = np.log(abs(plot_data['OD600'].values))

    x_152 = plot_data_152['Time'].values
    y_152 = np.log(abs(plot_data_152['OD600'].values))

    x_range = []
    t_slope = []
    intercept = 0
    slope = 0
    w = range1
    z = range4
    extend_line = range2
    t_slope = 0
    for t in range(0, x.size-w):
        x_t, y_t = x[t:t+w], y[t:t+w]
        res = linregress(x_t, y_t)
        if abs(sum(y_t))/w < z and res.slope > slope:
            slope = res.slope
            intercept = res.intercept
            t_slope = t

        x_range = np.arange(x[t_slope]-extend_line, x[t_slope]+(extend_line))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,

                             ),))
    fig.add_trace(go.Scatter(x=x_152, y=y_152,
                             mode='markers+lines', name='WT',
                             marker=dict(
                                 symbol="circle",
                                 size=5,

                             ),))
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=intercept + slope * x_range,
            name='y='+str(round(slope, 3))+'X'+str(round(intercept, 3)),
            mode='lines+markers'))

    fig.add_vline(x=x[t_slope], line_width=3, line_dash="dash", line_color='#636EFA', name='WT-Line',
                  annotation_text="   WT Slope = "+str(round(x[t_slope], 4)), annotation_position="top left")

    fig.update_layout(

        title=metabo2+" #"+str(reps2) +
        " logaritmic scale - ln = log e  Concentration "+conc_value+' mM',
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="ln(OD600)",
        legend_title="Strain",)
    # font=dict(family="Courier New, monospace", size=14, color="white"))

    fig.update_layout(autotypenumbers='convert types', hovermode='x')
    fig.update_xaxes(showspikes=True, spikecolor="green",
                     spikesnap="hovered data", spikemode="across")
    fig.update_yaxes(showspikes=False)
    return fig


# app_tabs = html.Div(
#     [
#         dbc.Tabs(
#             [
#                 dbc.Tab(label="upper", tab_id="upper-mentions", style=tab_style,
#                         active_tab_style=tab_selected_style,
#                         className='font_size'
#                         ),
#                 dbc.Tab(label="explor", tab_id="explor_mentions", style=tab_style,
#                         active_tab_style=tab_selected_style,
#                         className='font_size'
#                         ),

#             ],
#             id="tabs",
#             active_tab="upper-mentions",
#         ),
#     ]
# )

# app.layout = dbc.Container([
#     # html.Div([
#     #     html.Div([
#     #         html.Div([
#     #             html.H2('Metabolite Upper Limit', style={
#     #                 "margin-bottom": "0px", 'color': 'white'}),
#     #             html.H4('2021-2023',
#     #                     style={"margin-top": "0px", 'color': 'white'}),

#     #         ]),
#     #     ], className="twelve column", id="title")

#     # ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),


#     html.Div(app_tabs),
#     html.Div(id='content', children=[])

# ])


# @app.callback(
#     Output("content", "children"),
#     [Input("tabs", "active_tab")]
# )
# def switch_tab(tab_chosen):
#     if tab_chosen == "upper-mentions":
#         return upper_layout
#     elif tab_chosen == "explor_mentions":
#         return explor_layout

#     return html.P("This shouldn't be displayed for now...")


if __name__ == '__main__':
    app.run_server(debug=True)

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                        ],
                                value='ALL',
                                placeholder="Select Launch Site",
                                searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,
                                max=10000, step=1000,
                                marks={0: '0', 2500:'2500',5000:'5000', 7500:'7500', 10000:'10000'},
                                value=[min_payload,max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    filterd_df_class=spacex_df[spacex_df['class']==1]
    if entered_site == 'ALL':
        fig = px.pie(filterd_df_class, values='class', 
        names='Launch Site', 
        title='Total Success Launches by site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        percentage_counts = filtered_df['class'].value_counts(normalize=True) * 100
        fig = px.pie(filtered_df, 
        values=percentage_counts,
        names=percentage_counts.index,
        title=f'Total Success launches for site {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    #filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=max_payload]
    #filtered_df = filtered_df[filtered_df['Payload Mass (kg)']>=min_payload]

    if entered_site == 'ALL':
        fig = px.scatter(spacex_df,
        y='class', 
        x='Payload Mass (kg)', 
        title='Correletion between Payload Mass and Succesful landings',
        color="Booster Version Category")
        fig.update_xaxes(range=[entered_payload[0], entered_payload[1]])
        fig.update_yaxes(range=[-0.2, 1.2])
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.scatter(filtered_df,
        y='class', 
        x='Payload Mass (kg)', 
        title=f'Correletion between Payload Mass and Succesful landings for {entered_site}')
        fig.update_xaxes(range=[entered_payload[0], entered_payload[1]])
        fig.update_yaxes(range=[-0.2, 1.2])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port = 8051)

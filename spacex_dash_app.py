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

# Setting up Dropdown values
site_options_arr = ["All sites"]
for site in spacex_df['Launch Site'].unique():
    site_options_arr.append(site)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=site_options_arr, 
                                    value=site_options_arr[0],  # Default value
                                    style={'width': '210px'}
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload, max=max_payload, step=1000,
                                    value=[min_payload, max_payload] 
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    # Filter DataFrame based on selected launch site
    if selected_site == 'All sites':
        data = spacex_df.groupby('Launch Site')['class'].mean() # All sites
    else:
        data = spacex_df[spacex_df['Launch Site']==selected_site]['class'].value_counts() # Selected site
    
    # Generate a pie chart
    fig = px.pie(data, values=data.values, names=data.index, title=f'Total Success Launches By Site: {selected_site}')
    
    # Return the figure to be used in the 'success-pie-chart' Graph component
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter DataFrame based on inputs
    if selected_site == 'All sites':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])][['Launch Site', 'Payload Mass (kg)', 'class']]
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                     (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])][['Launch Site', 'Payload Mass (kg)', 'class']]

    # Generate scatter chart
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Launch Site", 
                 title=(f"Correlation between Payload and Sucess for Site: {selected_site}"))
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load data
olympic_data = pd.read_csv('Olympic_data.csv')

# Data preprocessing
medal_data = olympic_data.dropna(subset=['Medal'])

# Line Plot: Trend of total medals over the years
def create_line_plot(selected_sport):
    if selected_sport == 'All':
        filtered_data = medal_data
    else:
        filtered_data = medal_data[medal_data['Sport'] == selected_sport]

    medals_over_years = (
        filtered_data.groupby('Year')['Medal']
        .count()
        .reset_index()
    )
    return px.line(
        medals_over_years,
        x='Year',
        y='Medal',
        title=f'Total Medals Over the Years ({selected_sport})',
        markers=True,
        labels={'Year': 'Year', 'Medal': 'Total Medals'},
        color_discrete_sequence=['#FFA07A']
    )

# Bar Plot: Top 10 countries by medal count
def create_bar_plot(selected_sport):
    if selected_sport == 'All':
        filtered_data = medal_data
    else:
        filtered_data = medal_data[medal_data['Sport'] == selected_sport]

    country_medal_counts = (
        filtered_data.groupby('Team')['Medal']
        .count()
        .sort_values(ascending=False)
        .reset_index()
        .head(10)
    )
    return px.bar(
        country_medal_counts,
        x='Team',
        y='Medal',
        title=f'Top 10 Countries by Medal Count ({selected_sport})',
        labels={'Team': 'Country', 'Medal': 'Medal Count'},
        color_discrete_sequence=['#66CDAA']
    )

# Pie Chart: Gender distribution of medal winners
def create_pie_chart(selected_sport):
    if selected_sport == 'All':
        filtered_data = medal_data
    else:
        filtered_data = medal_data[medal_data['Sport'] == selected_sport]

    gender_distribution = filtered_data['Sex'].value_counts().reset_index()
    gender_distribution.columns = ['Sex', 'Count']
    return px.pie(
        gender_distribution,
        names='Sex',
        values='Count',
        title=f'Medals by Gender ({selected_sport})',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

# Dash app layout
app = dash.Dash(__name__)
sports = ['All'] + sorted(medal_data['Sport'].unique())

app.layout = html.Div(
    style={
        'backgroundImage': 'linear-gradient(to right, #4A00E0, #8E2DE2)', 
        'padding': '10px'
    },
    children=[
        html.H1('Olympics Sports Performance', style={
            'textAlign': 'center', 
            'color': '#FFFFFF',
            'marginBottom': '30px',
            'fontFamily': 'Arial, sans-serif'
        }),
        html.Div([
            html.Label('Select Sport:', style={'color': '#FFFFFF', 'fontSize': '20px'}),
            dcc.Dropdown(
                id='sport-dropdown',
                options=[{'label': sport, 'value': sport} for sport in sports],
                value='All',
                style={'backgroundColor': '#FFFFFF', 'color': '#000000'}
            ),
        ], style={
            'width': '50%', 
            'margin': '0 auto', 
            'paddingBottom': '20px',
        }),
        html.Div(
            children=[
                dcc.Graph(id='line-plot', style={'display': 'inline-block', 'width': '48%', 'border': '1px solid #FFFFFF', 'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF'}),
                dcc.Graph(id='bar-plot', style={'display': 'inline-block', 'width': '48%', 'border': '1px solid #FFFFFF', 'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF'}),
            ]
        ),
        html.Div(
            children=[
                dcc.Graph(id='pie-chart', style={'width': '50%', 'margin': '0 auto', 'border': '1px solid #FFFFFF', 'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#FFFFFF'}),
            ]
        ),
    ]
)

# Callbacks to update graphs based on dropdown selection
@app.callback(
    [
        Output('line-plot', 'figure'),
        Output('bar-plot', 'figure'),
        Output('pie-chart', 'figure')
    ],
    [Input('sport-dropdown', 'value')]
)
def update_graphs(selected_sport):
    return (
        create_line_plot(selected_sport),
        create_bar_plot(selected_sport),
        create_pie_chart(selected_sport)
    )

if __name__ == '__main__':
    app.run_server(debug=True)
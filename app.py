import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import requests
from io import StringIO

# Load your dataset directly from GitHub
url = 'https://raw.githubusercontent.com/rbolt13/StardewData/main/data-raw/items.csv'
response = requests.get(url)
df = pd.read_csv(StringIO(response.text))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Dropdown(
        id='item-dropdown',
        options=[{'label': item, 'value': item} for item in df['name']],
        value=df['name'].iloc[0]
    ),
    dcc.Input(id='quantity-input', type='number', value=1),
    html.Div(id='total-xp-output')
])

# Define callback to update total xp based on user input
@app.callback(
    Output('total-xp-output', 'children'),
    [Input('item-dropdown', 'value'),
     Input('quantity-input', 'value')]
)
def update_total_xp(selected_item, quantity):
    xp_per_item = df[df['name'] == selected_item]['xp'].iloc[0]
    total_xp = quantity * xp_per_item
    return f'Total XP: {total_xp}'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

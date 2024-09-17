import pandas as pd
import json
import yfinance as yf
from plotter import plotter
from predictor import predictor
from dash import Dash, html, dcc, Input, Output, State
from datetime import datetime, date, timedelta
import numpy as np
from df_maker import df_maker
# Load configs
with open('configs.json', 'r') as f:
    configs = json.load(f)

const = configs['const']
coef = configs['coef']
data_path = configs['data_path']
df = pd.read_csv(data_path)
date_string = '2024-07-26'
start = datetime.strptime(date_string, '%Y-%m-%d').date()
df_temp = df_maker(const, coef, start)
df = pd.concat([df, df_temp], ignore_index=True)

# Get latest BTC price and date
btc_data = yf.Ticker("BTC-USD")
latest_data = btc_data.history(period="1d")
latest_price = latest_data['Open'].iloc[0]
log2_latest_price = np.log2(latest_price)
latest_date = latest_data.index[0].strftime('%Y-%m-%d')

# Plot data
fig = plotter(df, 'Date', ['Open', 'Prediction'], 'BTC/USD')
log_fig = plotter(df, 'Date', ['log2open', 'PredictedLog2Open'], 'BTC/USD (Log2)')
tickvals = [1, 10, 100, 1000, 2000, 3000, 4000, 5000]
ticktext = [df['Date'].iloc[i-1] for i in tickvals]
loglog_fig = plotter(df, 'dayth', ['log2open', 'PredictedLog2Open'], 'BTC/USD (LogLog)')
loglog_fig.update_layout(xaxis=dict(
        type='log',
        tickvals=tickvals,
        ticktext=ticktext
    ))


app = Dash(__name__,
           meta_tags = [{'name':'viewport',
                       'content': 'width=device-width, initial-scale=0.1, maximum-scale=2,minimun-scale=0.1'}])
server = app.server

app.layout = html.Div(children=[
    html.Div([
            dcc.Markdown(f'# Bitcoin Price Predictor'),
            dcc.Markdown(f"### {latest_date}: ${'{:.0f}'.format(latest_price)} ({'{:.1f}'.format(log2_latest_price)})"),
        html.Div([
            dcc.Input(
                id='date-input',
                type='text',
                placeholder='Enter a date to predict',
                value='2025-01-01'),
            html.Button('Click', id='submit-date', n_clicks=0),
            html.Div(id='date-result', style={'marginTop': '10px'})
            ])], 
            style={'display': 'flex', 
            'flexDirection': 'column', 
            'alignItems': 'center', 
            'width': '100%', 
            'marginBottom': '20px'}),

    html.Div([
        html.Div(id='hover-info', style={'marginLeft': '40%'}),
        dcc.Graph(id='log2-price-graph', figure=log_fig),
        html.Div(id='hover-info-1', style={'marginLeft': '40%'}),
        dcc.Graph(id='price-graph', figure=fig),
        html.Div(id='hover-info-2', style={'marginLeft': '40%'}),
        dcc.Graph(id='loglog-price-graph', figure=loglog_fig)],
        style={'display': 'inline-block', 
               'width': '100%', 
               'verticalAlign': 'top'})
    ], 
    style={'width': '80%', 
    'display': 'flex', 
    'flexDirection': 'column', 
    'alignItems': 'center',
    'margin': '0 10%'
    })

@app.callback(
    Output('date-result', 'children'),
    Input('submit-date', 'n_clicks'),
    State('date-input', 'value')
)
def update_date_result(n_clicks, date_text):
    if n_clicks == 0:
        return html.P('')
    try:
        price_pred, log2_pred = predictor(const, coef, date_text)
    except ValueError:
        return html.P('Invalid date format. Please enter a date in the format YYYY-MM-DD')
    
    max_date = date(2060, 7, 19)
    min_date = date(2010, 7, 19)
    date_object = datetime.strptime(date_text, '%Y-%m-%d').date()
    if date_object > max_date or date_object < min_date:
        return html.P('Date out of range. Please enter a date between 2010-07-19 and 2060-07-19')

    return html.Div([
        dcc.Markdown(f"### Prediction: ${'{:.0f}'.format(price_pred)} ({'{:.1f}'.format(log2_pred)})")
    ])

@app.callback(
    Output('hover-info', 'children'),
    Input('log2-price-graph', 'hoverData'),
)
def display_hover_info(hoverData):
    if hoverData is None:
        return ""
    
    # Extracting information from hoverData
    points = hoverData['points']
    hover_info = []
    x_value = points[0]['x']
    price_curve_0 = None
    price_curve_1 = None

    # Loop through points to find prices for curveNumber 0 and 1
    for point in points:
        curve_number = point['curveNumber']
        y_value = point['y']
        if curve_number == 0:
            price_curve_0 = y_value  # Price for curveNumber 0
        elif curve_number == 1:
            price_curve_1 = y_value  # Price for curveNumber 1

    # Construct the hover info string
    hover_info = f"### {x_value}: {price_curve_0:.1f}"
    
    if price_curve_1 is not None:
        hover_info += f" (pred={price_curve_1:.1f})"  # Add curveNumber 1's price in red

    return html.Div([dcc.Markdown(hover_info)]) # Display all hover info

@app.callback(
    Output('hover-info-1', 'children'),
    Input('price-graph', 'hoverData'),
)
def display_hover_info_1(hoverData):
    if hoverData is None:
        return ""
    
    # Extracting information from hoverData
    points = hoverData['points']
    hover_info = []
    x_value = points[0]['x']
    price_curve_0 = None
    price_curve_1 = None

    # Loop through points to find prices for curveNumber 0 and 1
    for point in points:
        curve_number = point['curveNumber']
        y_value = point['y']
        if curve_number == 0:
            price_curve_0 = y_value  # Price for curveNumber 0
        elif curve_number == 1:
            price_curve_1 = y_value  # Price for curveNumber 1

    # Construct the hover info string
    hover_info = f"### {x_value}: ${price_curve_0:.0f}"
    
    if price_curve_1 is not None:
        hover_info += f" (pred=${price_curve_1:.0f})"  # Add curveNumber 1's price in red

    return html.Div([dcc.Markdown(hover_info)]) # Display all hover info

@app.callback(
    Output('hover-info-2', 'children'),
    Input('loglog-price-graph', 'hoverData'),
)
def display_hover_info_2(hoverData):
    if hoverData is None:
        return ""
    
    # Extracting information from hoverData
    points = hoverData['points']
    hover_info = []
    start_date = date(2010, 7, 19)
    x_value = points[0]['x']
    x_value = (start_date + timedelta(days=x_value - 561)).strftime('%Y-%m-%d')
    price_curve_0 = None
    price_curve_1 = None

    # Loop through points to find prices for curveNumber 0 and 1
    for point in points:
        curve_number = point['curveNumber']
        y_value = point['y']
        if curve_number == 0:
            price_curve_0 = y_value  # Price for curveNumber 0
        elif curve_number == 1:
            price_curve_1 = y_value  # Price for curveNumber 1

    # Construct the hover info string
    hover_info = f"### {x_value}: {price_curve_0:.1f}"

    if price_curve_1 is not None:
        hover_info += f" (pred={price_curve_1:.1f})"  # Add curveNumber 1's price in red

    return html.Div([dcc.Markdown(hover_info)]) # Display all hover info


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
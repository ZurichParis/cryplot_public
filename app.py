from sqlalchemy import create_engine, text as sql_text
from config import DATABASE_URI, score_test, score_train
import pandas as pd
from get_latest import get_latest_day
from get_by_date import get_by_date
from dash import Dash, html, dcc, Input, Output, State
from datetime import datetime, date
from figure_maker import create_figure

# Connect to the database and query data
engine = create_engine(DATABASE_URI)
query = "SELECT * FROM btc_prices"
df = pd.read_sql_query(con=engine.connect(), 
                            sql=sql_text(query))

# get price info(log2, actual) for the last availbale date in df
latest_day = get_latest_day(df)
latest_content = get_by_date(df,latest_day) # list of html.P objects

# Create the figures
fig = create_figure(df, 'Date', ['Open', 'Prediction'], 'BTC/USD')
log2_figure = create_figure(df, 'Date', ['log2open', 'PredictedLog2Open'], 'BTC/USD (Log2)')
tickvals = [1, 10, 100, 1000, 2000, 3000, 4000, 5000]
ticktext = [df['Date'].iloc[i-1] for i in tickvals]
ll_figure = create_figure(df, 'dayth', ['log2open', 'PredictedLog2Open'], 'BTC/USD (LogLog)')
ll_figure.update_layout(xaxis=dict(
        title='Day',
        type='log',
        tickvals=tickvals,
        ticktext=ticktext
    ))

# get price info(actual prices if available, prediction prices) for specific date
app = Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Markdown(f'### Introduction'),
        html.P(f"100% return achieved every time everytime value Y(log2) increases by 1"),
        dcc.Markdown(f'### Model Info'),
        html.P(f"R2 Train: {'{:.4f}'.format(score_train)}"),
        html.P(f"R2 Train: {'{:.4f}'.format(score_test)}"),
        dcc.Markdown(f'### BTC Prices {latest_day}'),
        html.Div(latest_content),
        html.Div([
            dcc.Input(
                id='date-input',
                type='text',
                placeholder='Enter a date (2024-01-01)',
                value='2024-01-01'),
            html.Button('Submit', id='submit-date', n_clicks=0),
            html.Div(id='output-date', style={'marginTop': '10px'})
            ])], 
            style={'display': 'inline-block', 'width': '20%', 
                   'verticalAlign': 'top', 'marginLeft': '20px', 'marginTop': '13px'}),
    html.Div([
        dcc.Graph(id='log2-price-graph', figure=log2_figure),
        dcc.Graph(id='price-graph', figure=fig),
        dcc.Graph(id='loglog-price-graph', figure=ll_figure)],
        style={'display': 'inline-block', 
               'width': '79%', 
               'verticalAlign': 'top','marginLeft': '1%'})
    ], style={'width': '100%', 'display': 'flex'})

@app.callback(
    Output('output-date', 'children'),Input('submit-date', 'n_clicks'),
    State('date-input', 'value')
)
def update_output(n_clicks, date_text):
    if n_clicks == 0:
        return html.P('Enter a date and press submit')
    try:
        date_object = datetime.strptime(date_text, '%Y-%m-%d').date()
    except ValueError:
        return html.P('Invalid date format. Please enter a date in the format YYYY-MM-DD')
    
    max_date = date(2060, 7, 19)
    min_date = date(2010, 7, 19)
    if date_object > max_date or date_object < min_date:
        return html.P('Date out of range. Please enter a date between 2010-07-19 and 2060-07-19')
    content = get_by_date(df, date_object)

    return html.Div([
        dcc.Markdown(f'### BTC Prices {date_object}'),
        html.Div(content)
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
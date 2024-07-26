from sqlalchemy import create_engine, text as sql_text
from config import DATABASE_URI, score_test, formator
import pandas as pd
from get_by_date import get_by_date
from dash import Dash, html, dcc, Input, Output, State
from datetime import datetime, date
from figure_maker import create_figure
import dash_bootstrap_components as dbc
import os

# Connect to the database and query data
engine = create_engine(DATABASE_URI)
query = "SELECT * FROM btc_prices"
df = pd.read_sql_query(con=engine.connect(), 
                            sql=sql_text(query))

# get price and date for the last availbale date in df
latest_day = df.iloc[-1]['Date']
latest_price = formator(df.iloc[-1]['Open'])

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
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags = [{'name':'viewport',
                       'content': 'width=device-width, initial-scale=1.o, maximum-scale=1.0, minimun-scale=1.0'}])
app.layout = dbc.Container([
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('# Introduction', style={'textAlign': 'center'}),
            html.P(
                f"""Here is a tool for bitcoin(btc) price analyzing. Log2 is used in Y axis for the btc daily prices. 
                   Hence each time y value increased by 1, btc price actually doubled. 
                   The prediction(Red) achieved accuracy score of 0.95.""",
                style={'textAlign': 'justify'}
            ),
            html.P(
                "Enter a future date then it tells you the predicted bitcoin price!",
                style={'textAlign': 'justify'}
            ),
        ],  xs=12, sm=12, md=12, lg=12, xl=12, className='side-panel'),        
    ], className="justify-content-center"),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(f'''#### BTC Prices {latest_day}  \n\n ${latest_price}''', style={'textAlign': 'center'}),
            html.Div([
                dcc.Input(
                    id='date-input',
                    type='text',
                    placeholder='Enter a date (2024-01-01)',
                    value='2024-01-01'),
                html.Button('Click', id='submit-date', n_clicks=0),
                html.Div(id='output-date', style={'marginTop': '10px'})
            ], style={'textAlign': 'center'}),
        ],  xs=12, sm=12, md=12, lg=12, xl=12, className='side-panel')
    ], className="justify-content-center"),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='log2-price-graph', figure=log2_figure),
            dcc.Graph(id='price-graph', figure=fig),
            dcc.Graph(id='loglog-price-graph', figure=ll_figure)
        ], width=12, lg=9)
    ], className="justify-content-center"),
], fluid=True)


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
    query_date, query_pred = get_by_date(df, date_object)

    return html.Div([
        dcc.Markdown(f'''#### BTC Prediction {query_date} \n\n ${query_pred}'''),
        ])


if __name__ == "__main__":
    # Get the port from the environment variable (default to 8050 if not set)
    port = int(os.environ.get("PORT", 8050))
    # Run the app
    app.run_server(host='0.0.0.0', port=port, debug=True)

from dash import html
from datetime import date

def get_latest_day(df) -> date:
    latestday = df.iloc[-1]['Date']
    return latestday
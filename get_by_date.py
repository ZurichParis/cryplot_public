import pandas as pd
from datetime import date, datetime
from predictor import predictor
from config import formator

def get_by_date(df: pd.DataFrame, date_obj: date):
    if type(date_obj) is not date:
        date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
    date_string = date_obj.strftime('%Y-%m-%d')
    _, info_pred = predictor(date_obj)
    prediction = formator(info_pred)
    
    return date_string, prediction
    
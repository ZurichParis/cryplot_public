import pandas as pd
from datetime import date, datetime
from output import output_content_list
from predictor import predictor
from config import formator

def get_by_date(df: pd.DataFrame, date_obj: date):
    if type(date_obj) is not date:
        date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
    date_string = date_obj.strftime('%Y-%m-%d')
    
    row = df[df['Date'] == date_string]
    if row.empty:
        log2_info_pred, info_pred = predictor(date_obj)
        log2_info_pred = formator(log2_info_pred)
        info_pred = formator(info_pred)
        historical_content = output_content_list(info_pred, log2_info_pred)
    else:
        info_price = formator(row['Open'].values[0])
        info_pred = formator(row['Prediction'].values[0])
        log2_info_price = formator(row['log2open'].values[0])
        log2_info_pred = formator(row['PredictedLog2Open'].values[0])
        historical_content = output_content_list(info_pred, log2_info_pred, log2_info_price, info_price)
    
    return historical_content
    
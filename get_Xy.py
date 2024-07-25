from sqlalchemy import create_engine, text as sql_text
from config import DATABASE_URI
import pandas as pd

def get_Xy():
    engine = create_engine(DATABASE_URI)
    query = "SELECT dayth, log2dayth, log2open FROM btc_prices ORDER BY dayth"
    df_temp = pd.read_sql_query(con=engine.connect(), 
                            sql=sql_text(query))
    X = df_temp[['log2dayth']]
    y = df_temp['log2open']
    return X, y
from datetime import date
from config import CONST, COEF
import numpy as np

def predictor(date_obj: date) -> tuple:
    print(type(date_obj))
    dayth = 561 + (date_obj - date(2010,7,19)).days
    log2_info_pred = np.log2(dayth) * COEF + CONST
    info_pred = 2 ** log2_info_pred
    log2_info_pred = log2_info_pred
    info_pred = info_pred
    
    return log2_info_pred, info_pred

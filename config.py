CONST = -54.520264886733685
COEF = 5.663924535251358
DATABASE_URI = 'sqlite:///btcusd_data.db'

test_size = 0.1
score_train = 0.954
score_test = 0.959

def formator(x: float) -> str:
    return "{:.1f}".format(x)
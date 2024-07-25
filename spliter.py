from sklearn.model_selection import train_test_split

def spliter(X,y,test_size):
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, shuffle=True, random_state=42)
    return X_train, X_test, y_train, y_test
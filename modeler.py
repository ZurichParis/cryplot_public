from sklearn.linear_model import LinearRegression

def modeler(X_train, X_test, y_train, y_test):
    reg = LinearRegression().fit(X_train,y_train)
    const = reg.intercept_
    score_train = reg.score(X_train,y_train)
    score_test = reg.score(X_test,y_test)
    coef = reg.coef_[0]
    return const, coef, score_train, score_test
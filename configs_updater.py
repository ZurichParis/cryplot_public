import config
# need fix

def configs_updater(const, coef, score_train, score_test):
    setattr(config, "CONST", const)
    setattr(config, "COEF", coef)
    setattr(config, "score_train", score_train)
    setattr(config, "score_test", score_test)
    
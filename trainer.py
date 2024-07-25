from get_Xy import get_Xy
from spliter  import spliter
from config import test_size
from modeler import modeler
import sys
from configs_updater import configs_updater

def trainer(set):
    X, y = get_Xy()
    X_train, X_test, y_train, y_test = spliter(X, y, test_size)
    const, coef, score_train, score_test = modeler(X_train, X_test, y_train, y_test)
    print(f'Intercept (const): {const}')
    print(f'Coefficient (coef): {coef}')
    print(f'Training Score: {score_train}')
    print(f'Test Score: {score_test}')
    if set:
        configs_updater(const, coef, score_train, score_test)
        print('configs updated')


if __name__ == "__main__":
    # Check if enough arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <set_config: True or False>")
        sys.exit(1)
    set_config_arg = sys.argv[1].strip().lower()
    # Access arguments from the command line
    set = sys.argv[1]
    if set_config_arg in ['true', '1', 'yes']:
        set = True
    elif set_config_arg in ['false', '0', 'no']:
        set = False
    else:
        print("Invalid argument. Please use 'True' or 'False'.")
        sys.exit(1)
    
    # Call the trainer function with the converted argument
    trainer(set=set)


    


import config

def get_config(name):
    value = getattr(config, name, None)
    return value

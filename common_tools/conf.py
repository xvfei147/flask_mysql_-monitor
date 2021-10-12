import os
from yaml import load

config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')

with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf = load(cont)


def get_email_args():
    return cf.get('email')


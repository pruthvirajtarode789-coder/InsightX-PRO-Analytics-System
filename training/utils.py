# training/utils.py - helper functions
import pandas as pd, os
BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "..", "data")

def load_customers():
    return pd.read_csv(os.path.join(DATA_DIR, "customers_sample.csv"))

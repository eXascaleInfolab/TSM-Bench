
import os
def store_results( dataset , query , system):
    path = f"results/offline/{dataset}/{query}"
    os.makedirs(path, exist_ok=True)

import json

def load_query_templates(system_name):
    with open(f"systems/{system_name}/queries.sql") as file:
        return [ line.strip()  for line in file.readlines()]
    
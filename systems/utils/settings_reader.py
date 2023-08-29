import json

def read_settings():
	with open("../scenarios.json") as file:
		scenarios = json.load(file)
		return scenarios



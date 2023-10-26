import json

def read_scenarios():
	with open("../scenarios.json") as file:
		scenarios = json.load(file)
		return scenarios



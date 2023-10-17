import random
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from tqdm import tqdm

dtime = datetime(2019, 4, 30, 00)
dtimestamp = datetime.timestamp(dtime)
ms = int(round(dtimestamp * 1000))
n_it = 100
granularity = 10 #seconds

def generate_repeats(length, num_series, repeats_percentage):
	time_series_data = []
	for _ in range(num_series):
		# Ensure the repeats percentage is between 0 and 100
		repeats_percentage = max(0, min(100, repeats_percentage))
		
		time_series = []
		previous_value = random.uniform(0, 1)  # Initialize the first value randomly
		
		for _ in range(length):
			if random.randint(0, 100) < repeats_percentage:
				current_value = previous_value 
			else:
				# Generate a new random value
				current_value = random.uniform(0, 1)
			
			# Ensure the generated value stays within the [0, 1] range
			current_value = max(0, min(1, current_value))
			
			time_series.append(current_value)
			previous_value = current_value
		time_series_data.append(time_series)
	return time_series_data

def generate_scarsity(length, num_series, scarsity_percentage):
	time_series_data = []
	for _ in range(num_series):
		# Ensure the scarsity percentage is between 0 and 100
		scarsity_percentage = max(0, min(100, scarsity_percentage))
		
		time_series = []
		previous_value = random.uniform(0, 1)  # Initialize the first value randomly
		
		for _ in range(length):
			if random.randint(0, 100) < scarsity_percentage:
				current_value = None 
			else:
				# Generate a new random value
				current_value = random.uniform(0, 1)
			time_series.append(current_value)
			previous_value = current_value
		time_series_data.append(time_series)
	return time_series_data

def generate_delta(length, num_series, delta_percentage):
	time_series_data = []
	for _ in range(num_series):
		delta_percentage = max(0, min(100, delta_percentage))
		time_series = []
		previous_value = random.uniform(0, 1)  # Initialize the first value randomly
		for _ in range(length):
			delta = random.uniform(-1 * delta_percentage, delta_percentage )  
			current_value = previous_value + delta
			time_series.append(current_value)
			previous_value = current_value
		time_series_data.append(time_series)
	return time_series_data

def export(ts, file):
	df = pd.DataFrame(ts).T
	df['time'] = [datetime.fromtimestamp((ms + i * 1000 * granularity) // 1000).strftime("%Y/%m/%dT%H:%M:%S") for i in range(len(df))] 
	df['st'] = ['st' + str(i // (len(df) // 10)) for i in range(len(df))] 
	df = df[ ['time'] + ['st'] + [ col for col in df.columns if col != 'time' and col != 'st' ] ]
	df.to_csv(file, index=False)
	return df


length=100
num_series = 1
repeats_percentage=90
scarsity_percentage=10
delta_percentage=10


time_series_data = generate_repeats(length, num_series, repeats_percentage)
time_series_data = export(time_series_data, 'repeats_'+str(repeats_percentage)+'.csv')
# Plot the time series
time_series_data.plot(marker='o', linestyle='-')
plt.title('Repeats ' + str(repeats_percentage) )
plt.xlabel('Time')
plt.ylabel('Value')
plt.grid(True)
plt.show()


time_series_data = generate_scarsity(length, num_series, scarsity_percentage)
time_series_data = export(time_series_data, 'scarsity_'+str(scarsity_percentage)+'.csv')
time_series_data.plot(marker='o', linestyle='-')
plt.title('Scarsity ' + str(scarsity_percentage) )
plt.xlabel('Time')
plt.ylabel('Value')
plt.grid(True)
plt.show()


time_series_data = generate_delta(length, num_series, delta_percentage)
time_series_data = export(time_series_data, 'delta_'+str(delta_percentage)+'.csv')
time_series_data.plot(marker='o', linestyle='-')
plt.title('Delta ' + str(delta_percentage) )
plt.xlabel('Time')
plt.ylabel('Value')
plt.grid(True)
plt.show()

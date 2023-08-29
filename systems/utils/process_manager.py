from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k
from contextlib import contextmanager

@contextmanager
def dbs_manager(system,sleep_time=2):
	system = system.lower()
	assert system in ['monetdb', 'clickhouse', 'questdb', 'timescaledb', 'influx','druid','extremedb']

	if system in ["timescaledb","questdb"]:
		process = Popen(['sh', 'variables.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
		stdout, stderr = process.communicate()

	launch_arguments = ['sh', 'launch.sh']

	if system in ['monetdb','druid','influx','clickhouse']:
		launch_arguments.append('&')

	process = Popen(launch_arguments, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	_, _ = process.communicate()

	process = Popen(['sleep', str(sleep_time)], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
	_ , _  = process.communicate()

	try:
		yield
	finally:
		print("done")
		process = Popen(['sh', 'stop.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
		stdout, stderr = process.communicate()
		print("process stopped")


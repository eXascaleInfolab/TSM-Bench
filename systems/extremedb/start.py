import os
import subprocess


def launch():
	# Command to source the script and print the environment
	command = '/bin/bash -c "source variables.sh; env"'

	# Run the command as a subprocess, capturing the output
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	output, error = proc.communicate()

	# Parse the output to extract the environment variables
	env_lines = [line.decode("utf-8").split('=', 1) for line in output.splitlines() if b'=' in line]
	env = dict(env_lines)


	# Merge the extracted environment variables with the current environment
	new_env = os.environ.copy()
	new_env.update(env)

	new_env["OLDPWD"] = os.getcwd()
	os.environ.update(new_env)


	# Run launch.sh with the modified environment and let it run in the background
	process = subprocess.Popen(['sh', 'launch.sh'], env=new_env, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


	process = subprocess.Popen(['sleep', '10'], env=new_env, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	process.communicate()

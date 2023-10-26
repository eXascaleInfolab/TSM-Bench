import os
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL # py3k

def launch():    
    with change_directory(__file__):
        process = Popen(['sh', 'launch.sh'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

        process = Popen(['sleep', '10'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        stdout, stderr = process.communicate()

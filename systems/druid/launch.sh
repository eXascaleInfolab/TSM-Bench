#!/bin/sh

# Check if the Druid process is running
if ps -ef | grep -q '[d]ruid/' ; then
    echo "Druid is already running. Not starting it again."
else
    # Start the Druid server
    ./apache-druid-25.0.0/bin/start-single-server-medium > /dev/null 2>&1 &

    # Wait for it to start (you can adjust the sleep duration as needed)
    sleep 300
fi

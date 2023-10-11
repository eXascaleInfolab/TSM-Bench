#!/bin/sh

output=$(./apache-druid-25.0.0/bin/start-single-server-medium & > /dev/null &)

echo "$output"

if echo "$output" | grep -q 'maybe another'; then
	echo "not waiting"
	sleep 20
else
	sleep 300
fi


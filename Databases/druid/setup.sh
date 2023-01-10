#!/bin/sh


time ./apache-druid-25.0.0/bin/post-index-task --file load.json --url http://localhost:8081 &

#!/bin/sh

ps -ef | grep 'druid' | grep -v grep | awk '{print $2}' | xargs -r kill -9
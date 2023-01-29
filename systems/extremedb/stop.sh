#!/bin/sh

ps -ef | grep 'xsql' | grep -v grep | awk '{print $2}' | xargs -r kill -9

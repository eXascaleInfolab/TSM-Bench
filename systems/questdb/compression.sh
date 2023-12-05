#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi

. ../config.env


result=$(du -sk "$QuestDBroot/db/$dataset" | cut -f1)
echo "${result}KB"


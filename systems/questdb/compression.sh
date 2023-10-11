#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi

result=$( du -sh $HOME/.questdb/db/$dataset)
echo "$result"


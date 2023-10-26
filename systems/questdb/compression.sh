#!/bin/sh

dataset="d1"
if [ $# -ge 1 ]; then
    dataset="$1"
fi

result=$(du -sk "$HOME/.questdb/db/$dataset" | cut -f1)
echo "${result}KB"


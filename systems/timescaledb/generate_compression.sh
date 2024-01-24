#!/bin/bash

for delta in 1 3 5 10; do
    echo "delta: $delta"
    sh load.sh delta_$delta
done

for scarsity in 10 30 60 80; do
    echo "scarsity: $scarsity"
    sh load.sh scarsity_$scarsity
done


for repeats in 10 30 70 90; do
    echo "repeats: repeats"
    sh load.sh repeats_$repeats
done
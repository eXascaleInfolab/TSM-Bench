

file_name="syn_cond"

for delta in 1 3 5 10; do
    echo "delta: $delta"
    sh load.sh ${file_name}_delta_$delta
done

for scarsity in 10 30 60 80; do
    echo "scarsity: $scarsity"
    sh load.sh ${file_name}_scarsity_$scarsity
done

for outliers in 1 2 3 10; do
    echo "outliers: $outliers"
    sh load.sh ${file_name}_outliers_$outliers
done

for repeats in 10 30 70 90; do
    echo "repeats: repeats"
    sh load.sh ${file_name}_repeats_$repeats
done
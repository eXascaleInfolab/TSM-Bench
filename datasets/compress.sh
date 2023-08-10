cd ..
mkdir -p splits
tar -cvzf - *.csv | split -b 50m - "splits/datasets_splits."

tar -cvzf - *.txt | split -b 50m - "splits/datasets_splits."

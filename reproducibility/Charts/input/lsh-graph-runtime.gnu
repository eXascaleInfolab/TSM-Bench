set terminal pdf enhanced
set output 'lsh-graph-input.pdf'
set sample 100000
set tics font "Helvetica,16"
set title font ",16"
set key font ",16"

set title "Generation runtime vs. Input size"
set xlabel "# datapoints (1k)"
set ylabel "Runtime (s)"



# Now plot the data with lines and points
plot 'lsh-graph-runtime.dat' using 1:2 w lp title 'lsh', \
     '' using 1:3 w lp title 'graph'

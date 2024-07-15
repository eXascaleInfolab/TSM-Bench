set terminal pdf enhanced
set output 'lsh-graph-output.pdf'
set sample 100000

set title "Generation runtime vs. Output size"
set xlabel "# datapoints (1k)"
set ylabel "Runtime (s)"



# Now plot the data with lines and points
plot 'lsh-graph-runtime.dat' using 1:2 w lp title 'lsh', \
     '' using 1:3 w lp title 'graph'

set terminal pdfcairo transparent enhanced font "Gill Sans, 12" linewidth 2 rounded dashed

set style line 80 lc rgb "#202020" lt 1 lw 1
# Border: 3 (X & Y axes)
set border 15 back ls 80

# set style line 81 lc rgb "#808080" lt 1 lw 1
# set grid back ls 81, ls 81

# Assuming that `gnuplot-colorbrewer` is installed.
load 'PuRd.plt'

set xtics border in scale 1,0.5 nomirror rotate by 45 right font ', 10'
set ytics border in scale 1,0.5 nomirror norotate autojustify font ', 9'

set tics scale -0.1
set tics out

set xtics nomirror
set ytics nomirror

set cblabel "Latency (in ms)"

set datafile separator comma

set output OUT_FILE
plot IN_FILE matrix rowheaders columnheaders u 1:2:3 with image pixels
unset output

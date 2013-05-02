#!/bin/sh
cut -f2 | rev | cut -d. -f-2 | rev | sort | uniq -c | sort -nr | egrep '(hu-|tu-|uni-|rwth-)' | head -n20 | gnuplot -p -e "unset key; set term png; set output 'refefe-unis.png'; set ytics rotate by 90; unset xtics; set x2tics border in scale 1,1 nomirror rotate by 90 offset character 0,0,0; set tmargin 10; set style fill solid; plot '-' using 1:x2ticlabels(2) with histogram"; convert -rotate 90 refefe-unis.png refefe-unis.png
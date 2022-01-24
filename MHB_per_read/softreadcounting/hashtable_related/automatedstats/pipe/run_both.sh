infol=$1

ct=CD8TIL

outfile=${infol}_cpgcount.txt

python3 automatedStats_hastbles.py ${infol} ${ct} ${outfile}

python3 summary_heatmap.py ${outfile} ${ct}





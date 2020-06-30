allmatwithgene=$1


corresdict=$2

outfile=${allmatwithgene}_summary_${corresdict}


python3 genesummary.py ${allmatwithgene} ${corresdict} ${outfile}





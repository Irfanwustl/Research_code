nonareportfile=$1  #/Users/irffanalahi/Research/Research_code/gitignorefolder/stereotypicalNA/toy.txt_NoNA_report.txt

rate=$2 ##0.4

outfile=${nonareportfile}_cutoff${rate}.txt

python3 considerforSM.py ${nonareportfile} ${rate}  ${outfile}

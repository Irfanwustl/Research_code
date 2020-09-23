



chrstart=22 #1
chrend=22 #22

proc=30


### a foldername required #####
bamfile1=bamfiles_sorted/TWCY-1382-1382-CD14-PBMC_sorted
bamfile2=bamfiles_sorted/TWCY-1382-1382-CD19-PBMC_sorted


./run_binCoverge_filter.sh ${chrstart} ${chrend} ${proc} ${bamfile1}


./run_clusterdoublebam.sh ${chrstart} ${chrend} ${proc} ${bamfile1} ${bamfile2}


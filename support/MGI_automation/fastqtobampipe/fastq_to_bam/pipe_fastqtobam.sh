#### ENTRY of fastq to bam conversion####



fastqfolder=$1

output_bamfolder=$2

fastqfolderbasename=$(basename ${fastqfolder})

generated_bsub_commandfile=${output_bamfolder}/${fastqfolderbasename}_bamconversion.sh


python3 Generate_command_for_fastqtobam.py ${fastqfolder} ${output_bamfolder} ${generated_bsub_commandfile}

chmod +x ${generated_bsub_commandfile}


${generated_bsub_commandfile}

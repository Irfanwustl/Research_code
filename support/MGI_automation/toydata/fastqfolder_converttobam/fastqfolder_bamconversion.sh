bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder_converttobam/fastqfolder_converttobam_bamconversiion_logs/EM-cfDNA-3.log  -q general -a 'docker(broadinstitute/picard)' java -jar /usr/picard/picard.jar FastqToSam F1=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder/EM-cfDNA-3_R1.fastq.gz F2=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder/EM-cfDNA-3_R2.fastq.gz  O=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder_converttobam/fastqfolder_converttobam_allbams/EM-cfDNA-3/EM-cfDNA-3.bam SM=EM-cfDNA-3

bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder_converttobam/fastqfolder_converttobam_bamconversiion_logs/EM-cfDNA-30.log  -q general -a 'docker(broadinstitute/picard)' java -jar /usr/picard/picard.jar FastqToSam F1=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder/EM-cfDNA-30_R1.fastq.gz F2=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder/EM-cfDNA-30_R2.fastq.gz  O=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder_converttobam/fastqfolder_converttobam_allbams/EM-cfDNA-30/EM-cfDNA-30.bam SM=EM-cfDNA-30

bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder_converttobam/fastqfolder_converttobam_bamconversiion_logs/EM-cfDNA-10.log  -q general -a 'docker(broadinstitute/picard)' java -jar /usr/picard/picard.jar FastqToSam F1=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder/EM-cfDNA-10_R1.fastq.gz F2=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder/EM-cfDNA-10_R2.fastq.gz  O=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder_converttobam/fastqfolder_converttobam_allbams/EM-cfDNA-10/EM-cfDNA-10.bam SM=EM-cfDNA-10

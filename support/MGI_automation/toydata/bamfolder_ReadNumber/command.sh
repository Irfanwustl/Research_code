bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder_ReadNumber/logs/EM_4_cfDNA.log  -q general -a  'docker(irfanwustl/insilico_mix)' samtools view -c /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder/EM_4_cfDNA/tot-67-cfDNA.bam > /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder_ReadNumber/Readnumber/EM_4_cfDNA
bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder_ReadNumber/logs/EM_3_cfDNA.log  -q general -a  'docker(irfanwustl/insilico_mix)' samtools view -c /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder/EM_3_cfDNA/tot-66-cfDNA.bam > /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder_ReadNumber/Readnumber/EM_3_cfDNA
bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder_ReadNumber/logs/EM_10_cfDNA.log  -q general -a  'docker(irfanwustl/insilico_mix)' samtools view -c /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder/EM_10_cfDNA/tot-72-cfDNA.bam > /Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder_ReadNumber/Readnumber/EM_10_cfDNA

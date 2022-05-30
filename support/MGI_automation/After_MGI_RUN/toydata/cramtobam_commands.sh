bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_commands/EM-Seq_03-spike_cramtobam.log  -q general -a 'docker(irfanwustl/insilico_mix)' samtools view -b -T /storage1/fs1/aadel/Active/work/Hg38Reference/all_sequences.fa -o /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_bam/EM-Seq_03-spike.final.bam  /storage1/fs1/aadel/Active/gmsroot/model_data/5dcf9a5fd8f849da99168e857f62bf87/build7b1674aa21624cfd94479a62a41f629e/results/final.cram  
bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_commands/healthy_normal-NU-48-Bulk-WB_cramtobam.log  -q general -a 'docker(irfanwustl/insilico_mix)' samtools view -b -T /storage1/fs1/aadel/Active/work/Hg38Reference/all_sequences.fa -o /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_bam/healthy_normal-NU-48-Bulk-WB.final.bam  /storage1/fs1/aadel/Active/gmsroot/model_data/e97602ec7e3c4c7f9c332ff5b75b90f2/build2dfdbcd465dd45f981d63f4dd09346f0/results/final.cram  
bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_commands/healthy_NU-51-bulk-PBMC_cramtobam.log  -q general -a 'docker(irfanwustl/insilico_mix)' samtools view -b -T /storage1/fs1/aadel/Active/work/Hg38Reference/all_sequences.fa -o /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_bam/healthy_NU-51-bulk-PBMC.final.bam  /storage1/fs1/aadel/Active/gmsroot/model_data/665e272cf0c746579eeef9533dd7f206/buildd84fb3e3648a4d9ea7db8571d3ff9d80/results/final.cram  
bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_commands/BS-Seq_02-spike_cramtobam.log  -q general -a 'docker(irfanwustl/insilico_mix)' samtools view -b -T /storage1/fs1/aadel/Active/work/Hg38Reference/all_sequences.fa -o /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_bam/BS-Seq_02-spike.final.bam  /storage1/fs1/aadel/Active/gmsroot/model_data/98587e37d84442f1b4a35c374b44ce90/build772483d5af4342379cdcff21e5d52a46/results/final.cram  
bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_commands/healthy_NU-49-bulk-PBMC_cramtobam.log  -q general -a 'docker(irfanwustl/insilico_mix)' samtools view -b -T /storage1/fs1/aadel/Active/work/Hg38Reference/all_sequences.fa -o /storage1/fs1/aadel/Active/work/analysis/Automating_MGI/After_MGI/testfilelist3_bam/healthy_NU-49-bulk-PBMC.final.bam  /storage1/fs1/aadel/Active/gmsroot/model_data/c085784e122e46508c0dcc3631872200/build16b5026242524b7b8e23e0acd78694e5/results/final.cram  


bsub -n 20 -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo insilico_training_compute1.log -q general -a 'docker(irfanwustl/insilico_mix)' "bash runinsilico_mix.sh"


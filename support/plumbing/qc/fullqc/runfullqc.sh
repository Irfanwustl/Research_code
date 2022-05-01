
inputfolder=$1

depthprefix=$2


logdir=${inputfolder}_qclogs

mkdir ${logdir}




bsub -n 8 -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo ${logdir}/frag.log -q general -a 'docker(irfanwustl/rpythonsmatools)' ./makefrag.sh ${inputfolder}

bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo ${logdir}/flag.log -q general -a 'docker(irfanwustl/rpythonsmatools)' ./only_flagstat_taken_from_mpp2.sh ${inputfolder}



bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo ${logdir}/depth.log -q general -a 'docker(irfanwustl/rpythonsmatools)' ./makedepth_v2.sh ${inputfolder} ${depthprefix}

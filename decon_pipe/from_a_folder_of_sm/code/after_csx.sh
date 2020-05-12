csx_out=$1
sig=$2


#############rename#################################################
cd ${csx_out}

for f in ./*bedgraph*; do mv -- "$f" "${f//bedgraph*/bg}"; done

cd ..






#########################load variables ##########################

source decon_pipe_variables.txt

###################### combine result ##################################
combine_csx=${csx_out}.txt

python combine_deconvOut.py ${csx_out}  ${combine_csx}




############################ for record result ####################



merged_with_groundtruth=${combine_csx}_${gtFile}_merged
Rscript merge_with_gt.R ${combine_csx} ${gtFile} ${merged_with_groundtruth}





############## if resolution changes, only the below part will change #############################

./plotcorr_ep_pbl_til.sh ${merged_with_groundtruth}



python3 recordPerf.py ${sig} ${combine_csx} ${merged_with_groundtruth} ${masterperf}

######################################################################################




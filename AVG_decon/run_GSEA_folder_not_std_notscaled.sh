
inPath=all_bg_rolled_SigMatrix_FC_threshold_2_g20_SigMatrix_FC_threshold_2__realhyper_g5_combinedOnlyposition_intersected_cyberin_scaled_inverted_selectedinverted  ##in_folder  #####mixfiles folder

sig=SigMatrix_FC_threshold_2_g20_SigMatrix_FC_threshold_2__realhyper_g5_combined

outfolder=mix_${inPath}DeconvResult_notstd_notscaled    ############


mkdir ${outfolder}


fList=($( find ${inPath} -name "*bedgraph_cyberin_scaled_inverted_selectedinverted"  ))


for fl in ${fList[@]}
do
	mix=$(basename ${fl})

	mkdir ${outfolder}/${mix} 
	outPath=${outfolder}/${mix}

	echo ${fl}

	Rscript GSEA_like_not_std_noscaled.R ${sig} ${fl} ${outPath}

	echo "result of ${mix}  saved in ${outPath}"

done


inPath=$1  #"/home/ialahi/work/analysis/weekwise/week3/fix_sig/manual_try/g20_5_out1tilpos/run_decon/all_bg_rolled_Sig_g20_5_manual_filter1Onlyposition_intersected_cyberin_scaled_inverted_selectedinverted"



outfolder=${inPath}_CSxOut


mkdir ${outfolder}

sig=$2  #"Sig_g20_5_manual_filter1"



fList=($( find ${inPath} -name "*bedgraph*"  ))





for fl in ${fList[@]}
do
	mix=$(basename ${fl})

	mkdir ${outfolder}/${mix} 
	outPath=${outfolder}/${mix}

	echo ${mix} 

	docker run -v ${inPath}:/src/data -v ${outPath}:/src/outdir lyronctk/cibersortxfractions  --mixture ${mix}  --sigmatrix ${sig}  --verbose TRUE

	echo "result of ${mix}  saved in ${outPath}"

done


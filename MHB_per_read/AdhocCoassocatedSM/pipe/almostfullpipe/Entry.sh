
smfolder=$1  

longlistofcpg=BluNeuEP_poormanHypo_assigned.txt_bg #NeuPBLpoormanHypo_assigned.txt_mhb #pblsubsetpoormanMHB_hypo.txt_assigned.txt_mhb


radius=150


outdir=${smfolder}_processed

mkdir ${outdir}


dirList=($( ls ${smfolder} ))


i=0
while (( i < ${#dirList[@]} ))
do
	python3 CreateSurroundingFeatureFromExistingSm.py ${smfolder}/${dirList[i]} ${radius} ${smfolder}/${dirList[i]}_radius_${radius} 

	sort -k 1,1 -k2,2n ${smfolder}/${dirList[i]}_radius_${radius} > ${smfolder}/${dirList[i]}_radius_${radius}Sorted

	bedtools merge  -i ${smfolder}/${dirList[i]}_radius_${radius}Sorted > ${smfolder}/${dirList[i]}_radius_${radius}SortedMerged


	bedtools intersect -a ${longlistofcpg} -b ${smfolder}/${dirList[i]}_radius_${radius}SortedMerged -wa -wb -header > ${outdir}/${dirList[i]}WithSurrounding.txt

	(( i++ ))
done






###################### Next manually add blockchr,blockstart and blockend. Then run drop unique on the outdir################### 




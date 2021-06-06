infolder=$1 #/Users/irffanalahi/Research/Research_code/gitignorefolder/metpostprocess/frommetDMRtoBamintersectBEDfile_test/inONLYDMR

offset=10

intermediatefolder=${infolder}_addedoffset_headerdelete



mkdir ${intermediatefolder}




dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	
	python3 addoffset_headdelete.py ${infolder}/${dirList[i]}   ${offset}   ${intermediatefolder}/${dirList[i]}
	
 	(( i++ ))
done



python3 mergealldfinafolderrbindlike_noheader.py ${intermediatefolder} ${intermediatefolder}_rc

uniq ${intermediatefolder}_rc > ${intermediatefolder}_rc_uniq

sort -k 1,1 -k2,2n ${intermediatefolder}_rc_uniq > ${infolder}_readyforBAM.bed


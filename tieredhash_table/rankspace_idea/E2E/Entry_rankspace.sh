

infolder=$1

howmany=$2

reffile=$3  ####for final heat
compartmentfile=$4  ####for final heat

outdir=${infolder}_rankspace

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 towards_rankspace_faster.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}_CpGdelta_info_faster.txt

	python3 heatmap_from_rankspace.py ${outdir}/${dirList[i]}_CpGdelta_info_faster.txt ${howmany}
 	(( i++ ))
done


forheatunderlyingdata_ranked=${infolder}_ranked

mkdir ${forheatunderlyingdata_ranked}

cp ${outdir}/*forheatunderlyingdata_ranked.txt ${forheatunderlyingdata_ranked}/


posforheat=${infolder}_pos
mkdir ${posforheat}

cp ${outdir}/*pos.txt ${posforheat}/

echo Now inflection_point_bilge_fixed

python3 inflection_point_bilge_fixed.py ${forheatunderlyingdata_ranked} ${forheatunderlyingdata_ranked}_inflection_index.txt


echo Now ENTRY_sm_genration_dependent.sh

./ENTRY_sm_genration_dependent.sh ${forheatunderlyingdata_ranked} ${howmany} ${forheatunderlyingdata_ranked}_inflection_index.txt


echo now forheatmap

forheatoutfolder=${reffile}_int_$(basename ${posforheat})

./bedintersect_onefolder.sh ${reffile} ${posforheat} ${forheatoutfolder}


refsortedbyrankpos=${forheatoutfolder}_sortedby_$(basename ${posforheat})

python3 sort_sample_accordingtorank.py ${forheatoutfolder} ${posforheat} ${refsortedbyrankpos}

./pipe_b2c_to_heat.sh ${refsortedbyrankpos} ${compartmentfile}





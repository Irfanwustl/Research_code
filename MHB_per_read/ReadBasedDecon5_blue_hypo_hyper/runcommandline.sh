

sm=$1  #pblsubsetpoormanMHB_hypo.txt_assigned.txt_mhb_sampled
bamfolder=$2

globalout=$3


smbasename=$( basename ${sm} )

outfolder=${globalout}/${smbasename}_result


mkdir ${outfolder}



dirList=($( ls ${bamfolder} | grep -v '\.bai$'))


i=0
while (( i < ${#dirList[@]} ))
do

	#echo nowSM=========${dirList[i]} 

	python3 runcommandline.py ${sm} ${bamfolder}/${dirList[i]}  ${outfolder}/${dirList[i]} 

	


	(( i++ ))

done










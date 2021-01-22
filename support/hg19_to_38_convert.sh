bg_in=$1  #########param=CFEA data folder

outdir=${bg_in}_hg38

out_unmapped=${outdir}_unmapped

dirList=($( ls ${bg_in}  ))

mkdir ${outdir}

mkdir ${out_unmapped}




chain=/home/ialahi/work/CFEA/tools/hg19ToHg38.over.chain.gz



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	/home/ialahi/work/CFEA/tools/liftOver ${bg_in}/${dirList[i]} ${chain} ${outdir}/${dirList[i]}  ${out_unmapped}/${dirList[i]}_unmapped
 	(( i++ ))
done
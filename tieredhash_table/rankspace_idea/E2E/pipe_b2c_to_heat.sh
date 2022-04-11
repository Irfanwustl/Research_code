
bg_in=$1  

phenfile=$2

outdir=${bg_in}_ciberin


./b2c_full_folder_withheader.sh    ${bg_in}   ${outdir}


heatout=${outdir}_forheatmap

mkdir ${heatout}


cp ${outdir}/* ${heatout}/

echo "now heat"

./heat_folder.sh ${heatout} ${phenfile}






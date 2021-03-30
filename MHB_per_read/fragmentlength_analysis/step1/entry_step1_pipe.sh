alloutfolder=$1

suffix=final.txt
allfinaldir=${alloutfolder}_${suffix}

./collectfile.sh  ${alloutfolder} ${suffix}  ${allfinaldir}



readnamedir=${allfinaldir}_readname
./run_seperatereadnames.sh ${allfinaldir} ${readnamedir}


start=$SECONDS

infodepthfolder=$1

outfolder=${infodepthfolder}_bed


mkdir ${outfolder}

python3 depthtobed_notparallal.py ${infodepthfolder} ${outfolder}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

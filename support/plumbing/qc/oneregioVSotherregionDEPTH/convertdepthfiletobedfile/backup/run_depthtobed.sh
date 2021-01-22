infodepthfolder=$1

outfolder=${infodepthfolder}_bed


mkdir ${outfolder}

python3 depthtobed.py ${infodepthfolder} ${outfolder}

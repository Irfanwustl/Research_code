infodepthintersectedfolder=$1

outfolder=${infodepthintersectedfolder}_quantile

col=3


mkdir ${outfolder}

python3 quantile_report.py ${infodepthintersectedfolder} ${outfolder} ${col}

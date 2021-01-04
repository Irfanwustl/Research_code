######all files in th foldr must have .txt extension

infolder=$1
outname=${infolder}_report.txt
python3 report.py ${infolder} ${outname}


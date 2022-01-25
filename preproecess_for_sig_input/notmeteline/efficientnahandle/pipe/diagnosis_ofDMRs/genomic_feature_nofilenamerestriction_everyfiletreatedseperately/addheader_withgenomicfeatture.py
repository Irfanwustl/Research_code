import pandas as pd 
import sys
import os.path

import re


inputfile=sys.argv[1]

if os.path.getsize(inputfile) == 0:
	sys.exit(0)


inputfiledf=pd.read_csv(inputfile,sep="\t",header=None,low_memory = False)

outfile=sys.argv[2]


inputfilebasename=os.path.basename(inputfile)





if "All_Gene_Info.txt_prom1000_sorted" in inputfilebasename:
	region="promoter"
elif "3utrexon" in inputfilebasename:
	region="3utrexon"
elif "5utrexon" in inputfilebasename:
	region="5utrexon"
elif "cds" in inputfilebasename:
	region="cds"
elif "intron" in inputfilebasename:
	region="intron"
elif "repeat" in inputfilebasename:
	region="repeat"
elif "notfound" in inputfilebasename:
	region="notfound"
else:
	print("error in region")
	sys.exit(1)



outdf=inputfiledf.rename(columns={0: "chrom", 1: "start",2:"end",inputfiledf.columns[-1]:"Gene/Repeat type"})
outdf['Region']=region


outdf.to_csv(outfile,sep="\t",index=False)





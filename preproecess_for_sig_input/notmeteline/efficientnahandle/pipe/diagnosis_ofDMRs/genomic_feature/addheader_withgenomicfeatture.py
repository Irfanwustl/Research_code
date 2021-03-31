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

m = re.search('g1_(.+?)_\d+_g2', inputfilebasename)
if m:
    found = m.group(1)

else:
	print("found=",found)
	print("exiting")

	sys.exit(1)




celltype=found



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



outdf=inputfiledf.rename(columns={0: "chrom", 1: "start",2:"end",3:"q",4:celltype+"-others",5:"#cpg",6:"p(MWU)",7:"p(2dks)",8:celltype,9:"others",inputfiledf.columns[-1]:"Gene/Repeat type"})
outdf['Region']=region


outdf.to_csv(outfile,sep="\t",index=False)





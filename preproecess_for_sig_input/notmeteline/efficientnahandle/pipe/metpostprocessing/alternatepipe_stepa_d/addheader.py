import pandas as pd 
import sys

import re


inputfile=sys.argv[1]

inputfiledf=pd.read_csv(inputfile,sep="\t",header=None)

outfile=sys.argv[2]


m = re.search('g1_(.+?)_\d+_g2', inputfile)
if m:
    found = m.group(1)

else:
	print("found=",found)
	print("exiting")

	sys.exit(1)




celltype=found


outdf=inputfiledf.rename(columns={0: "chrom", 1: "start",2:"end",3:"q",4:celltype+"-others",5:"#cpg",6:"p(MWU)",7:"p(2dks)",8:celltype,9:"others"})


outdf.to_csv(outfile,sep="\t",index=False)











import pandas as pd
import re

import sys

biggerfile=sys.argv[1]

outfile=sys.argv[2]


biggerdf=pd.read_csv(biggerfile,sep="\t",header=None,skiprows=1)



def headerfix():

    m = re.search('g1_(.+?)_\d+_g2', biggerfile)
    if m:
        found = m.group(1)

    else:
        print("cell type not found", biggerfile)
        print("exiting")

        sys.exit(1)

    celltype = found
    
  
    
    
    newcolnames=["DMRchrom","DMRstart","DMRend","q","diff","#cpg","p(MWU)","p(2dks)",celltype,"others"]
    return newcolnames


with open (biggerfile) as f:
    line=f.readline()
    line=line.split("\n")
    colnames=line[0].split("\t")


furthercols=headerfix()
totalcols=colnames+furthercols

biggerdf.columns=totalcols

biggerdf.to_csv(outfile,sep="\t",index=False)

import sys
import pandas as pd

sm=sys.argv[1]

out=sys.argv[2]


smdf=pd.read_csv(sm,sep="\t",dtype=str)

smdf['position']=smdf['chrom'].str.cat(smdf['start'],sep=":")

outdf=smdf[['position','celltype']]




outdf.to_csv(out,sep="\t",index=False)
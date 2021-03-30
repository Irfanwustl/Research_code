import pandas as pd
import sys

infile=sys.argv[1]
infocolname=sys.argv[2]
outfile=sys.argv[3]



indf=pd.read_csv(infile,sep="\t")
outdf=indf[infocolname]

outdf.to_csv(outfile,sep="\t",index=False,header=None)





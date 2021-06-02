import pandas as pd
import sys

sortedfile=sys.argv[1]
numofdmr=int(sys.argv[2])
outfile=sys.argv[3]

sorteddf=pd.read_csv(sortedfile,sep="\t")

if numofdmr<0:
	outdf=sorteddf
else:
	outdf=sorteddf.head(n=numofdmr)

outdf.to_csv(outfile,sep="\t",index=False,header=False)

import pandas as pd
import sys


infile=sys.argv[1]
outfile=sys.argv[2]

topnumber=int(sys.argv[3])


indf=pd.read_csv(infile,sep='\t')

outdf=indf.head(n=topnumber)


outdf.to_csv(outfile,sep='\t',index=False)

import pandas as pd 

import sys
















infile=sys.argv[1]
outfile=sys.argv[2]


indf=pd.read_csv(infile,sep="\t")



#print(indf)

outdf=indf.dropna()

#print(outdf)

outdf.to_csv(outfile,sep="\t",index=False)




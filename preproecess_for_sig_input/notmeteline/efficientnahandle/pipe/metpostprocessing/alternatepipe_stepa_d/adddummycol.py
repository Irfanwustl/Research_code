

import pandas as pd 
import sys




inputfile=sys.argv[1]

inputfiledf=pd.read_csv(inputfile,sep="\t")

outfile=sys.argv[2]


inputfiledf['dummy1']=-1
inputfiledf['dummy2']=-1
inputfiledf['dummy3']=-1
inputfiledf['dummy4']=-1
inputfiledf['dummy5']=-1
inputfiledf['dummy6']=-1  #### does dummy adds to the end always?

outdf=inputfiledf


outdf.to_csv(outfile,sep="\t",index=False)











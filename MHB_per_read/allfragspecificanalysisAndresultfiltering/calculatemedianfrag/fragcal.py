import pandas as pd
import sys
from collections import defaultdict


finalfile=sys.argv[1]
outfile=sys.argv[2]

finaldf=pd.read_csv(finalfile,sep="\t",index_col=0)

celltyplist=["MEL_TUMOR","PBL","TIL"]   #####hardcoded



finaldf=finaldf[finaldf['fraglength']!=-1]



fragdict=defaultdict(list)
for cell in celltyplist:
	pos=finaldf[finaldf['finalacceptedfor']==cell]

	summaryfraglength=pos['fraglength'].median()

	fragdict[cell].append(summaryfraglength)



outdf=pd.DataFrame(fragdict)

outdf.to_csv(outfile,sep="\t",index=False,na_rep="NA")







import pandas as pd 

import sys

ref=pd.read_csv(sys.argv[1],sep="\t")
outname=sys.argv[2]


outdf=ref.drop_duplicates(subset=['chrom', 'start','end'], keep=False)


outdf.to_csv(outname,sep="\t",index=False)



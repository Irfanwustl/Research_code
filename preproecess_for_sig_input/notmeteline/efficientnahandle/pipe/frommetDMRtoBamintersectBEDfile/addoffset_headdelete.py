import pandas as pd
import sys




infile=sys.argv[1]
offset=int(sys.argv[2])

outfile=sys.argv[3]


indf=pd.read_csv(infile,sep="\t")


indf['start']=indf['start'] - offset
indf['end']=indf['end'] + offset

indf.loc[indf['start'] < 0,'start']=0   

outdf=indf[['chrom','start','end']]

outdf.to_csv(outfile,sep="\t",index=False,header=False)





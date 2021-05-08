import pandas as pd
import sys

infile=sys.argv[1]
outfile=sys.argv[2]
infocolname=["ReadName","acceptedCpGLen","notacceptedCpGLen","len_hypolist","len_hyperlist","fraglength","finalacceptedfor","finalrejectedfor"]   #hardcoded




indf=pd.read_csv(infile,sep="\t")
outdf=indf[infocolname]

outdf.to_csv(outfile,sep="\t",index=False)





import pandas as pd 
import sys






def mymerge(rdf,pldf,ffile):
	outdf=rdf.merge(pldf,left_on='Composite Element REF', right_on='ID_REF')

	outdf=outdf.drop(["Composite Element REF","ID_REF"],axis=1)
	outdf.to_csv(ffile,sep="\t",index=False,header = False)


















reffile=sys.argv[1]


plosfile=sys.argv[2]

outname=sys.argv[3]

refdf=pd.read_csv(reffile,sep="\t")





plosdf=pd.read_csv(plosfile,sep="\t")

mymerge(refdf,plosdf,outname)


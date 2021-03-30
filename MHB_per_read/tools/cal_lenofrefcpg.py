import pandas as pd
import sys

infile=sys.argv[1]
outfinal=sys.argv[2]

infinal=pd.read_csv(infile,sep="\t")




infinal['acceptedCpG']=infinal.acceptedCpG.apply(lambda x: x[1:-1].split(','))
infinal['acceptedCpG']=infinal.acceptedCpG.apply(lambda x:[i for i in x if eval(i)] )  ###### understand it

infinal['notacceptedCpG']=infinal.notacceptedCpG.apply(lambda x: x[1:-1].split(','))
infinal['notacceptedCpG']=infinal.notacceptedCpG.apply(lambda x:[i for i in x if eval(i)] )

infinal['mismatchCpG']=infinal.mismatchCpG.apply(lambda x: x[1:-1].split(','))
infinal['mismatchCpG']=infinal.mismatchCpG.apply(lambda x:[i for i in x if eval(i)] )





infinal['acceptedCpGLen']=infinal['acceptedCpG'].str.len()
infinal['notacceptedCpGLen']=infinal['notacceptedCpG'].str.len()
infinal['mismatchCpGLen']=infinal['mismatchCpG'].str.len()

infinal.to_csv(outfinal,sep="\t",index=False)

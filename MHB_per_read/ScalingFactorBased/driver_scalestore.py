import pandas  as pd
import sys
import scalemasterdf

sm=sys.argv[1]
finalfile=sys.argv[2]


smdf=pd.read_csv(sm,sep="\t")

finaldf=pd.read_csv(finalfile,sep="\t")


smdf['celltype']=smdf.celltype.apply(lambda x: x[1:-1].split(','))



finaldf['acceptedCpG'] = finaldf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['notacceptedCpG'] = finaldf.notacceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['CheckedCpG'] = finaldf.CheckedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['finalrejectedfor']=finaldf.finalrejectedfor.apply(lambda x: x[1:-1].split(','))




scaleobj=scalemasterdf.ScaleMasterdf(smdf,finaldf)

scaldf=scaleobj.coreAlgo()

scaldf.to_csv(finalfile+"_scaleinfo.txt",sep="\t",index=False)



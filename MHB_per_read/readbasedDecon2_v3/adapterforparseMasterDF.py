import pandas as pd
import parseMasterDF
import helpadapter
import sys
import os.path

masterdffile=sys.argv[1]
outdir=sys.argv[2]
percentcpgforrejection=float(sys.argv[3]) ### 0 to 1
mincpgforpoditivecall=int(sys.argv[4])

masterdfbasename=os.path.basename(masterdffile)
outmasterpath=outdir+"/"+masterdfbasename

masterdf=pd.read_csv(masterdffile,sep="\t")


#masterdf['CheckedCpG'] = masterdf.CheckedCpG.apply(lambda x: x[1:-1].split(','))
masterdf['acceptedCpG']=masterdf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
masterdf['notacceptedCpG']=masterdf.notacceptedCpG.apply(lambda x: x[1:-1].split(','))
masterdf['mismatchCpG']=masterdf.mismatchCpG.apply(lambda x: x[1:-1].split(','))








masterdf['ucelltype']=masterdf.ucelltype.apply(lambda x: x[1:-1].split(','))




helpucelltype=helpadapter.Helpadapter(masterdf.copy(),'ucelltype')

adjustedDF=helpucelltype.adjustCellListRow()

if masterdf.shape!=adjustedDF.shape:
    print("something wrong in adjustment.Exiting")
    sys.exit(1)


celllist=["'CD14'","'CD19'","'CD4'","'CD8'","'CD56'","'Neu'","'EPCAM'"]      ###########################################################################


pMDF=parseMasterDF.ParseMasterDF(adjustedDF,celllist,percentCpGcoverforrejection=percentcpgforrejection,minCpGforpositivecall=mincpgforpoditivecall)

finaldf,ABSestimate,ABSestimateNormalized=pMDF.coreAlgo()


finaldfname=outmasterpath+"_rej"+str(percentcpgforrejection)+"_mincpg"+str(mincpgforpoditivecall)+"_final.txt"
finaldf.to_csv(finaldfname,sep="\t", index=False)



ABSestimate.to_csv(finaldfname+"_ABSreadcount_divisioned.txt",sep="\t", index=False)




ABSestimateNormalized.to_csv(finaldfname+"_ABSreadcount_divisionedNormalized.txt",sep="\t", index=False)


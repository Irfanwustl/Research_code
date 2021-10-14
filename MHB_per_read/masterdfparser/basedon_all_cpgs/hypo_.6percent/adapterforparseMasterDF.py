import pandas as pd
import parseMasterDF
import helpadapter
import sys
import os.path

masterdffile=sys.argv[1]
outdir=sys.argv[2]
mincpgforpoditivecall=int(sys.argv[3])
percentcpgforrejection=float(sys.argv[4]) ### 0 to 1

rejectionMode=sys.argv[5]   ########## 'ov' or 'nov'


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

helpucelltype=helpadapter.Helpadapter(adjustedDF.copy(),'acceptedCpG')

adjustedDF=helpucelltype.adjustCellListRow()

helpucelltype=helpadapter.Helpadapter(adjustedDF.copy(),'notacceptedCpG')

adjustedDF=helpucelltype.adjustCellListRow()




if masterdf.shape!=adjustedDF.shape:
    print("something wrong in adjustment.Exiting")
    sys.exit(1)


celllist=["mNeu"]      ###########################################################################


pMDF=parseMasterDF.ParseMasterDF(adjustedDF,celllist,percentCpGcoverforrejection=percentcpgforrejection,minCpGforpositivecall=mincpgforpoditivecall,rejectionmode=rejectionMode)

finaldf,ABSestimate,ABSestimateNormalized,poscountdf,allcountdf,negcountdf=pMDF.coreAlgo()


finaldfname=outmasterpath+"_rej"+str(percentcpgforrejection)+"_mincpg"+str(mincpgforpoditivecall)+"_rejmode_"+rejectionMode+"_final.txt"
finaldf.to_csv(finaldfname,sep="\t", index=False)



ABSestimate.to_csv(finaldfname+"_ABSreadcount_divisioned.txt",sep="\t", index=False)




ABSestimateNormalized.to_csv(finaldfname+"_ABSreadcount_divisionedNormalized.txt",sep="\t", index=False)


poscountdf.to_csv(finaldfname+"_posCount.txt",sep="\t", index=False)


allcountdf.to_csv(finaldfname+"_allCount.txt",sep="\t", index=False)


negcountdf.to_csv(finaldfname+"_negCount.txt",sep="\t", index=False)









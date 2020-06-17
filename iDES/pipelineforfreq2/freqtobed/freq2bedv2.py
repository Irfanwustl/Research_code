###param1 =freq file 

###param2=path with name of out file








import pandas as pd

import sys
import math







def generatebed(df_freq,bedfile):
	allrows=[]


	df_freq_rownum=df_freq.shape[0]

	rindex=0
	while rindex < df_freq_rownum:
		Crow=df_freq.iloc[rindex,:]
		

		mergedrow=generateRow(Crow)

		if mergedrow[3]!=-1:
			allrows.append(mergedrow)

		rindex=rindex+1



	beddf = pd.DataFrame(allrows)



	beddf.to_csv(bedfile,sep="\t",index=False,header = False)


def methcal(depth,meth,unmeth):
	if depth!=(meth+unmeth):
		print ("error in depth")
		sys.exit(1)

	beta=0
	if depth>0:
		beta=meth/float(meth+unmeth)
		betaSymbol=str(beta)
	else:
		betaSymbol="."
	return beta,betaSymbol


def generateRow(Crow):
	
	Cmeth=Crow['R+']
	Cunmeth=Crow['T+']

	Cdepth=Cmeth+Cunmeth

	Cbeta,CbetaSymbol=methcal(Cdepth,Cmeth,Cunmeth)



	
	Gmeth=Crow['R-']
	Gunmeth=Crow['T-']

	Gdepth=Gmeth+Gunmeth

	Gbeta,GbetaSymbol=methcal(Gdepth,Gmeth,Gunmeth)

	lastField=Crow['REF']+":"+CbetaSymbol+":"+str(Cdepth)+","+"G"+":"+GbetaSymbol+":"+str(Gdepth)

	if (Cdepth+Gdepth) > 0:
		finalbeta=(Cdepth*Cbeta+Gdepth*Gbeta)/float(Cdepth+Gdepth)
	else:
		finalbeta=-1

	chrom=Crow['CHR']



	
	startpos=Crow['POS']-1
	endpos=Crow['POS']+1

	totaldepth=Cdepth+Gdepth
	if totaldepth!=Crow['DEPTH']:
		print(totaldepth)
		print(Crow['DEPTH'])
		print("totaldepth missmatch")
		sys.exit(1)


	rowlikelist=[chrom,startpos,endpos,finalbeta,totaldepth,lastField]

	

	return rowlikelist





	













freqfile=sys.argv[1]

bedfile=sys.argv[2]

df = pd.read_csv(freqfile, sep="\t")





generatebed(df,bedfile)







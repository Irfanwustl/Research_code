###param1 =freq file 

###param2=path with name of out file








import pandas as pd

import sys
import math







def generatefreq(df_freq,bedfile):
	allrows=[]


	df_freq_rownum=df_freq.shape[0]

	rindex=0
	while rindex < df_freq_rownum:
		Crow=df_freq.iloc[rindex,:]
		Grow=df_freq.iloc[rindex+1,:]

		mergedrow=generateRow(Crow,Grow)

		

		allrows.append(mergedrow)

		rindex=rindex+2



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


def generateRow(Crow,Grow):
	Cdepth=Crow['DEPTH']
	Cmeth=Crow['R+']
	Cunmeth=Crow['T+']

	Cbeta,CbetaSymbol=methcal(Cdepth,Cmeth,Cunmeth)



	Gdepth=Grow['DEPTH']
	Gmeth=Grow['R+']
	Gunmeth=Grow['A+']

	Gbeta,GbetaSymbol=methcal(Gdepth,Gmeth,Gunmeth)

	lastField=Crow['REF']+":"+CbetaSymbol+":"+str(Cdepth)+","+Grow['REF']+":"+GbetaSymbol+":"+str(Gdepth)


	finalbeta=(Cdepth*Cbeta+Gdepth*Gbeta)/float(Cdepth+Gdepth)

	chrom=Crow['CHR']
	if chrom!=Grow['CHR']:
		print("chrom error")
		sys.exit(1)


	
	startpos=Crow['POS']-1
	endpos=Grow['POS']

	totaldepth=Cdepth+Gdepth
	rowlikelist=[chrom,startpos,endpos,finalbeta,totaldepth,lastField]

	

	return rowlikelist





	













freqfile=sys.argv[1]

bedfile=sys.argv[2]

df = pd.read_csv(freqfile, sep="\t")


if df.shape[0]%2!=0:
	print("uneven row in freq file: ")
	print(df.shape)
	sys.exit(1)


generatefreq(df,bedfile)







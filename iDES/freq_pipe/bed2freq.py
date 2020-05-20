###param1 =bed file with depth

###param2=path with name of out file








import pandas as pd

import sys
import math




def generatefreq(df_bed,ffile):
	column_names=["CHR","POS","DEPTH","REF","R+","R-","A+","A-","C+","C-","T+","T-","G+","G-"]
	freqdf = pd.DataFrame(columns = column_names)


	df_bed_rownum=df.shape[0]
	for rindex in range(df_bed_rownum):
		onerow=df_bed.iloc[rindex,:]
		Crow,Grow=splitOneRow(onerow)
		freqdf=freqdf.append(Crow,ignore_index=True)
		freqdf=freqdf.append(Grow,ignore_index=True)

	freqdf.to_csv(ffile,sep="\t",index=False)


def parseDepthCol(singlePart):
	meth=0
	unmeth=0

	strlist=singlePart.split(":")
	chrom=strlist[0]
	depth=int(strlist[2])
	if depth>0:
		beta=float(strlist[1])
		meth=math.floor(beta*depth)
		unmeth=depth-meth

		if unmeth<0:
			print ("error in meth cal")
			sys.exit(1)



	return chrom,depth,meth,unmeth



def splitOneRow(onerow):
	
	Gpos=onerow[2]
	Cpos=Gpos-1


	depthCol = onerow[5]
	strlist=depthCol.split(",")
	cPart=strlist[0]
	gPart=strlist[1]


	fchrom,fdepth,fmeth,funmeth=parseDepthCol(cPart)

	if fchrom!="C":
		print ("wrong forward strand")
		sys.exit(1)

	chrom=onerow[0]	
	Crow={"CHR":chrom,"POS":Cpos,"DEPTH":fdepth,"REF":fchrom,"R+":fmeth,"R-":0,"A+":0,"A-":0,"C+":0,"C-":0,"T+":funmeth,"T-":0,"G+":0,"G-":0} 
	
	rchrom,rdepth,rmeth,runmeth=parseDepthCol(gPart)
	if (rchrom!="G"):
		print ("wrong reverse strand")
		sys.exit(1)

	Grow={"CHR":chrom,"POS":Gpos,"DEPTH":rdepth,"REF":rchrom,"R+":rmeth,"R-":0,"A+":runmeth,"A-":0,"C+":0,"C-":0,"T+":0,"T-":0,"G+":0,"G-":0}



	return Crow,Grow
	
















bedfile=sys.argv[1]

freqfile=sys.argv[2]

df = pd.read_csv(bedfile, header=None,sep="\t")

generatefreq(df,freqfile)



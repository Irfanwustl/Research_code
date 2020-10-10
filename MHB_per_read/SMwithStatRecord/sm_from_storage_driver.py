
import smFromStorage

import pandas as pd


import sys
statinfofile=sys.argv[1]  #"result_out/testout.txt"

phenfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code_using_standard_practise/data/meth_phen_class_irf_only_relevant.txt"

outfile=sys.argv[3]


qcutoff=float(sys.argv[4])
fcutoff=float(sys.argv[5])
minnumfeature=int(sys.argv[6])
maxnumfeature=int(sys.argv[7])
gap=int(sys.argv[8])

if gap==0:
	print("gap should not be 0, changing to 1")
	gap=1

statinfo=pd.read_csv(statinfofile,sep="\t",index_col=0)

phenoClass=pd.read_csv(phenfile,sep="\t",header=None,index_col=0)



startfeature=minnumfeature

while startfeature<=maxnumfeature:
	outfname=outfile+"_g"+str(startfeature)+".txt"
	test=smFromStorage.SmFromStorage(statinfo, phenoClass, qcutoff, fcutoff, startfeature,outfname)
	startfeature=startfeature+gap

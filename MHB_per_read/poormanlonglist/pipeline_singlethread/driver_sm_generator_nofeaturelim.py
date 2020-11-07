import sys
from sm_generator import TTest_hooked
import pandas as pd
import math

reffile=sys.argv[1]
phenfile=sys.argv[2]

outdir=sys.argv[3]

qvalue=float(sys.argv[4])

FC=float(sys.argv[5])

numfeature=math.inf

rdf=pd.read_csv(reffile,sep="\t",index_col=0)




phenoClass=pd.read_csv(phenfile,sep="\t",header=None,index_col=0)



thooktest=TTest_hooked(rdf,phenoClass,'TTest',qvalue,FC,numofFeature=numfeature,outdir=outdir)


thooktest.generateSM()
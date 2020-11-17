

import sys
import filterFeature
import pandas as pd


smfilepath=sys.argv[1]
sm=pd.read_csv(smfilepath,sep="\t")
#sm['celltype']=sm.celltype.apply(lambda x: x[1:-1].split(','))
masterdir=sys.argv[2]
ff=filterFeature.FilterFeature(sm,masterdir,smfilepath)

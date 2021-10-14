import ReadAssign

import pandas as pd


import sys

smfile=sys.argv[1]

bamfilepath=sys.argv[2]


outpath=sys.argv[3]

sm=pd.read_csv(smfile, sep="\t")



#### for our data howsm should be default(no need to mention)###
b=ReadAssign.ReadAssign(bamfilepath, 40, 0,sm,outpath)
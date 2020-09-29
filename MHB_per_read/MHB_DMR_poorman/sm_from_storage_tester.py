
import poormanMHBsm

import pandas as pd



statinfofile="result_out/testout.txt"

phenfile="/Users/irffanalahi/Research/Research_code_using_standard_practise/data/meth_phen_class_irf_only_relevant.txt"

statinfo=pd.read_csv(statinfofile,sep="\t",index_col=0)

phenoClass=pd.read_csv(phenfile,sep="\t",header=None,index_col=0)

test=poormanMHBsm.poormanMHBsm(statinfo,phenoClass,.8,0,2,radius=100)
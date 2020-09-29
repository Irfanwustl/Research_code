import StoreStat

import pandas as pd



reffile="/Users/irffanalahi/Research/Research_code_using_standard_practise/data/q25d1.txt_inverted_head.txt"
phenfile="/Users/irffanalahi/Research/Research_code_using_standard_practise/data/meth_phen_class_irf_only_relevant.txt"

rdf=pd.read_csv(reffile,sep="\t",index_col=0)




phenoClass=pd.read_csv(phenfile,sep="\t",header=None,index_col=0)



ss=StoreStat.StoreStat(rdf,phenoClass,"result_out/testout.txt")

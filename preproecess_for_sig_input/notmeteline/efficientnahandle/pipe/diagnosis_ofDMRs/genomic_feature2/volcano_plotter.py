import pandas as pd 

from bioinfokit import analys, visuz
import sys

inputfile=sys.argv[1]


# load dataset as pandas dataframe


df = pd.read_csv(inputfile,sep="\t")



visuz.gene_exp.volcano(df=df, lfc=df.columns[4],lfc_thr=[0.3],pv_thr=[0.000000001], pv='q',figtype="pdf")
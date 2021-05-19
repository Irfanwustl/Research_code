#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
alldmrperformance=sys.argv[1] #  "//Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test/getAUC/TILfinaldmr_report.txt"
AucCOL=sys.argv[2] #"PreTxNDBvsHealthy_AUC_TIL"
out=alldmrperformance+"_"+AucCOL+".txt"

alldmrperformancedf=pd.read_csv(alldmrperformance,sep="\t")
#alldmrperformancedf['Unnamed: 0']


# In[2]:


alldmrperformancedf.rename(columns={AucCOL: 'c'},inplace=True)
alldmrperformancedf[['chrom','start','end']] = alldmrperformancedf['Unnamed: 0'].str.split("_",expand=True)


alldmrperformancedf['end'] = alldmrperformancedf['end'].str.replace(r'.txt$', '')
outdf=alldmrperformancedf[['chrom','start','end','c']]


outdf.to_csv(out,na_rep='NA',sep="\t",index=False)


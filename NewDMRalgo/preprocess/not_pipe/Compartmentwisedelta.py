#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

rowmeanfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/ITGAEandERICH1_cin_nr0.5_imputed_rowmean.txt"

phenfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/LTMEourCD8TILLwithBLOURPBLPhenoClass.txt"
celltype="CD8TIL"
pheno=pd.read_csv(phenfile,sep="\t", header=None, index_col=0)
outfile=rowmeanfile+"_compdeltafor_"+celltype+".txt"
rowmeandf=pd.read_csv(rowmeanfile,sep="\t",index_col=0)


# In[2]:


def comparmentwisdiff():
    cells=(pheno.index).tolist()

    newdf=pd.DataFrame()
    for cell in cells:
        if cell!=celltype:
            tempdelta=celltype+"-"+cell
            newdf[tempdelta]=rowmeandf[celltype]-rowmeandf[cell]

    return newdf       


# In[3]:


outdf=comparmentwisdiff()
outdf.to_csv(outfile,sep="\t")

